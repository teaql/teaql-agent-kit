import { randomUUID } from "node:crypto";
import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

const RECOVERY = "agent-context-kit-progress-recovery-v1";
const BLOCKER = "agent-context-kit-progress-blocker-v1";
const KEEP = new Set(["agent-context-kit-active-v1", "agent-context-kit-policy-denials-v1"]);
interface Message { role: string; content?: unknown; stopReason?: unknown; customType?: string; details?: unknown }
function text(message: Message): string {
 if (typeof message.content === "string") return message.content;
 return Array.isArray(message.content) ? message.content.filter(p => p?.type === "text").map(p => p.text).join("\n") : "";
}
const PROMISE = /\b(?:let me|i (?:will|shall|need to))\s+(?:(?:first|now|directly|re-?)\s*)?(?:read|check|inspect|run|build|test|fix|edit|review|look)|让我(?:再|重新|先|直接|继续|一下)*\s*(?:读|看|查|检查|查看|修复|运行|执行|验证|审视)/i;
function grams(value: string): Set<string> {
 const s=value.toLowerCase().replace(/[^\p{L}\p{N}]/gu, "").slice(0, 8000);
 return new Set(Array.from({length:Math.max(0,s.length-2)},(_,i)=>s.slice(i,i+3)));
}
function similar(a: string, b: string): boolean {
 const x=grams(a), y=grams(b); let overlap=0;
 for(const g of x)if(y.has(g))overlap++;
 return x.size+y.size>0 && 2*overlap/(x.size+y.size)>=0.55;
}
/** Three similar progress promises after the last tool boundary; factual repeated answers are not stalls. */
export function hasPiReplyLoop(messages: readonly Message[]): boolean {
 const replies: string[]=[];
 for(const m of messages.slice(-48)) {
  if(m.role==="toolResult" || (m.role==="assistant" && Array.isArray(m.content) && m.content.some(p=>p?.type==="toolCall")))replies.length=0;
  else if(m.role==="assistant" && m.stopReason==="stop")replies.push(text(m));
 }
 const last=replies[replies.length-1];
 return !!last && last.length>=8 && PROMISE.test(last) && !/MISSING_ASSIST|LARGE_REWRITE_REQUEST|VERIFICATION_INCOMPLETE|STALLED_NO_TOOL_PROGRESS/.test(last) && replies.slice(0,-1).filter(v=>PROMISE.test(v)&&similar(last,v)).length>=2;
}
function recoveryID(message: Message): string | undefined {
 if(message.role!=="custom" || message.customType!==RECOVERY || !message.details || typeof message.details!=="object")return;
 const value=(message.details as {recoveryID?:unknown}).recoveryID;
 return typeof value==="string"?value:undefined;
}
function branchMessages(ctx: ExtensionContext): Message[] {
 const messages: Message[]=[];
 for(const entry of ctx.sessionManager.getBranch()) {
  if(entry.type==="message")messages.push(entry.message);
  else if(entry.type==="custom_message")messages.push({role:"custom",content:entry.content,customType:entry.customType,details:entry.details});
 }
 return messages;
}
export function registerPiProgressRecovery(pi: ExtensionAPI): void {
 let anchor: string | undefined, recoveries=0;
 const restore=(_event: unknown,ctx: ExtensionContext)=>{
  anchor=undefined;recoveries=0;
  for(const message of branchMessages(ctx)){const id=recoveryID(message);if(id)anchor=id;}
 };
 const afterAnchor=(messages: readonly Message[])=>{
  const index=anchor?messages.map(recoveryID).lastIndexOf(anchor):-1;
  return index>=0?messages.slice(index+1):messages;
 };
 const report=()=>{
  anchor=randomUUID();recoveries++;
  return {customType:RECOVERY,display:true,details:{recoveryID:anchor},content:JSON.stringify({status:"CONTEXT_RECOVERED",source:"host_progress_guard",message:"Repeated progress-only replies without tool calls were detected. The original transcript is preserved. This request view keeps system/tool instructions, active host policy, all preceding user instructions and messages after this recovery marker. Focus on the current user task; old compiler errors and previous promises are not current evidence. Re-read permitted files or request current Assist when facts are needed. Actually invoke registered tools when the task requires them; otherwise answer the current question directly. Respect all access and mutation restrictions. If blocked, report the concrete blocker. Do not repeat a promise to act."})};
 };
 pi.on("session_start",restore);pi.on("session_tree",restore);
 pi.on("before_agent_start",(event,ctx)=>{
  if(event.messageType!=="user")return;
  recoveries=0;
  if(hasPiReplyLoop(afterAnchor(branchMessages(ctx))))return {message:report()};
 });
 pi.on("turn_end",(event,ctx)=>{
  if(event.continue || event.outcome!=="completed" || ctx.signal?.aborted || event.message.role!=="assistant" || event.message.stopReason!=="stop")return;
  const recent=afterAnchor(branchMessages(ctx));
  const relapse=recoveries>=1 && !recent.some(m=>m.role==="toolResult" || (m.role==="assistant" && Array.isArray(m.content) && m.content.some(p=>p?.type==="toolCall"))) && PROMISE.test(text(event.message)) && !/MISSING_ASSIST|LARGE_REWRITE_REQUEST|VERIFICATION_INCOMPLETE/.test(text(event.message));
  if(!hasPiReplyLoop(recent) && !relapse)return;
  if(recoveries>=1)return {entries:[...event.entries,{type:"custom_message" as const,customType:BLOCKER,display:true,content:JSON.stringify({status:"STALLED_NO_TOOL_PROGRESS",message:"Reply repetition continued after one automatic context recovery. Stop automatic retries and report the unresolved task; no completion has been established."})}]};
  return {entries:[...event.entries,{type:"custom_message" as const,...report()}],continue:true};
 });
 pi.on("context_with_system",event=>{
  if(!anchor)return;
  const index=event.messages.map(recoveryID).lastIndexOf(anchor);
  if(index<0)return;
  const earlier=event.messages.slice(0,index);
  const retained=earlier.filter(m=>m.role==="system" || (m.role==="custom" && KEEP.has(m.customType)));
  const users=earlier.filter(m=>m.role==="user");
  return {messages:[...retained,...users,...event.messages.slice(index)]};
 });
}
