"""Octop hook plugin for request-local context and controlled native file reads."""

import asyncio
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import json
import logging
import os
from pathlib import Path
import re
from typing import Annotated, Any, NotRequired, TypedDict

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import AgentState, OmitFromInput
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage
from langgraph.config import get_config

from .policy import OUTSIDE, read_denial


logger = logging.getLogger(__name__)
START = re.compile(r"<!--BLOCK_ID:([a-z0-9_-]+)-->")
END = re.compile(r"<!--/BLOCK_ID:([a-z0-9_-]+)-->")
DISCARD = re.compile(r"<!--DISCARD_BLOCK:([a-z0-9_-]+)-->")
EPHEMERAL = re.compile(r"(?:\A|[\r\n])<!--ephemeral-->(?=\Z|[\r\n])")
UNCHECKED_READS = frozenset({"ls", "glob", "grep", "read_image", "read_video"})
SOURCE_LIMIT = 65536
STATE = "teaql_octop_context_v1"


@dataclass(frozen=True)
class AgentPolicy:
    root: Path
    source: Path | None


class Lifecycle(TypedDict):
    owner: list[str]
    revision: str
    sequence: int
    blocks: dict[str, str]
    discarded: list[str]


class ContextState(AgentState[Any]):
    teaql_octop_context_v1: NotRequired[Annotated[Lifecycle, OmitFromInput]]


def _declarations(markdown: str) -> tuple[dict[str, str], list[str]]:
    lines = re.findall(r"[^\r\n]*(?:\r\n|\r|\n|$)", markdown)
    tags = [line.rstrip("\r\n") for line in lines]
    counts = Counter(m[1] for line in tags if (m := START.fullmatch(line)))
    blocks: dict[str, str] = {}
    discards: list[str] = []
    open_id = None
    body_start = 0
    invalid = False
    for index, line in enumerate(tags):
        if match := START.fullmatch(line):
            if open_id is not None:
                invalid = True
            else:
                open_id = match[1]
                body_start = index + 1
                invalid = counts[open_id] > 1
        elif open_id is not None and (match := END.fullmatch(line)):
            if match[1] != open_id:
                invalid = True
                continue
            if not invalid:
                blocks[open_id] = "".join(lines[body_start:index])
            open_id = None
        elif match := DISCARD.fullmatch(line):
            discards.append(match[1])
    return blocks, discards


