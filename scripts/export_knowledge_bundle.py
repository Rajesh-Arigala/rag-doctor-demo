from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORTS_DIR = PROJECT_ROOT / "exports"

ACTIVE_CORPUS = PROJECT_ROOT / "data/corpus/drmadhupatil_enriched_rag_corpus.jsonl"
ACTIVE_METADATA_MANIFEST = PROJECT_ROOT / "data/corpus/metadata_enrichment_manifest.json"
ACTIVE_EMBEDDINGS = PROJECT_ROOT / "data/embeddings/drmadhupatil_vertex_embeddings.jsonl"
PROMPT_POLICY = PROJECT_ROOT / "PROMPT_ENGINEERING_FINAL.md"
FAQ_LAYER = PROJECT_ROOT / "backend/app/rag/faq.py"


def copy_if_exists(source: Path, destination: Path, missing: list[str]) -> bool:
    if not source.exists():
        missing.append(str(source.relative_to(PROJECT_ROOT)))
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_readme(path: Path, version: str) -> None:
    path.write_text(
        f"""# Knowledge Bundle

Version: `{version}`

This bundle was exported from `rag-doctor-demo`.

Use it as an import package for the main multi-agent usecase-0 project.

Expected files:

```text
corpus.jsonl
metadata_manifest.json
embeddings.jsonl
prompt_policy.md
faq_exact_answers.py
content_version.json
```

Main project destination recommendation:

```text
backend/knowledge/latest/
```
""",
        encoding="utf-8",
    )


def main() -> None:
    today = datetime.now().strftime("%Y_%m_%d")
    timestamp = datetime.now().isoformat(timespec="seconds")
    version = f"{today}_knowledge_bundle"

    dated_dir = EXPORTS_DIR / version
    latest_dir = EXPORTS_DIR / "latest"

    for directory in (dated_dir, latest_dir):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    missing: list[str] = []
    files = {
        "corpus.jsonl": ACTIVE_CORPUS,
        "metadata_manifest.json": ACTIVE_METADATA_MANIFEST,
        "embeddings.jsonl": ACTIVE_EMBEDDINGS,
        "prompt_policy.md": PROMPT_POLICY,
        "faq_exact_answers.py": FAQ_LAYER,
    }

    for output_name, source in files.items():
        copy_if_exists(source, dated_dir / output_name, missing)

    manifest = {
        "knowledge_version": version,
        "generated_at": timestamp,
        "source_project": "rag-doctor-demo",
        "source_root": str(PROJECT_ROOT),
        "bundle_files": sorted(files.keys()),
        "missing_source_files": missing,
        "active_corpus": str(ACTIVE_CORPUS.relative_to(PROJECT_ROOT)),
        "active_metadata_manifest": str(ACTIVE_METADATA_MANIFEST.relative_to(PROJECT_ROOT)),
        "active_embeddings": str(ACTIVE_EMBEDDINGS.relative_to(PROJECT_ROOT)),
        "prompt_policy": str(PROMPT_POLICY.relative_to(PROJECT_ROOT)),
        "faq_layer": str(FAQ_LAYER.relative_to(PROJECT_ROOT)),
    }

    write_json(dated_dir / "content_version.json", manifest)
    write_readme(dated_dir / "README.md", version)

    shutil.copytree(dated_dir, latest_dir, dirs_exist_ok=True)

    print("Knowledge bundle exported")
    print(f"version={version}")
    print(f"dated={dated_dir}")
    print(f"latest={latest_dir}")
    if missing:
        print("missing_files=" + ", ".join(missing))


if __name__ == "__main__":
    main()

