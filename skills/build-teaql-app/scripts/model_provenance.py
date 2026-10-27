#!/usr/bin/env python3
"""Capture current Agent metadata and stamp only a KSML entry root (stdlib only)."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import uuid
from xml.parsers import expat
from xml.sax.saxutils import quoteattr

FIELDS = ('agent', 'agent_version', 'llm_provider', 'llm_model')
ENV_FIELDS = {key: 'TEAQL_RUNTIME_' + key.upper() for key in FIELDS}
SCHEMA = 'teaql.runtime-actor/v1'
MAX_XML = 10 * 1024 * 1024
MAX_LINE = 1024 * 1024


def value(raw):
    # Identifiers only: no prompts, URLs, arbitrary environment dumps or credentials.
    if not isinstance(raw, str):
        return 'unknown'
    raw = raw.strip()
    if not raw or raw.lower() == 'unknown':
        return 'unknown'
    if len(raw) > 200 or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._+:/@ -]*', raw):
        return 'unknown'
    if '://' in raw or raw.lower().startswith(('sk-', 'bearer ', 'ghp_', 'github_pat_')):
        return 'unknown'
    return raw


def codex_actor(env):
    actor = dict.fromkeys(FIELDS, 'unknown')
    sources = dict.fromkeys(FIELDS, 'unavailable')
    session_id = env.get('CODEX_THREAD_ID', '')
    if not session_id:
        return actor, sources, None, None
    try:
        uuid.UUID(session_id)
    except ValueError:
        return actor, sources, None, None
    actor['agent'], sources['agent'] = 'codex', 'CODEX_THREAD_ID'
    home = Path(env.get('CODEX_HOME') or Path.home() / '.codex')
    # Match only this session. Never choose the newest session or read config defaults.
    candidates = list((home / 'sessions').glob('**/*-' + session_id + '.jsonl'))
    if len(candidates) != 1:
        return actor, sources, session_id, None
    meta, turn = None, None
    try:
        with candidates[0].open('rb') as stream:
            while True:
                line = stream.readline(MAX_LINE + 1)
                if not line:
                    break
                if len(line) > MAX_LINE:
                    while line and not line.endswith(b'\n'):
                        line = stream.readline(MAX_LINE + 1)
                    continue
                # A writer may still be appending the final record.
                if not line.endswith(b'\n'):
                    continue
                try:
                    record = json.loads(line)
                except (ValueError, UnicodeError):
                    continue
                if not isinstance(record, dict):
                    continue
                payload = record.get('payload')
                if not isinstance(payload, dict):
                    continue
                if record.get('type') == 'session_meta':
                    if payload.get('id') != session_id:
                        return actor, sources, session_id, None
                    meta = {k: payload.get(k) for k in ('cli_version', 'model_provider')}
                elif record.get('type') == 'turn_context':
                    # Use the latest context, even when its model is missing. Do not
                    # accidentally carry a known model across an unknown/switching turn.
                    turn = {k: payload.get(k) for k in ('turn_id', 'model', 'model_provider')}
    except OSError:
        return actor, sources, session_id, None
    if meta is None:
        return actor, sources, session_id, None
    wanted_turn = env.get('CODEX_TURN_ID')
    actor['agent_version'] = value(meta.get('cli_version'))
    sources['agent_version'] = 'codex.session_meta.cli_version'
    if turn is not None and (not wanted_turn or wanted_turn == turn.get('turn_id')):
        actor['llm_model'] = value(turn.get('model'))
        actor['llm_provider'] = value(turn.get('model_provider') or meta.get('model_provider'))
        sources['llm_model'] = 'codex.turn_context.model'
        sources['llm_provider'] = 'codex.turn_context.model_provider' if turn.get('model_provider') else 'codex.session_meta.model_provider'
        return actor, sources, session_id, turn.get('turn_id')
    return actor, sources, session_id, None


def capture(env=None):
    env = os.environ if env is None else env
    # Other hosts can export a *current-run* identity bundle from their own API.
    # A complete bundle is intentional; partial fields never mix two agents.
    explicit = [key for key in ENV_FIELDS.values() if key in env]
    if explicit:
        if len(explicit) != len(FIELDS) or not env.get('TEAQL_RUNTIME_SESSION_ID'):
            raise ValueError('Runtime exports require all four TEAQL_RUNTIME_* fields and TEAQL_RUNTIME_SESSION_ID; use unknown for unavailable fields')
        actor = {key: value(env[name]) for key, name in ENV_FIELDS.items()}
        sources = {key: name for key, name in ENV_FIELDS.items()}
        session_id, turn_id = value(env['TEAQL_RUNTIME_SESSION_ID']), None
        if session_id == 'unknown':
            raise ValueError('Runtime session ID is unavailable or invalid')
    else:
        actor, sources, session_id, turn_id = codex_actor(env)
    return {'schema': SCHEMA, 'captured_at': datetime.now(timezone.utc).isoformat(),
            'session_id': session_id, 'turn_id': turn_id, 'actor': actor, 'sources': sources}


def load_context(path, env=None):
    env = os.environ if env is None else env
    if path.stat().st_size > 16384:
        raise ValueError('Runtime context is too large')
    data = json.loads(path.read_text())
    allowed = {'schema', 'captured_at', 'session_id', 'turn_id', 'actor', 'sources'}
    if not isinstance(data, dict) or set(data) - allowed or data.get('schema') != SCHEMA:
        raise ValueError('Unsupported runtime context')
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(data['captured_at'])).total_seconds()
    if not -30 <= age <= 300:
        raise ValueError('Runtime context expired; capture again on the Agent host')
    current = env.get('TEAQL_RUNTIME_SESSION_ID') or env.get('CODEX_THREAD_ID')
    if current and current != data.get('session_id'):
        raise ValueError('Runtime context belongs to a different current session')
    if env.get('CODEX_TURN_ID') and env['CODEX_TURN_ID'] != data.get('turn_id'):
        raise ValueError('Runtime context belongs to a different current turn')
    if not isinstance(data.get('actor'), dict) or set(data['actor']) != set(FIELDS):
        raise ValueError('Runtime context must contain exactly the four actor fields')
    # Ignore arbitrary source descriptions in input; only normalized identities leave this process.
    data['actor'] = {key: value(data['actor'][key]) for key in FIELDS}
    return data


def parse_root(body):
    body.decode('utf-8-sig')  # XML byte patching below deliberately supports UTF-8 only.
    if len(body) > MAX_XML:
        raise ValueError('Model exceeds 10 MiB')
    parser = expat.ParserCreate()
    parser.ordered_attributes = True
    found = []

    def start(name, attributes):
        if not found:
            if name != 'root':
                raise ValueError('Expected one unqualified KSML root element')
            found.append((parser.CurrentByteIndex, dict(zip(attributes[::2], attributes[1::2]))))

    def no_dtd(*_):
        raise ValueError('DTD/entity declarations are not supported')

    parser.StartElementHandler = start
    parser.StartDoctypeDeclHandler = no_dtd
    parser.EntityDeclHandler = no_dtd
    parser.Parse(body, True)
    if not found:
        raise ValueError('Save a complete model before stamping provenance')
    offset, attributes = found[0]
    quote = None
    for end in range(offset, len(body)):
        ch = body[end]
        if quote:
            if ch == quote:
                quote = None
        elif ch in (34, 39):
            quote = ch
        elif ch == 62:
            return offset, end + 1, attributes
    raise ValueError('Incomplete root opening tag')


def entry_path(model, entry=None):
    model = Path(model)
    if not model.is_dir():
        if entry:
            raise ValueError('--entry applies only to a model directory')
        return model
    if entry:
        selected = model / entry
        if not selected.resolve().is_relative_to(model.resolve()):
            raise ValueError('Entry escapes model directory')
        return selected
    main = model / 'main.xml'
    if main.is_file():
        return main
    candidates = []
    for path in sorted(model.glob('*.xml')):
        _, _, attributes = parse_root(path.read_bytes())
        if attributes.get('name'):
            candidates.append(path)
    if len(candidates) != 1:
        raise ValueError('Ambiguous model directory; pass --entry relative/path.xml')
    return candidates[0]


def skill_version():
    skill = Path(__file__).resolve().parents[1]
    repo = skill.parents[1]
    if (repo / 'skills/build-teaql-app').resolve() == skill and (repo / '.git').exists():
        try:
            rev = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, timeout=3, text=True).strip()
            dirty = subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain', '--', 'skills/build-teaql-app'], timeout=3, text=True).strip()
            return rev + ('-dirty' if dirty else '')
        except (OSError, subprocess.SubprocessError):
            pass
    try:
        return value((skill / 'VERSION').read_text())
    except OSError:
        return 'unknown'


def stamp(model, context, entry=None):
    path = entry_path(model, entry)
    if path.is_symlink():
        raise ValueError('Entry must be a regular file, not a symlink')
    before = path.read_bytes()
    start, end, attributes = parse_root(before)
    if not attributes.get('name'):
        raise ValueError('Entry root must declare its service name; do not stamp included module roots')
    existing = attributes.get('model_uuid')
    if existing is not None:
        uuid.UUID(existing)  # Never replace an invalid identity silently.
    attributes['model_uuid'] = existing or str(uuid.uuid4())
    attributes.update({key: value(context['actor'].get(key)) for key in FIELDS})
    attributes['skill_version'] = skill_version()
    closing = '/>' if before[start:end].rstrip().endswith(b'/>') else '>'
    opening = '<root' + ''.join(' ' + k + '=' + quoteattr(v) for k, v in attributes.items()) + closing
    after = before[:start] + opening.encode('utf-8') + before[end:]
    parse_root(after)
    changed = after != before
    if changed:
        descriptor, tmp = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
        try:
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(after)
                stream.flush()
                os.fsync(stream.fileno())
            os.chmod(tmp, stat.S_IMODE(path.stat().st_mode))
            if path.read_bytes() != before:
                raise ValueError('Model changed concurrently; retry provenance capture/stamp')
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    return {'entry': str(path.resolve()), 'changed': changed,
            'model_uuid': attributes['model_uuid'],
            'actor': {key: attributes[key] for key in FIELDS},
            'skill_version': attributes['skill_version']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('capture', help='Emit only current-run identity metadata; run on Agent host')
    apply = commands.add_parser('stamp', help='Write identity to saved entry root before each TeaQL operation')
    apply.add_argument('--input', required=True)
    apply.add_argument('--entry')
    apply.add_argument('--context', type=Path, help='Fresh capture JSON from Agent host (for SSH execution)')
    args = parser.parse_args()
    try:
        if args.command == 'capture':
            result = capture()
        else:
            context = load_context(args.context) if args.context else capture()
            result = stamp(args.input, context, args.entry)
        print(json.dumps(result, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError, expat.ExpatError) as error:
        # No transcript content, XML values, credentials or subprocess stderr in diagnostics.
        print('Provenance could not be applied: ' + type(error).__name__ + '. Check input/context and recapture if needed.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
