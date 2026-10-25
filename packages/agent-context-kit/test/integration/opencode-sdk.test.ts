import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { Effect } from "effect";
import { Message } from "@opencode/ai";
import { fromPromise } from "@opencode/plugin/promise/adapter";
import { createOpenCodeContextPolicyPlugin } from "../../src/adapters/opencode-context.ts";

test("published OpenCode SDK executes strict plugin registration, controlled IO and rejection through its real Promise/Effect bridge", async (t) => {
	const root = mkdtempSync(join(tmpdir(), "opencode-sdk-policy-"));
	t.after(() => rmSync(root, { recursive: true, force: true }));
	mkdirSync(join(root, "src")); mkdirSync(join(root, "generated"));
	writeFileSync(join(root, "generated/.agent-no-read.md"), "Use permitted docs.");
	writeFileSync(join(root, "generated/private.ts"), "SDK_SENTINEL_DO_NOT_RETURN");
	const tools = new Map<string, { execute(input: unknown, context: unknown): Effect.Effect<{ content: string }, unknown> }>();
	const hooks = new Map<string, (input: any) => Effect.Effect<any, any>>();
	const registration = { dispose: Effect.void };
	const hook = (domain: string) => (name: string, callback: any) => Effect.sync(() => { hooks.set(`${domain}:${name}`, callback); return registration; });
	// Unused host APIs are present for the real bridge to wrap, but fail if invoked.
	const unused: any = new Proxy(() => { throw new Error("Unexpected host API call"); }, { get: () => unused });
	const host = new Proxy({
		location: { directory: root },
		tool: {
			hook: hook("tool"),
			transform: (callback: any) => Effect.sync(() => {
				callback({ list: () => [], get: () => undefined, remove: (id: string) => tools.delete(id),
					add: (tool: any) => tools.set(tool.name, tool), update: unused, namespace: unused });
				return registration;
			}),
		},
		session: new Proxy({ hook: hook("session") }, { get: (target, key) => key === "hook" ? target.hook : unused }),
		shell: { hook: hook("shell") },
	}, { get: (target, key) => Reflect.get(target, key) ?? unused });
	const plugin = fromPromise(createOpenCodeContextPolicyPlugin({ projectRoot: root, writeRoots: ["src"], readOnlyPaths: ["generated"] }));
	await Effect.runPromise(Effect.scoped(Effect.gen(function* () {
		yield* plugin.effect(host as never);
		for (const tool of tools.values()) assert.deepEqual((tool as any).options, { codemode: false }, "Strict tools must be visible without the disabled native Code Mode executor");
		const context = { progress: () => Effect.void };
		const created = yield* tools.get("context_create")!.execute({ path: "src/app.ts", content: "working" }, context);
		assert.equal(JSON.parse(created.content).status, "ok");
		const read = yield* tools.get("context_read")!.execute({ path: "generated/private.ts" }, context);
		assert.equal(JSON.parse(read.content).status, "excluded");
		assert.doesNotMatch(read.content, /SDK_SENTINEL_DO_NOT_RETURN/);
		const rejected = yield* Effect.result(hooks.get("tool:execute.before")!({ tool: "bash", input: {} }));
		assert.equal(rejected._tag, "Failure");
		const request = { sessionID: "sdk-session", system: [{ type: "text", text: "native auto context" }], messages: [Message.user("inspect")], tools: {} };
		yield* hooks.get("session:context")!(request);
		assert.doesNotMatch(JSON.stringify(request), /native auto context|SDK_SENTINEL_DO_NOT_RETURN/);
		assert.doesNotThrow(() => Message.make(request.messages.at(-1)!));
	})));
});
