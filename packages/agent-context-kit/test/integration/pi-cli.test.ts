import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

test("native Pi CLI uses guarded tools and fresh context through a real local provider", (t) => {
	const base = mkdtempSync(join(tmpdir(),"pi-native-cli-"));
	const root = join(base,"project");
	mkdirSync(root);
	t.after(() => rmSync(base,{recursive:true,force:true}));
	for(const name of ["generated","src","agent",".pi/extensions"]) mkdirSync(join(root,name),{recursive:true});
	writeFileSync(join(root,"generated/.agent-no-read.md"),"Use Assist and editable application source.");
	writeFileSync(join(root,"generated/private.rs"),"NATIVE_CLI_PRIVATE_SENTINEL");
	writeFileSync(join(root,"AGENTS.md"),"PERMITTED_CLI_PROJECT_GUIDE");
	writeFileSync(join(root,"SYSTEM.md"),"NATIVE_CLI_SYSTEM_SENTINEL");
	writeFileSync(join(root,"APPEND_SYSTEM.md"),"NATIVE_CLI_APPEND_SENTINEL");
	writeFileSync(join(root,"program"),Buffer.from("\x7fELF\0PRIVATE_BINARY_SENTINEL"));
	writeFileSync(join(root,"large.log"),"x".repeat(11*1024*1024));
	writeFileSync(join(root,".pi/extensions/unsafe.ts"),"throw new Error('UNSAFE_EXTENSION_LOADED');");
	const sdk = import.meta.resolve("@earendil-works/pi-coding-agent");
	const ai = import.meta.resolve("@earendil-works/pi-ai/providers/faux");
	const main = new URL("main.js",sdk).href;
	const entry = new URL("../../src/adapters/pi-cli.ts",import.meta.url).href;
	const runner = join(base,"runner.mjs");
	writeFileSync(runner, `
import assert from 'node:assert/strict';
import {main} from ${JSON.stringify(main)};
import {fauxProvider,fauxAssistantMessage,fauxToolCall} from ${JSON.stringify(ai)};
import {createPiContextCliExtension,preparePiContextCliArgs} from ${JSON.stringify(entry)};
const faux=fauxProvider({provider:'native-cli-policy-test',models:[{id:'fixture',name:'Fixture'}],tokensPerSecond:1000000,tokenSize:{min:1000,max:1000}});
const calls=[['read',{path:'generated/private.rs'}],['read',{path:'generated/other.rs'}],['read',{path:'program'}],['read',{path:'program',offset:2}],['read',{path:'large.log'}],['read',{path:'missing.log'}],['grep',{path:'.',pattern:'needle'}],['write',{path:'src/main.rs',content:'value = 1;'}],['edit',{path:'src/main.rs',edits:[{oldText:'1',newText:'2'}]}],['write',{path:'generated/new.rs',content:'blocked'}],['host_capability',{}],['bash',{command:'cat generated/private.rs'}]];
let requests=0;
let blockedResults=0;
const check=context=>{requests++;const text=JSON.stringify(context);assert.doesNotMatch(text,/NATIVE_CLI_PRIVATE_SENTINEL|NATIVE_CLI_SYSTEM_SENTINEL|NATIVE_CLI_APPEND_SENTINEL|PRIVATE_BINARY_SENTINEL/);assert.match(text,/PERMITTED_CLI_PROJECT_GUIDE/);const last=context.messages.findLast(message=>message.role==='toolResult');if(last?.toolName==='read'){const data=JSON.parse(last.content[0].text);assert.equal(last.isError,true);assert.equal(data.blocked,true);assert.equal(data.retryable,false);if(data.status==='excluded'){blockedResults++;assert.equal(data.attemptsForScope,blockedResults);if(blockedResults===2){assert.equal(data.previouslyBlocked,true);assert.equal(data.guidance,undefined);assert.match(text,/host_policy/);}}else assert.ok(['UNSUPPORTED_BINARY','FILE_TOO_LARGE','FILE_NOT_FOUND'].includes(data.code));}if(last?.toolName==='grep')assert.equal(last.isError,false);};
faux.setResponses([...calls.map(([name,args],index)=>context=>{check(context);return fauxAssistantMessage(fauxToolCall(name,args,{id:'native-'+index}),{stopReason:'toolUse'});}),context=>{check(context);return fauxAssistantMessage('Native CLI protection verified.',{stopReason:'stop'});}]);
const args=preparePiContextCliArgs(['--offline','--provider','native-cli-policy-test','--model','fixture','--no-session','--print','Inspect project'],{fileArgs:[]});
const capability={name:'host_capability',label:'Host capability',parameters:{type:'object',properties:{},additionalProperties:false},description:'Fixed host capability.',execute:async()=>({content:[{type:'text',text:'HOST_CAPABILITY_WORKED'}]})};
await main(args,{extensionFactories:[pi=>pi.registerProvider(faux.provider),createPiContextCliExtension([capability])]});
assert.equal(requests,13);
assert.equal(blockedResults,2);
`);
	const run=spawnSync(process.execPath,["--experimental-strip-types",runner],{
		cwd:root,encoding:"utf8",timeout:30000,maxBuffer:128*1024,
		env:{...process.env,PI_CODING_AGENT_DIR:join(root,"agent"),PI_OFFLINE:"1",PI_SKIP_VERSION_CHECK:"1",NO_COLOR:"1"},
	});
	assert.equal(run.status,0,`${run.stderr}\n${run.stdout}`);
	assert.doesNotMatch(run.stdout+run.stderr,/NATIVE_CLI_PRIVATE_SENTINEL|UNSAFE_EXTENSION_LOADED/);
	assert.match(run.stdout,/Native CLI protection verified/);
	assert.equal(readFileSync(join(root,"src/main.rs"),"utf8"),"value = 2;");
	assert.equal(readFileSync(join(root,"generated/private.rs"),"utf8"),"NATIVE_CLI_PRIVATE_SENTINEL");
});

