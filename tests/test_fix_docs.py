import pytest

from fix_docs import apply_replacements, fix_docs, fix_file


@pytest.fixture
def outdated_sample() -> str:
    return """\
Run the old goal:

    mvn io.teaql:teaql-maven-plugin:1.0.1:gen-lib

Requires cargo-teaql >= 0.2.2 and version `0.2.2` of the CLI.
"""


@pytest.fixture
def updated_sample() -> str:
    return """\
Run the old goal:

    mvn io.teaql:teaql-maven-plugin:1.1.0:generate -Dservice=java-lib

Requires cargo-teaql >= 1.1.0 and version `1.1.0` of the CLI.
"""


def test_apply_replacements(outdated_sample: str, updated_sample: str) -> None:
    assert apply_replacements(outdated_sample) == updated_sample


def test_apply_replacements_no_match_unchanged() -> None:
    content = "Nothing to change here.\n"
    assert apply_replacements(content) == content


def test_fix_file_updates_and_reports(tmp_path, outdated_sample: str, updated_sample: str) -> None:
    doc = tmp_path / "doc.md"
    doc.write_text(outdated_sample, encoding="utf-8")

    assert fix_file(doc) is True
    assert doc.read_text(encoding="utf-8") == updated_sample


def test_fix_file_unchanged(tmp_path) -> None:
    doc = tmp_path / "doc.md"
    doc.write_text("Already current.\n", encoding="utf-8")

    assert fix_file(doc) is False


def test_fix_docs_walks_directory(tmp_path, outdated_sample: str, updated_sample: str) -> None:
    nested = tmp_path / "playbooks"
    nested.mkdir()
    (tmp_path / "root.md").write_text(outdated_sample, encoding="utf-8")
    (nested / "deep.md").write_text(outdated_sample, encoding="utf-8")
    (tmp_path / "skip.txt").write_text(outdated_sample, encoding="utf-8")

    changed = fix_docs(tmp_path)

    assert changed == 2
    assert (tmp_path / "root.md").read_text(encoding="utf-8") == updated_sample
    assert (nested / "deep.md").read_text(encoding="utf-8") == updated_sample
    assert (tmp_path / "skip.txt").read_text(encoding="utf-8") == outdated_sample
