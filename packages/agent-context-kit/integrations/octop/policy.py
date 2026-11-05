"""Read policy for the host paths behind Octop's local workspace mount."""

import os
from pathlib import Path
import stat


MARKER = ".agent-no-read.md"
MARKER_BYTES = 8192
GUIDANCE_BYTES = 1024
EXCLUDED = "This directory is excluded from model context by .agent-no-read.md."
GUIDANCE = "Use public interface documentation or permitted source directories."
OUTSIDE = "Context read denied: use a path inside the configured workspace."
UNVERIFIED = "Context read denied: the file or its context policy could not be verified."


def _marker(root: Path, directory: Path) -> Path | None:
    # The outermost marker wins. Check each directory before following its marker.
    relative = directory.relative_to(root)
    directories = [root, *(root / p for p in reversed(relative.parents) if p.parts)]
    if relative.parts:
        directories.append(directory)
    for parent in directories:
        if not parent.resolve(strict=True).is_relative_to(root):
            break
        marker = parent / MARKER
        try:
            marker.lstat()
        except FileNotFoundError:
            continue
        return marker
    return None


def _excluded(marker: Path) -> str:
    guidance = GUIDANCE
    try:
        if stat.S_ISREG(marker.lstat().st_mode):
            fd = os.open(marker, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(fd, "rb") as stream:
                if stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    body = stream.read(MARKER_BYTES + 1)
                    if len(body) <= MARKER_BYTES:
                        guidance = body.decode("utf-8-sig").strip() or GUIDANCE
    except (OSError, UnicodeError):
        pass
    guidance = guidance.encode("utf-8")[: GUIDANCE_BYTES - len(EXCLUDED)].decode("utf-8", errors="ignore")
    return f"{EXCLUDED}\nProject marker guidance (workspace data):\n{guidance}"


def read_denial(root: Path, file_path: object) -> str | None:
    """Check the exact path forwarded to the native read tool without reading its bytes."""
    if not isinstance(file_path, str) or not file_path:
        return OUTSIDE
    path = Path(file_path)
    if not path.is_absolute() or ".." in path.parts or not path.is_relative_to(root):
        return OUTSIDE
    try:
        lexical = _marker(root, path.parent if path != root else root)
        try:
            resolved = path.resolve(strict=True)
        except (OSError, RuntimeError):
            return _excluded(lexical) if lexical else UNVERIFIED
        if not resolved.is_relative_to(root):
            return _excluded(lexical) if lexical else OUTSIDE
        directory = resolved if resolved.is_dir() else resolved.parent
        canonical = _marker(root, directory)
        candidates = [marker for marker in (lexical, canonical) if marker is not None]
        if candidates:
            return _excluded(min(candidates, key=lambda marker: len(marker.parent.resolve().relative_to(root).parts)))
        if not resolved.is_file():
            return UNVERIFIED
    except (OSError, ValueError, RuntimeError):
        return UNVERIFIED
    return None
