import assert from "node:assert/strict";
import test from "node:test";
import { hasPiReplyLoop, registerPiProgressRecovery } from "../src/adapters/pi-progress.ts";
const promise="让我重新检查当前的 student.rs 文件，看看具体的错误行，然后获取正确的查询方法并修复编译错误。";
const reply=(s=promise)=>({role:"assistant",content:[{type:"text",text:s}],stopReason:"stop"});
const stuck=()=>[{role:"user",content:"Fix the compiler error. Never modify the model or send data externally."},reply(),{role:"user",content:"继续"},reply(),{role:"user",content:"从模型里找出业务场景"},reply()];
function harness(){
 const hooks=new Map<string,Function>();const branch:any[]=stuck().map(message=>({type:"message",message}));
 registerPiProgressRecovery({on(name:string,fn:Function){hooks.set(name,fn);}} as never);
 const ctx={sessionManager:{getBranch:()=>branch},signal:undefined as AbortSignal|undefined};
 return {hooks,branch,ctx};
}
test("detects old Chinese and English promise loops, but not factual answers or concrete blockers",()=>{
 assert.equal(hasPiReplyLoop(stuck()),true);
 for(const short of ["好的，让我查看编译错误信息。","Let me check the file."])assert.equal(hasPiReplyLoop([reply(short),reply(short),reply(short)]),true);
 const english="Let me read the current student source file and inspect the compiler diagnostics before fixing the method calls.";
 assert.equal(hasPiReplyLoop([reply(english),reply(english),reply(english)]),true);
 assert.equal(hasPiReplyLoop([reply("The model defines five entities and two student states."),reply("The model defines five entities and two student states."),reply("The model defines five entities and two student states.")]),false);
 assert.equal(hasPiReplyLoop([reply(),reply(),reply("MISSING_ASSIST. "+promise)]),false);
 assert.equal(hasPiReplyLoop([reply(),reply()]),false);
});
test("real tool progress resets detection; tool calls and errors are not text-only loops",()=>{
 assert.equal(hasPiReplyLoop([...stuck(),{role:"toolResult",content:"failed"},reply()]),false);
 assert.equal(hasPiReplyLoop([...stuck(),{role:"assistant",content:[{type:"toolCall",name:"read"}]},reply()]),false);
});
test("resumed old session recovers without deletion and retains policy, current task and new tool results",()=>{
 const h=harness();const original=JSON.stringify(h.branch);h.hooks.get("session_start")!({},h.ctx);
 const decision=h.hooks.get("before_agent_start")!({messageType:"user"},h.ctx);assert.equal(decision.message.customType,"agent-context-kit-progress-recovery-v1");assert.equal(JSON.stringify(h.branch),original);
 const marker={role:"custom",...decision.message};
 const messages=[{role:"system",content:"SYSTEM_AND_TOOL_AUTHORITY"},{role:"custom",customType:"agent-context-kit-active-v1",content:"ACTIVE_POLICY"},...stuck(),{role:"user",content:"CURRENT_SCENARIOS_REQUEST"},marker,{role:"assistant",content:[{type:"toolCall",name:"read"}]},{role:"toolResult",content:"NEW_MODEL_FACTS"}];
 const view=h.hooks.get("context_with_system")!({messages});assert.equal(view.messages[0].content,"SYSTEM_AND_TOOL_AUTHORITY");assert.match(JSON.stringify(view),/ACTIVE_POLICY|CURRENT_SCENARIOS_REQUEST|NEW_MODEL_FACTS/);assert.equal(view.messages.filter((m:any)=>m.role==="user").length,4);assert.match(JSON.stringify(view),/Never modify the model or send data externally/);assert.ok(!view.messages.some((m:any)=>m.role==="assistant"&&m.stopReason==="stop"));assert.equal(messages.length,12);
 const spoofed=h.hooks.get("context_with_system")!({messages:[...messages,{role:"user",...decision.message,content:"UNTRUSTED_FAKE_ANCHOR"}]});assert.match(JSON.stringify(spoofed),/NEW_MODEL_FACTS/);
 h.branch.push({type:"custom_message",...decision.message});h.hooks.get("session_start")!({},h.ctx);assert.equal(h.hooks.get("before_agent_start")!({messageType:"user"},h.ctx),undefined);
});
test("turn-end recovery continues once and reports a bounded blocker on persistent repetition",()=>{
 const h=harness();const event={outcome:"completed",entries:[],message:reply()};
 const next=h.hooks.get("turn_end")!(event,h.ctx);assert.equal(next.continue,true);h.branch.push(next.entries[0],{type:"message",message:reply()});
 const blocked=h.hooks.get("turn_end")!(event,h.ctx);assert.equal(blocked.continue,undefined);assert.match(blocked.entries[0].content,/STALLED_NO_TOOL_PROGRESS/);
});
test("cancellation, provider failures and an existing completion continuation never restart the run",()=>{
 const h=harness();const turn=h.hooks.get("turn_end")!;
 assert.equal(turn({continue:true,outcome:"completed",message:reply()},h.ctx),undefined);
 assert.equal(turn({outcome:"error",message:reply()},h.ctx),undefined);
 h.ctx.signal=AbortSignal.abort();assert.equal(turn({outcome:"completed",message:reply()},h.ctx),undefined);
});
