from __future__ import annotations

import shutil
import sys
from pathlib import Path


REQUIRED_FILES = {
    "corpus.jsonl",
    "embeddings.jsonl",
    "metadata_manifest.json",
    "prompt_policy.md",
    "faq_exact_answers.py",
    "content_version.json",
}


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/import_knowledge_bundle.py <bundle_dir> <destination_dir>")
        raise SystemExit(2)

    bundle_dir = Path(sys.argv[1]).expanduser().resolve()
    destination_dir = Path(sys.argv[2]).expanduser().resolve()

    if not bundle_dir.exists():
        raise SystemExit(f"Bundle does not exist: {bundle_dir}")

    missing = sorted(name for name in REQUIRED_FILES if not (bundle_dir / name).exists())
    if missing:
        raise SystemExit("Bundle is missing required files: " + ", ".join(missing))

    destination_dir.mkdir(parents=True, exist_ok=True)

    for item in bundle_dir.iterdir():
        if item.is_file():
            shutil.copy2(item, destination_dir / item.name)

    print("Knowledge bundle imported")
    print(f"source={bundle_dir}")
    print(f"destination={destination_dir}")


if __name__ == "__main__":
    main()
