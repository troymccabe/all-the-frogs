#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys

IMAGE_EXTENSIONS = {".gif", ".jpg", ".jpeg", ".png", ".webp", ".svg"}


def rename_stem(stem: str) -> str | None:
    if not stem.startswith("bufo-"):
        return None
    thing = stem.removeprefix("bufo-")
    if not thing:
        return None
    return f"{thing}-frog"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    source_dir = repo_root / "all-the-bufo"
    target_dir = repo_root / "all-the-frogs"

    if not source_dir.is_dir():
        print(f"error: source directory not found: {source_dir}", file=sys.stderr)
        return 1

    target_dir.mkdir(exist_ok=True)

    copied = 0
    for path in sorted(source_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        new_stem = rename_stem(path.stem)
        if new_stem is None:
            continue

        destination = target_dir / f"{new_stem}{path.suffix.lower()}"

        if destination.exists():
            print(f"error: destination already exists: {destination.name}", file=sys.stderr)
            return 1

        shutil.copy2(path, destination)
        print(f"Copied {path.name} -> {destination.name}")
        copied += 1

    print(f"Wrote {copied} frog files to {target_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
