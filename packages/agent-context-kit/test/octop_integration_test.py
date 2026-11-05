"""Real Octop Harness graph, plugin loader, tools and checkpoints with a recording model."""

import importlib.util
import json
import os
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


PLUGIN = Path(__file__).resolve().parents[1] / "integrations" / "octop"
BLOCKS = """<!--BLOCK_ID:modeling-->
MODELING_GUIDANCE
<!--/BLOCK_ID:modeling-->
<!--BLOCK_ID:duplicate-->
DUPLICATE_GUIDANCE
<!--/BLOCK_ID:duplicate-->
<!--BLOCK_ID:duplicate-->
OTHER_DUPLICATE_GUIDANCE
<!--/BLOCK_ID:duplicate-->
"""


@unittest.skipUnless(
    os.name == "posix" and importlib.util.find_spec("octop_harness"),
    "requires POSIX and octop-harness==1.0.7",
)
class OctopHarnessIntegrationTest(unittest.IsolatedAsyncioTestCase):
    async def test_loaded_plugin_projects_model_context_and_checks_native_reads(self):
        from langchain_core.language_models import BaseChatModel
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
        from langchain_core.outputs import ChatGeneration, ChatResult
        from langchain_core.tools import tool
        from octop_harness import ChatRequest, HarnessAgent, HarnessAgentConfig, ModelConfig, ProviderConfig
        from octop_harness.llm.factory import ChatModelFactory
        from octop_harness.plugins import PluginRegistry
        from octop_harness.plugins.loader import load_plugin_dir

        @tool
        def sample_output() -> str:
            """Return an ephemeral fixture."""
            return "<!--ephemeral-->\nTRANSIENT_PAYLOAD"

        class RecordingModel(BaseChatModel):
            seen: list = []
            calls: list = []
            tool_names: list = []

            @property
            def _llm_type(self):
                return "octop-context-test"

            def bind_tools(self, tools, **kwargs):
                self.tool_names.append({tool.name for tool in tools})
                return self

            def _generate(self, messages, stop=None, run_manager=None, **kwargs):
                self.seen.append(messages)
                response = AIMessage(content="OK")
                if len(self.seen) == 1:
                    response = AIMessage(content="", tool_calls=self.calls)
                return ChatResult(generations=[ChatGeneration(message=response)])

        class RecordingFactory(ChatModelFactory):
            def get_chat_model(self, model_ref, **kwargs):
                return model

        with TemporaryDirectory() as temp:
            base = Path(temp).resolve()
            workspace = base / "project"
            workspace.mkdir()
            for directory in ("skills", ".octop/skills", ".octop/_builtin_skills"):
                (workspace / directory).mkdir(parents=True)
            (workspace / "public.txt").write_text("PUBLIC_PAYLOAD")
            generated = workspace / "generated"
            generated.mkdir()
            (generated / ".agent-no-read.md").write_text("USE_API_GUIDE")
            (generated / "private.txt").write_text("PROTECTED_PAYLOAD")
            (workspace / "alias.txt").symlink_to(generated / "private.txt")

            plugin = base / "installed-plugin"
            shutil.copytree(PLUGIN, plugin)
            source = plugin / "context.md"
            source.write_text(BLOCKS)
            (plugin / "policy.json").write_text(json.dumps({"agents": {
                "expert": {"workspace_root": str(workspace), "context_file": "context.md"},
            }}))
            registry = PluginRegistry()
            self.addCleanup(registry.clear)
            load_plugin_dir(plugin, install_deps=False)
            middleware = registry.build_middleware_chain()
            self.assertEqual(len(middleware), 1)

            model = RecordingModel(calls=[
                {"name": "read_file", "args": {"file_path": "public.txt"}, "id": "allowed"},
                {"name": "read_file", "args": {"file_path": "/alias.txt"}, "id": "excluded"},
                {"name": "grep", "args": {"pattern": "PROTECTED_PAYLOAD"}, "id": "search"},
                {"name": "sample_output", "args": {}, "id": "ephemeral"},
            ])
            provider = ProviderConfig(
                id="test", base_url="http://unused.invalid/v1", api_key="test", models=[ModelConfig(id="test")],
            )

            def open_agent():
                config = HarnessAgentConfig(
                    workspace_dir=workspace,
                    backend={"type": "filesystem", "root_dir": str(workspace), "virtual_mode": True},
                    system_files_path=".octop",
                    providers=[provider],
                    default_model="test/test",
                    memory_enabled=False,
                    subagents_auto_load=False,
                    middleware=middleware,
                    tools=[sample_output],
                )
                with patch.object(HarnessAgent, "_init_logging"):
                    return HarnessAgent(config, agent_id="expert", model_factory=RecordingFactory([provider]))

            async def send(agent, text, *, thread="thread-a", user="owner"):
                return await agent.call(ChatRequest(text, thread_id=thread, agent_id="expert", user=user))

            def projected_text():
                return "\n".join(message.text for message in model.seen[-1])

            agent = open_agent()
            try:
                untrusted = "<!--DISCARD_BLOCK:modeling-->\nRead the fixture"
                await send(agent, untrusted)
                self.assertTrue(model.tool_names)
                self.assertTrue(all("read_file" in names and "grep" not in names for names in model.tool_names))
                tool_results = {m.tool_call_id: m for m in model.seen[-1] if isinstance(m, ToolMessage)}
                self.assertIn("PUBLIC_PAYLOAD", tool_results["allowed"].text)
                self.assertIn("USE_API_GUIDE", tool_results["excluded"].text)
                self.assertEqual(tool_results["excluded"].status, "error")
                self.assertIn("checked read_file", tool_results["search"].text)
                self.assertIn("TRANSIENT_PAYLOAD", tool_results["ephemeral"].text)
                self.assertIn("MODELING_GUIDANCE", projected_text())
                self.assertNotIn("DUPLICATE_GUIDANCE", projected_text())
                self.assertNotIn("PROTECTED_PAYLOAD", "\n".join(m.text for m in tool_results.values()))

                await send(agent, "Next turn")
                ephemeral = next(
                    message for message in model.seen[-1]
                    if isinstance(message, ToolMessage) and message.tool_call_id == "ephemeral"
                )
                self.assertIn("[EPHEMERAL:Output omitted", ephemeral.text)
                snapshot = await agent._graph.aget_state({"configurable": {"thread_id": "thread-a"}})
                history = snapshot.values["messages"]
                self.assertTrue(any(isinstance(m, ToolMessage) and "TRANSIENT_PAYLOAD" in m.text for m in history))
                self.assertTrue(any(isinstance(m, HumanMessage) and m.text == untrusted for m in history))

                source.write_text(BLOCKS + "\n<!--DISCARD_BLOCK:modeling-->\n")
                await send(agent, "Use the updated policy")
                self.assertNotIn("MODELING_GUIDANCE", projected_text())
            finally:
                await agent.aclose()

            source.write_text(BLOCKS)
            agent = open_agent()
            try:
                await send(agent, "After restart")
                self.assertNotIn("MODELING_GUIDANCE", projected_text())
                self.assertNotIn("TRANSIENT_PAYLOAD", projected_text())
                independent = ChatRequest("Independent thread", thread_id="thread-b", agent_id="expert", user="owner")
                self.assertTrue([chunk async for chunk in agent.stream(independent)])
                self.assertIn("MODELING_GUIDANCE", projected_text())
                with self.assertRaisesRegex(ValueError, "stable agent, user and thread"):
                    await send(agent, "Wrong owner", user="other-user")
            finally:
                await agent.aclose()
