# Knowledge Sync Orchestration

Purpose: Explain how the RAG doctor demo exports approved knowledge and how the main multi-agent project imports it without manual selective copying.

Read this when you forget how weekly RAG updates move into the main multi-agent implementation.

## 1. Mental Model

```text
rag-doctor-demo
  = knowledge factory

main multi-agent usecase-0
  = runtime consumer
```

The RAG demo is where doctor feedback, approved Q&A, prompt tuning, and content improvement happen.

The main multi-agent project should not receive the whole RAG demo folder. It should receive only a clean knowledge bundle.

## 2. Weekly Flow

```text
Doctor Q&A updates
        ↓
RAG demo content curation
        ↓
RAG-ready corpus + embeddings rebuilt
        ↓
Export knowledge bundle
        ↓
Import bundle into main multi-agent project
        ↓
Run main project tests
        ↓
Deploy main usecase-0 when ready
```

## 3. Export Command

Run from the RAG demo project root:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
python3 scripts/export_knowledge_bundle.py
```

Full build/export/import command:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
scripts/run_full_knowledge_sync.sh \
  "/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2/backend/knowledge/latest"
```

This command builds Vertex embeddings first, so it requires Google ADC/Vertex access.

This creates:

```text
exports/latest/
exports/YYYY_MM_DD_knowledge_bundle/
```

`exports/` is a generated folder and is intentionally ignored by git. Regenerate it whenever needed.

## 4. Export Bundle Contents

Each exported bundle contains:

```text
corpus.jsonl
metadata_manifest.json
embeddings.jsonl
prompt_policy.md
faq_exact_answers.py
content_version.json
README.md
```

If embeddings are not available locally, the export script writes a clear warning in `content_version.json`.

Before a production import into the main multi-agent project, confirm that this file exists in the bundle:

```text
exports/latest/embeddings.jsonl
```

If it is missing, rebuild or regenerate embeddings first.

Build embeddings with:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
PYTHONPATH=backend python3 scripts/build_vertex_embeddings.py
```

## 5. Import Command

Run from the RAG demo project root, pointing to the main project destination:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
python3 scripts/import_knowledge_bundle.py \
  exports/latest \
  "/path/to/main-project/backend/knowledge/latest"
```

Recommended future destination in the main multi-agent project:

```text
backend/knowledge/latest/
```

## 6. What Gets Synced

Synced:

- Active RAG corpus.
- Metadata manifest.
- Active embeddings.
- Final prompt policy.
- Exact FAQ answer layer.
- Content version manifest.

Not synced:

- RAG demo frontend.
- RAG demo Cloud Run scripts.
- Raw doctor feedback.
- Full content lane drafts.
- Doctor-facing documentation.
- Demo-only deployment files.

## 7. Main Project Consumption Rule

The main project should treat this folder as its knowledge input:

```text
backend/knowledge/latest/
```

Expected files:

```text
backend/knowledge/latest/corpus.jsonl
backend/knowledge/latest/metadata_manifest.json
backend/knowledge/latest/embeddings.jsonl
backend/knowledge/latest/prompt_policy.md
backend/knowledge/latest/faq_exact_answers.py
backend/knowledge/latest/content_version.json
```

The main runtime can then map:

```text
RAG_CORPUS_PATH=backend/knowledge/latest/corpus.jsonl
RAG_EMBEDDINGS_PATH=backend/knowledge/latest/embeddings.jsonl
RAG_METADATA_MANIFEST_PATH=backend/knowledge/latest/metadata_manifest.json
```

## 8. Version Manifest

Every export writes:

```text
content_version.json
```

It records:

- Knowledge version.
- Export timestamp.
- Source project.
- Corpus path.
- Embedding path.
- Prompt policy path.
- FAQ layer path.
- Missing files, if any.

This is the audit trail for weekly knowledge movement.

## 9. When To Export

Export after:

- Doctor-approved Q&A is merged.
- RAG-ready corpus is updated.
- Embeddings are rebuilt.
- Local RAG demo tests pass.

Suggested cadence:

```text
Daily:
Collect doctor Q&A.

Every 3-5 days:
Triage and approve Q&A.

Weekly:
Rebuild corpus/embeddings, export bundle, import into main project, test.
```

## 10. When To Deploy

RAG demo Cloud Run:

- Redeploy only if demo runtime files changed.

Main multi-agent Cloud Run:

- Redeploy after imported knowledge is tested and the main app points to the new knowledge bundle.

## 11. One-Line Summary

```text
RAG demo exports knowledge. Main multi-agent imports knowledge. No weekly manual copying.
```