def _policy_map(directory: Path) -> dict[str, AgentPolicy]:
    try:
        raw = json.loads((directory / "policy.json").read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    agents = raw.get("agents") if isinstance(raw, dict) else None
    if not isinstance(agents, dict):
        raise ValueError("Octop context policy requires an agents object")
    if agents and os.name != "posix":
        raise ValueError("Octop context policy currently supports POSIX local filesystems")
    policies = {}
    for agent_id, entry in agents.items():
        if not agent_id or not isinstance(entry, dict) or not isinstance(entry.get("workspace_root"), str):
            raise ValueError("Each Octop context policy requires an agent ID and workspace_root")
        root = Path(entry["workspace_root"])
        if not root.is_absolute() or root != root.resolve(strict=True) or not root.is_dir() or root == root.parent:
            raise ValueError(f"workspace_root for {agent_id!r} must be a canonical local workspace directory")
        if directory.is_relative_to(root):
            raise ValueError("The installed plugin must be outside every configured agent workspace")
        filename = entry.get("context_file")
        source = None
        if filename is not None:
            if not isinstance(filename, str) or Path(filename).name != filename or not filename.endswith(".md"):
                raise ValueError("context_file must be a Markdown filename in the installed plugin directory")
            source = directory / filename
            if source.resolve(strict=True) != source or not source.is_file():
                raise ValueError("context_file must be an administrator-owned file outside the agent workspace")
        policies[agent_id] = AgentPolicy(root, source)
    return policies


def _scope() -> tuple[str, str, str]:
    config = get_config().get("configurable", {})
    return str(config.get("agent_id") or ""), str(config.get("user") or ""), str(config.get("thread_id") or "")


def _audit(scope, sequence, action, source, detail):
    logger.info("context action=%s scope=%r request=%d source=%s detail=%r", action, scope, sequence, source, detail)


def _read_source(path: Path) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(SOURCE_LIMIT + 1)
    if len(data) > SOURCE_LIMIT:
        raise ValueError("Octop lifecycle source exceeds 64 KiB")
    return data


def _message_text(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(
        part if isinstance(part, str) else part["text"]
        for part in content
        if isinstance(part, str) or (
            isinstance(part, dict) and part.get("type") == "text" and isinstance(part.get("text"), str)
        )
    )


def _render_blocks(state: Lifecycle) -> str:
    discarded = set(state["discarded"])
    blocks = []
    for block_id, body in state["blocks"].items():
        if block_id not in discarded:
            separator = "" if body.endswith("\n") else "\n"
            blocks.append(f"<!--BLOCK_ID:{block_id}-->\n{body}{separator}<!--/BLOCK_ID:{block_id}-->")
    return "\n\n".join(blocks)


class OctopContextMiddleware(AgentMiddleware):
    state_schema = ContextState

    def __init__(self, policies: dict[str, AgentPolicy]):
        self.policies = policies

    def before_model(self, state, runtime):
        scope = _scope()
        policy = self.policies.get(scope[0])
        if policy is None:
            return None
        previous = state.get(STATE, {})
        if not scope[2] or (previous and previous["owner"] != list(scope)):
            raise ValueError("Octop context policy requires a stable agent, user and thread scope")
        sequence = previous.get("sequence", 0) + 1
        blocks = dict(previous.get("blocks", {}))
        discarded = set(previous.get("discarded", []))
        revision = previous.get("revision", "")
        if policy.source is not None:
            data = _read_source(policy.source)
            digest = sha256(data).hexdigest()
            if digest != revision:
                definitions, discards = _declarations(data.decode("utf-8"))
                for block_id, body in definitions.items():
                    if block_id not in blocks:
                        blocks[block_id] = body
                        _audit(scope, sequence, "block_activated", policy.source.name, block_id)
                    elif blocks[block_id] != body:
                        _audit(scope, sequence, "block_id_conflict", policy.source.name, block_id)
                for block_id in discards:
                    if block_id not in blocks:
                        action = "discard_unknown"
                    elif block_id in discarded:
                        action = "discard_already_applied"
                    else:
                        action = "block_discarded"
                        discarded.add(block_id)
                    _audit(scope, sequence, action, policy.source.name, block_id)
                revision = digest
        return {
            STATE: {
                "owner": list(scope),
                "sequence": sequence,
                "revision": revision,
                "blocks": blocks,
                "discarded": sorted(discarded),
            },
        }

    async def abefore_model(self, state, runtime):
        return await asyncio.to_thread(self.before_model, state, runtime)

    def _project(self, request):
        scope = _scope()
        if scope[0] not in self.policies:
            return request
        state = request.state[STATE]
        messages = list(request.messages)
        latest_ai = next((i for i in range(len(messages) - 1, -1, -1) if isinstance(messages[i], AIMessage)), -1)
        for index, message in enumerate(messages):
            content = message.content
            body = _message_text(content)
            if "<!--DISCARD_BLOCK:" in body:
                for line in re.split(r"\r\n|\r|\n", body):
                    if match := DISCARD.fullmatch(line):
                        _audit(scope, state["sequence"], "discard_denied", message.type, match[1])
            if index < latest_ai and EPHEMERAL.search(body):
                serialized = content
                if not isinstance(content, str):
                    serialized = json.dumps(content, ensure_ascii=False, separators=(",", ":"))
                size = len(serialized.encode("utf-8"))
                stub = f"[EPHEMERAL:Output omitted after consumption;original_bytes={size}]"
                projected = stub if isinstance(content, str) else [{"type": "text", "text": stub}]
                messages[index] = message.model_copy(update={"content": projected})
                _audit(scope, state["sequence"], "ephemeral_consumed", message.type, size)
        active = _render_blocks(state)
        changes = {
            "messages": messages,
            "tools": [tool for tool in request.tools if getattr(tool, "name", None) not in UNCHECKED_READS],
        }
        if active:
            section = f"\n\n<agent_context_lifecycle_blocks>\n{active}\n</agent_context_lifecycle_blocks>"
            system = request.system_message
            if system is None:
                system = SystemMessage(content=section.lstrip())
            else:
                content = system.content
                merged = content + section if isinstance(content, str) else [
                    *content, {"type": "text", "text": section},
                ]
                system = system.model_copy(update={"content": merged})
            changes["system_message"] = system
        return request.override(**changes)

    def wrap_model_call(self, request, handler):
        return handler(self._project(request))

    async def awrap_model_call(self, request, handler):
        return await handler(self._project(request))

    def _prepare_tool(self, request):
        policy = self.policies.get(_scope()[0])
        if policy is None:
            return request
        call = request.tool_call
        name = call["name"]
        if name in UNCHECKED_READS:
            reason = "This context profile uses checked read_file with a known workspace path."
        elif name == "read_file":
            args = call["args"]
            raw_path = args.get("file_path")
            reason = OUTSIDE
            if isinstance(raw_path, str) and raw_path:
                host_path = policy.root / raw_path.lstrip("/")
                reason = read_denial(policy.root, str(host_path))
                if reason is None:
                    virtual_path = "/" + host_path.relative_to(policy.root).as_posix()
                    return request.override(tool_call={**call, "args": {**args, "file_path": virtual_path}})
        else:
            return request
        return ToolMessage(content=reason, name=name, tool_call_id=call["id"], status="error")

    def wrap_tool_call(self, request, handler):
        prepared = self._prepare_tool(request)
        return prepared if isinstance(prepared, ToolMessage) else handler(prepared)

    async def awrap_tool_call(self, request, handler):
        prepared = await asyncio.to_thread(self._prepare_tool, request)
        return prepared if isinstance(prepared, ToolMessage) else await handler(prepared)


def setup(ctx):
    policies = _policy_map(ctx.source_path.resolve())
    if policies:
        ctx.middleware(OctopContextMiddleware(policies))
