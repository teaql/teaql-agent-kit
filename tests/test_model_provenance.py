import contextlib
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/build-teaql-app/scripts/model_provenance.py'
spec = importlib.util.spec_from_file_location('model_provenance', SCRIPT)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sid = str(uuid.uuid4())
        self.env = {'CODEX_HOME': str(self.root), 'CODEX_THREAD_ID': self.sid}
        self.session = self.root / 'sessions/2026/10/27' / ('rollout-time-' + self.sid + '.jsonl')
        self.session.parent.mkdir(parents=True)
        self.meta = {'type': 'session_meta', 'payload': {'id': self.sid, 'cli_version': '0.164.0', 'model_provider': 'openai', 'instructions': 'DO NOT EXPORT ME'}}
        self.turn = {'type': 'turn_context', 'payload': {'turn_id': 'turn-1', 'model': 'actual-model', 'cwd': 'PRIVATE'}}
        self.records(self.meta, self.turn)

    def records(self, *records):
        self.session.write_text(''.join(json.dumps(r) + '\n' for r in records))

    def model(self, name='model.xml', attributes=''):
        path = self.root / name
        path.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<!-- before -->\n<root name="test-service" ' + attributes + '>\n  <!-- preserve -->\n  <node _name="A &amp; B" value="1"/>\n</root>\n')
        return path

    def test_current_session_whitelist(self):
        actor = p.capture(self.env)
        self.assertEqual(actor['actor'], {'agent': 'codex', 'agent_version': '0.164.0', 'llm_provider': 'openai', 'llm_model': 'actual-model'})
        self.assertNotIn('DO NOT EXPORT', json.dumps(actor))
        self.assertNotIn('PRIVATE', json.dumps(actor))

    def test_switch_uses_latest_model_and_provider(self):
        self.records(self.meta, self.turn, {'type': 'turn_context', 'payload': {'turn_id': 'turn-2', 'model': 'new-model', 'model_provider': 'other-provider'}})
        actor = p.capture(self.env)
        self.assertEqual(actor['actor']['llm_model'], 'new-model')
        self.assertEqual(actor['actor']['llm_provider'], 'other-provider')

    def test_missing_latest_model_never_reuses_previous(self):
        self.records(self.meta, self.turn, {'type': 'turn_context', 'payload': {'turn_id': 'turn-2'}})
        self.assertEqual(p.capture(self.env)['actor']['llm_model'], 'unknown')

    def test_wrong_turn_does_not_claim_previous_model(self):
        self.assertEqual(p.capture(self.env | {'CODEX_TURN_ID': 'turn-2'})['actor']['llm_model'], 'unknown')

    def test_other_session_never_used(self):
        other = self.session.with_name('rollout-newer-' + str(uuid.uuid4()) + '.jsonl')
        other.write_text(json.dumps({'type': 'turn_context', 'payload': {'model': 'wrong'}}) + '\n')
        self.assertEqual(p.capture(self.env)['actor']['llm_model'], 'actual-model')

    def test_metadata_id_must_match_filename_and_current_thread(self):
        self.meta['payload']['id'] = str(uuid.uuid4())
        self.records(self.meta, self.turn)
        self.assertEqual(p.capture(self.env)['actor']['llm_model'], 'unknown')

    def test_ambiguous_session_files_fail_to_unknown(self):
        shutil.copyfile(self.session, self.session.with_name('rollout-second-' + self.sid + '.jsonl'))
        self.assertEqual(p.capture(self.env)['actor']['agent_version'], 'unknown')

    def test_absent_session_and_defaults_are_not_identity(self):
        self.session.unlink()
        (self.root / 'config.toml').write_text('model = "default-not-actual"')
        env = self.env | {'OPENAI_MODEL': 'also-not-actual', 'OPENAI_API_KEY': 'sk-private'}
        self.assertEqual(p.capture(env)['actor']['llm_model'], 'unknown')
        self.assertNotIn('sk-private', json.dumps(p.capture(env)))
        self.assertEqual(set(p.capture({})['actor'].values()), {'unknown'})

    def test_non_context_chat_content_cannot_override_model(self):
        self.records(self.meta, self.turn, {'type': 'response_item', 'payload': {'model': 'injected', 'text': 'model=fake'}})
        self.assertEqual(p.capture(self.env)['actor']['llm_model'], 'actual-model')

    def test_oversize_and_partial_lines_do_not_break_capture(self):
        with self.session.open('ab') as f:
            f.write(b'x' * (p.MAX_LINE + 10) + b'\n')
            f.write(b'{"type":"response_item"')
        self.assertEqual(p.capture(self.env)['actor']['llm_model'], 'actual-model')

    def test_generic_host_exports_are_a_complete_current_run_bundle(self):
        env = {'TEAQL_RUNTIME_SESSION_ID': 'pi-session-1', 'TEAQL_RUNTIME_AGENT': 'pi', 'TEAQL_RUNTIME_AGENT_VERSION': '1.4.0', 'TEAQL_RUNTIME_LLM_PROVIDER': 'provider-a', 'TEAQL_RUNTIME_LLM_MODEL': 'model-a'}
        self.assertEqual(p.capture(env | self.env)['actor']['agent'], 'pi')
        self.assertEqual(p.capture(env)['actor']['llm_model'], 'model-a')
        del env['TEAQL_RUNTIME_LLM_PROVIDER']
        with self.assertRaises(ValueError): p.capture(env)

    def test_remote_snapshot_freshness_and_session_binding(self):
        path = self.root / 'context.json'
        snapshot = p.capture(self.env)
        path.write_text(json.dumps(snapshot))
        self.assertEqual(p.load_context(path, {})['actor'], snapshot['actor'])
        with self.assertRaises(ValueError): p.load_context(path, {'CODEX_THREAD_ID': str(uuid.uuid4())})
        with self.assertRaises(ValueError): p.load_context(path, self.env | {'CODEX_TURN_ID': 'another-turn'})
        snapshot['captured_at'] = (datetime.now(timezone.utc) - timedelta(minutes=6)).isoformat()
        path.write_text(json.dumps(snapshot))
        with self.assertRaises(ValueError): p.load_context(path, {})

    def test_remote_snapshot_rejects_extra_secret_fields(self):
        snapshot = p.capture(self.env)
        snapshot['api_key'] = 'sk-private'
        path = self.root / 'context.json'; path.write_text(json.dumps(snapshot))
        with self.assertRaises(ValueError): p.load_context(path, {})

    def test_stamp_preserves_uuid_and_every_byte_outside_opening_root(self):
        uid = str(uuid.uuid4())
        path = self.model(attributes='model_uuid="' + uid + '" custom="a &gt; b"')
        before = path.read_bytes(); a, b, _ = p.parse_root(before)
        result = p.stamp(path, p.capture(self.env))
        after = path.read_bytes(); c, d, attrs = p.parse_root(after)
        self.assertEqual(before[:a], after[:c]); self.assertEqual(before[b:], after[d:])
        self.assertEqual(attrs['custom'], 'a > b')
        self.assertEqual(result['model_uuid'], uid)
        self.assertEqual(attrs['llm_model'], 'actual-model')
        self.assertFalse(p.stamp(path, p.capture(self.env))['changed'])

    def test_actor_change_keeps_lifecycle_uuid(self):
        path = self.model(); first = p.stamp(path, p.capture(self.env))
        self.records(self.meta, {'type': 'turn_context', 'payload': {'model': 'switched'}})
        second = p.stamp(path, p.capture(self.env))
        self.assertEqual(first['model_uuid'], second['model_uuid'])
        self.assertEqual(second['actor']['llm_model'], 'switched')
        third = p.stamp(path, p.capture({}))
        self.assertEqual(first['model_uuid'], third['model_uuid'])
        self.assertEqual(third['actor']['llm_model'], 'unknown')

    def test_invalid_uuid_is_not_replaced(self):
        path = self.model(attributes='model_uuid="broken"'); before = path.read_bytes()
        with self.assertRaises(ValueError): p.stamp(path, p.capture(self.env))
        self.assertEqual(path.read_bytes(), before)

    def test_split_model_stamps_entry_only(self):
        main = self.model('main.xml'); module = self.root / 'module.xml'
        module.write_text('<root><child/></root>'); before = module.read_bytes()
        self.assertEqual(p.stamp(self.root, p.capture(self.env))['entry'], str(main.resolve()))
        self.assertEqual(module.read_bytes(), before)
        with self.assertRaises(ValueError): p.stamp(module, p.capture(self.env))

    def test_directory_requires_unambiguous_entry(self):
        self.model('one.xml'); self.model('two.xml')
        with self.assertRaises(ValueError): p.entry_path(self.root)
        self.assertEqual(p.entry_path(self.root, 'one.xml'), self.root / 'one.xml')
        with self.assertRaises(ValueError): p.entry_path(self.root, '../outside.xml')

    def test_atomic_invalid_xml_dtd_and_symlink_rejected(self):
        path = self.root / 'bad.xml'
        for raw in ['<root name="x"><bad></root>', '<!DOCTYPE root [<!ENTITY x "secret">]><root name="x"/>']:
            path.write_text(raw)
            with self.assertRaises(Exception): p.stamp(path, p.capture(self.env))
            self.assertEqual(path.read_text(), raw)
        link = self.root / 'link.xml'; link.symlink_to(self.model())
        with self.assertRaises(ValueError): p.stamp(link, p.capture(self.env))

    def test_file_mode_retained_and_self_closing_root_supported(self):
        path = self.root / 'small.xml'; path.write_text('<root name="x-service"/>'); path.chmod(0o640)
        p.stamp(path, p.capture(self.env))
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)
        self.assertTrue(path.read_bytes().endswith(b'/>'))

    def test_secret_like_or_unbounded_identifiers_become_unknown(self):
        for bad in ['sk-secret', 'Bearer abc', 'https://example.com?key=secret', 'x' * 201, 'model\nsecret']:
            self.assertEqual(p.value(bad), 'unknown')

    def test_copied_skill_works_without_repository_or_installed_packages(self):
        installed = self.root / 'installed/build-teaql-app'
        shutil.copytree(SCRIPT.parents[1], installed)
        path = self.model()
        env = {k: v for k, v in os.environ.items() if not k.startswith(('CODEX_', 'TEAQL_RUNTIME_'))} | self.env
        result = subprocess.run([sys.executable, str(installed / 'scripts/model_provenance.py'), 'stamp', '--input', str(path)], env=env, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['skill_version'], '2026.10.27.1')


if __name__ == '__main__':
    unittest.main()