test("native Pi print continues after premature stop, verifies edits and rechecks a localized repair", (t) => {
 const base=mkdtempSync(join(tmpdir(),"pi-completion-cli-")); const root=join(base,"project"); mkdirSync(root); mkdirSync(join(root,"src"));
 t.after(()=>rmSync(base,{recursive:true,force:true})); writeFileSync(join(root,"src/main.rs"),"value = 1;");
 const sdk=import.meta.resolve("@earendil-works/pi-coding-agent"); const main=new URL("main.js",sdk).href;
 const ai=import.meta.resolve("@earendil-works/pi-ai/providers/faux"); const entry=new URL("../../src/adapters/pi-cli.ts",import.meta.url).href;
 const runner=join(base,"runner.mjs");
 writeFileSync(runner,`
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {main} from ${JSON.stringify(main)};
import {fauxProvider,fauxAssistantMessage,fauxToolCall} from ${JSON.stringify(ai)};
import {createPiContextCliExtension,preparePiContextCliArgs} from ${JSON.stringify(entry)};
const faux=fauxProvider({provider:'completion-test',models:[{id:'fixture',name:'Fixture'}],tokensPerSecond:1000000,tokenSize:{min:1000,max:1000}});
const calls=[];let requests=0;
const edit=value=>fauxAssistantMessage(fauxToolCall('edit',{path:'src/main.rs',edits:[{oldText:'value = '+(value-1),newText:'value = '+value}]},{id:'edit-'+value}),{stopReason:'toolUse'});
faux.setResponses([
 ()=>{requests++;return edit(2);},
 ()=>{requests++;return fauxAssistantMessage('I will verify the edit now.',{stopReason:'stop'});},
 context=>{requests++;assert.match(JSON.stringify(context),/host_completion_check/);assert.match(JSON.stringify(context),/E0308/);return edit(3);},
 ()=>{requests++;return fauxAssistantMessage('The repair is done. I will run tests.',{stopReason:'stop'});},
 context=>{requests++;assert.match(JSON.stringify(context),/host_completion_check/);assert.deepEqual(calls,['app_build','app_test','app_build','app_test']);return fauxAssistantMessage('Verified after repair. Zero tests executed.',{stopReason:'stop'});}
]);
const checks=['app_build','app_test'].map(name=>({name,label:name,description:'Fixed verification',parameters:{type:'object',properties:{},additionalProperties:false},execute:async()=>{calls.push(name);if(name==='app_build'&&readFileSync('src/main.rs','utf8').includes('2'))throw new Error('{"status":"failed","diagnostics":[{"code":"E0308"}]}');return {content:[{type:'text',text:'{"status":"passed","tests":{"passed":0,"failed":0,"skipped":0}}'}],details:{status:'passed'}};}}));
await main(preparePiContextCliArgs(['--offline','--provider','completion-test','--model','fixture','--no-session','--print','Edit and verify'],{fileArgs:[]}),{extensionFactories:[pi=>pi.registerProvider(faux.provider),createPiContextCliExtension(checks)]});
assert.equal(requests,5); assert.equal(readFileSync('src/main.rs','utf8'),'value = 3;');
`);
 const run=spawnSync(process.execPath,["--experimental-strip-types",runner],{cwd:root,encoding:"utf8",timeout:30000,maxBuffer:256*1024,env:{...process.env,PI_CODING_AGENT_DIR:join(base,"agent"),PI_OFFLINE:"1",PI_SKIP_VERSION_CHECK:"1",NO_COLOR:"1"}});
 assert.equal(run.status,0,`${run.stderr}\n${run.stdout}`); assert.match(run.stdout,/Verified after repair/);
});

