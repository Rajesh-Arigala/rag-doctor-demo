# Active Embeddings

This is the active embedding folder used by the running app.

Primary reference file:

```text
drmadhupatil_vertex_embeddings.jsonl
```

This is the key reference point for the full content loop:

```text
approved content
      ↓
RAG-ready documents
      ↓
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
      ↓
RAG retrieval at runtime
```

If this file does not exist locally, it is generated when the app/retriever builds embeddings using the configured embedding client.

When preserving embedding snapshots, use dated filenames:

```text
YYYY_MM_DD_drmadhupatil_vertex_embeddings[_status_or_version].jsonl
YYYY_MM_DD_embedding_manifest[_status_or_version].json
YYYY_MM_DD_clinic_faiss[_status_or_version].index
```
