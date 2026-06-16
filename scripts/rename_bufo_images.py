#!/usr/bin/env python3

from pathlib import Path
import shutil
import sys

IMAGE_EXTENSIONS = {".gif", ".jpg", ".jpeg", ".png", ".webp", ".svg"}


def rename_stem(stem: str) -> str | None:
    if stem.startswith("bufo-"):
        thing = stem.removeprefix("bufo-")
        if not thing:
            return None
        return f"{thing}-frog"

    if stem.startswith("bufo"):
        thing = stem.removeprefix("bufo").lstrip("-_")
        if not thing:
            return "frog"
        return f"{thing}-frog"

    if stem.endswith("-bufo"):
        thing = stem.removesuffix("-bufo")
        if not thing:
            return None
        return f"{thing}-frog"

    if "-" not in stem:
        if stem in {"bufo", "boofo"}:
            return "frog"
        if "boofo" in stem:
            return stem.replace("boofo", "frog", 1)
        if "bufo" in stem:
            return stem.replace("bufo", "frog", 1)

    return None


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    source_dir = repo_root / "all-the-bufo"
    target_dir = repo_root / "all-the-frogs"

    if not source_dir.is_dir():
        print(f"error: source directory not found: {source_dir}", file=sys.stderr)
        return 1

    target_dir.mkdir(exist_ok=True)

    copied = 0
    skipped = 0
    for path in sorted(source_dir.iterdir()):
        if not path.is_file():
            continue
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        new_stem = rename_stem(path.stem)
        if new_stem is None:
            print(f"Skipped (unmatched filename): {path.name}", file=sys.stderr)
            skipped += 1
            continue

        destination = target_dir / f"{new_stem}{path.suffix.lower()}"

        if destination.exists():
            print(f"error: destination already exists: {destination.name}", file=sys.stderr)
            return 1

        shutil.copy2(path, destination)
        print(f"Copied {path.name} -> {destination.name}")
        copied += 1

    print(f"Wrote {copied} frog files to {target_dir}.")
    if skipped:
        print(f"Skipped {skipped} image files that did not match known bufo patterns.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