test("native Pi resumes an old stuck session, rebuilds request context and keeps transcript and policy intact", (t) => {
 const base=mkdtempSync(join(tmpdir(),"pi-stale-session-")),root=join(base,"project");mkdirSync(root);mkdirSync(join(root,"generated"));
 t.after(()=>rmSync(base,{recursive:true,force:true}));writeFileSync(join(root,"AGENTS.md"),"FRESH_POLICY_GUIDE");writeFileSync(join(root,"model.xml"),"CURRENT_MODEL_FACTS");writeFileSync(join(root,"generated/.agent-no-read.md"),"Use Assist.");writeFileSync(join(root,"generated/private.rs"),"RECOVERY_PRIVATE_SENTINEL");
 const sdk=import.meta.resolve("@earendil-works/pi-coding-agent"),main=new URL("main.js",sdk).href,ai=import.meta.resolve("@earendil-works/pi-ai/providers/faux"),entry=new URL("../../src/adapters/pi-cli.ts",import.meta.url).href;
 const runner=join(base,"runner.mjs");writeFileSync(runner,`
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {SessionManager} from ${JSON.stringify(sdk)};
import {main} from ${JSON.stringify(main)};
import {fauxProvider,fauxAssistantMessage,fauxToolCall} from ${JSON.stringify(ai)};
import {createPiContextCliExtension,preparePiContextCliArgs} from ${JSON.stringify(entry)};
const promise='Let me read the obsolete compiler errors and inspect the student source before repairing the unavailable query methods.';
const manager=SessionManager.create(process.cwd(),${JSON.stringify(join(base,"sessions"))});
for(let i=0;i<3;i++){manager.appendMessage({role:'user',content:'Old continuation '+i,timestamp:Date.now()+i*2});manager.appendMessage({...fauxAssistantMessage(promise,{stopReason:'stop'}),timestamp:Date.now()+i*2+1});}
const path=manager.getSessionFile();const original=readFileSync(path,'utf8');
const faux=fauxProvider({provider:'stale-session-test',models:[{id:'fixture',name:'Fixture'}],tokensPerSecond:1000000,tokenSize:{min:1000,max:1000}});let requests=0;
const check=context=>{requests++;const text=JSON.stringify(context);assert.match(text,/CURRENT_SCENARIO_TASK/);assert.match(text,/FRESH_POLICY_GUIDE/);assert.match(text,/CONTEXT_RECOVERED/);assert.doesNotMatch(text,/Let me read the obsolete compiler errors|RECOVERY_PRIVATE_SENTINEL/);};
faux.setResponses([
 context=>{check(context);return fauxAssistantMessage(fauxToolCall('read',{path:'generated/private.rs'},{id:'denial'}),{stopReason:'toolUse'});},
 context=>{check(context);const last=context.messages.findLast(m=>m.role==='toolResult');assert.equal(last.isError,true);return fauxAssistantMessage(fauxToolCall('read',{path:'model.xml'},{id:'facts'}),{stopReason:'toolUse'});},
 context=>{check(context);assert.match(JSON.stringify(context),/CURRENT_MODEL_FACTS/);return fauxAssistantMessage('Recovered the current model analysis.',{stopReason:'stop'});}
]);
await main(preparePiContextCliArgs(['--offline','--provider','stale-session-test','--model','fixture','--session',path,'--print','CURRENT_SCENARIO_TASK: read the model and identify use cases'],{fileArgs:[]}),{extensionFactories:[pi=>pi.registerProvider(faux.provider),createPiContextCliExtension()]});
assert.equal(requests,3);const saved=readFileSync(path,'utf8');assert.ok(saved.startsWith(original));assert.match(saved,/Let me read the obsolete compiler errors/);assert.match(saved,/agent-context-kit-progress-recovery-v1/);
`);
 const run=spawnSync(process.execPath,["--experimental-strip-types",runner],{cwd:root,encoding:"utf8",timeout:30000,maxBuffer:256*1024,env:{...process.env,PI_CODING_AGENT_DIR:join(base,"agent"),PI_OFFLINE:"1",PI_SKIP_VERSION_CHECK:"1",NO_COLOR:"1"}});
 assert.equal(run.status,0,`${run.stderr}\n${run.stdout}`);assert.match(run.stdout,/Recovered the current model analysis/);
});
