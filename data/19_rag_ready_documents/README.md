# 19 RAG Ready Documents

Use this lane for merged machine-ready documents created from approved content lanes.

This is the staging layer before embeddings.

Current active app corpus is:

```text
data/corpus/drmadhupatil_enriched_rag_corpus.jsonl
```

Future build scripts should merge approved lane content into a RAG-ready JSONL here, then update the active corpus path or copy the approved merged corpus to `data/corpus/`.

Filename rule:

```text
YYYY_MM_DD_merged_rag_documents[_status_or_version].jsonl
```

Example:

```text
2026_06_28_merged_rag_documents_doctor_approved.jsonl
```
