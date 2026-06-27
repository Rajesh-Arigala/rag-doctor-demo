# Knowledge Export -> Import -> Test Runbook

Project role: `rag-usecase-0` is the knowledge factory.  
Companion consumer: main multi-agent `usecase-0-v2`.

Use this runbook whenever doctor-approved content is updated and needs to move from the RAG demo into the main multi-agent project.

## 1. What This Folder Does

This folder owns:

- Doctor feedback intake.
- Approved clinic Q&A.
- Prompt policy.
- RAG-ready corpus.
- Embedding generation/export.
- Weekly knowledge bundle creation.

It does **not** own the final multi-agent runtime.

## 2. Weekly Workflow

```text
Doctor .md feedback
        ↓
Triage + approved Q&A
        ↓
Update RAG-ready corpus
        ↓
Rebuild embeddings
        ↓
Export knowledge bundle
        ↓
Import into main multi-agent usecase-0
        ↓
Run main tests
```

## 3. Source Files Used For Export

Current active source files:

```text
data/corpus/drmadhupatil_enriched_rag_corpus.jsonl
data/corpus/metadata_enrichment_manifest.json
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
PROMPT_ENGINEERING_FINAL.md
backend/app/rag/faq.py
```

If `data/embeddings/drmadhupatil_vertex_embeddings.jsonl` is missing, rebuild embeddings before doing a production import.

Build command:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
PYTHONPATH=backend python3 scripts/build_vertex_embeddings.py
```

## 4. Data Formats

### `corpus.jsonl`

JSON Lines file. One document per line.

Expected fields include:

```json
{
  "doc_id": "WEB-DRMADHU-001",
  "source_type": "website",
  "usecase": "doctor_appointment",
  "domain": "drmadhupatil.com",
  "page_id": "00_Homepage",
  "title": "Dr. Madhu Patil | Gynecologist & IVF Specialist",
  "url": "https://drmadhupatil.com/",
  "canonical_url": "https://drmadhupatil.com",
  "content": "clean RAG text",
  "metadata": {}
}
```

### `metadata_manifest.json`

JSON manifest describing corpus count, metadata version, page types, and enrichment information.

### `embeddings.jsonl`

JSON Lines embedding file. Each line should map a document id to its embedding vector.

Expected concept:

```json
{
  "doc_id": "WEB-DRMADHU-001",
  "embedding": [0.01, 0.02, 0.03]
}
```

Exact shape may follow the active embedding builder. Keep the import consumer aligned with the current loader.

### `prompt_policy.md`

Markdown file containing final assistant prompt rules.

Source:

```text
PROMPT_ENGINEERING_FINAL.md
```

### `faq_exact_answers.py`

Python exact-answer layer for high-value deterministic clinic questions.

Source:

```text
backend/app/rag/faq.py
```

### `content_version.json`

Audit manifest generated during export.

It records:

- knowledge version
- export timestamp
- source project
- source paths
- missing files

## 5. Export Command

Run:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
python3 scripts/export_knowledge_bundle.py
```

For a complete build/export/import in one command, run:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
scripts/run_full_knowledge_sync.sh \
  "/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2/backend/knowledge/latest"
```

This full sync requires:

```text
google-genai installed
Google Application Default Credentials available
Vertex AI access to text-embedding-005
```

Expected output:

```text
exports/YYYY_MM_DD_knowledge_bundle/
exports/latest/
```

Expected files:

```text
exports/latest/corpus.jsonl
exports/latest/metadata_manifest.json
exports/latest/embeddings.jsonl
exports/latest/prompt_policy.md
exports/latest/faq_exact_answers.py
exports/latest/content_version.json
exports/latest/README.md
```

Note:

```text
exports/ is generated and ignored by git.
```

## 6. Export Validation

Check:

```bash
ls -la exports/latest
sed -n '1,160p' exports/latest/content_version.json
```

Confirm:

```text
missing_source_files is empty
embeddings.jsonl exists
corpus.jsonl exists
prompt_policy.md exists
faq_exact_answers.py exists
```

If `embeddings.jsonl` is missing, do not import into the main project for production testing yet.

## 7. Import Into Main Multi-Agent Project

Recommended destination:

```text
/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2/backend/knowledge/latest/
```

Run:

```bash
cd /Users/jhonny001/Desktop/rag-usecase-0
python3 scripts/import_knowledge_bundle.py \
  exports/latest \
  "/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2/backend/knowledge/latest"
```

## 8. Main Project Test Commands

After import, go to the main project:

```bash
cd "/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2"
```

Run existing tests:

```bash
PYTHONPATH=. python -m pytest -p no:cacheprovider
```

Run smoke tests as needed:

```bash
PYTHONPATH=. python scripts/smoke_hybrid_retrieval.py
PYTHONPATH=. python scripts/smoke_agent_vertex_retrieval.py
PYTHONPATH=. python scripts/smoke_api_local.py
```

## 9. Deployment Rule

Do not redeploy for documentation-only changes.

Redeploy the RAG demo only if these changed:

```text
backend/
frontend/
data/corpus/
data/embeddings/
Dockerfile
backend/requirements.txt
```

Main multi-agent deployment should happen only after:

- import succeeds
- tests pass
- app runtime points to imported knowledge
- smoke test passes

## 10. One-Line Reminder

```text
Export from RAG demo. Import into main multi-agent. Test main. Then deploy.
```
