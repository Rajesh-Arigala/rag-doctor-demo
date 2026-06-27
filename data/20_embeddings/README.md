# 20 Embeddings Reference Layer

This is the numbered reference layer for embeddings and vector indexes.

Current active app embedding path is:

```text
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
```

The app reads this path from:

```text
backend/app/config.py
```

Arrow:

```text
data/19_rag_ready_documents/
        ↓
data/embeddings/drmadhupatil_vertex_embeddings.jsonl   ← ACTIVE EMBEDDING FILE
        ↓
backend/app/rag/retriever.py
```

Generated embedding files should be dated when preserved as snapshots:

```text
YYYY_MM_DD_drmadhupatil_vertex_embeddings[_status_or_version].jsonl
YYYY_MM_DD_embedding_manifest[_status_or_version].json
YYYY_MM_DD_clinic_faiss[_status_or_version].index
```

Example:

```text
2026_06_28_drmadhupatil_vertex_embeddings_doctor_approved.jsonl
2026_06_28_embedding_manifest_doctor_approved.json
2026_06_28_clinic_faiss_doctor_approved.index
```
