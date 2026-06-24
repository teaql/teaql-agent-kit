import pytest

from update_versions import (
    DEFAULT_TARGET_VERSION,
    collect_files,
    compile_patterns,
    update_content,
    update_file,
    update_versions,
)


@pytest.fixture
def mixed_content() -> str:
    return """\
Install cargo-teaql` version `0.2.0`.
Make sure cargo-teaql >= 0.2.2 is available.
Use cargo-teaql 0.2.0 for this guide.
The package is `cargo-teaql` `1.0.0`.
"""


@pytest.fixture
def updated_content() -> str:
    version = DEFAULT_TARGET_VERSION
    return f"""\
Install cargo-teaql` version `{version}`.
Make sure cargo-teaql >= {version} is available.
Use cargo-teaql {version} for this guide.
The package is `cargo-teaql` `{version}`.
"""


def test_compile_patterns_parameterizes_version() -> None:
    patterns = compile_patterns("3.0.0")
    assert all("3.0.0" in replacement for _pattern, replacement in patterns)


def test_update_content(mixed_content: str, updated_content: str) -> None:
    assert update_content(mixed_content, DEFAULT_TARGET_VERSION) == updated_content


def test_update_content_no_match_unchanged() -> None:
    content = "No cargo-teaql references here.\n"
    assert update_content(content, DEFAULT_TARGET_VERSION) == content


def test_update_file_updates_and_reports(tmp_path, mixed_content: str, updated_content: str) -> None:
    doc = tmp_path / "README.md"
    doc.write_text(mixed_content, encoding="utf-8")

    assert update_file(doc, DEFAULT_TARGET_VERSION) is True
    assert doc.read_text(encoding="utf-8") == updated_content


def test_update_file_unchanged(tmp_path) -> None:
    doc = tmp_path / "README.md"
    doc.write_text("No version info.\n", encoding="utf-8")

    assert update_file(doc, DEFAULT_TARGET_VERSION) is False


def test_collect_files_respects_globs(tmp_path) -> None:
    (tmp_path / "a.md").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    sub = tmp_path / "agents"
    sub.mkdir()
    (sub / "c.md").write_text("c")

    files = collect_files(tmp_path, globs=["*.md", "agents/*.md"])
    assert files == [tmp_path / "a.md", sub / "c.md"]


def test_update_versions_integration(tmp_path, mixed_content: str, updated_content: str) -> None:
    (tmp_path / "README.md").write_text(mixed_content, encoding="utf-8")

    changed = update_versions(tmp_path, version="2.0.2", globs=["*.md"])

    assert changed == 1
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == updated_content
