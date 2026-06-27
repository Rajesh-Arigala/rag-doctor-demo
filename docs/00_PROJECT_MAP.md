# Project Map

This repo is organized as a clinic content pipeline that feeds the RAG demo.

## Main Arrow

```text
Doctor / clinic content
        ↓
feedback/01_incoming_doctor_reviews/
        ↓
feedback/02_triaged_questions/
        ↓
feedback/03_approved_clinic_qa/
        ↓
data/01_source_website_corpus/ through data/18_doctor_notes_and_clinic_protocols/
        ↓
data/19_rag_ready_documents/
        ↓
data/embeddings/                         ← ACTIVE EMBEDDING REFERENCE
        └── drmadhupatil_vertex_embeddings.jsonl
        ↓
backend/app/rag/retriever.py
        ↓
frontend/index.html
        ↓
doctor tests again
```

## Active Runtime References

The app currently reads these default paths from `backend/app/config.py`:

```text
Active corpus:
data/corpus/drmadhupatil_enriched_rag_corpus.jsonl

Active metadata manifest:
data/corpus/metadata_enrichment_manifest.json

Active embedding file:
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
```

`data/20_embeddings/` is the numbered planning/reference layer. `data/embeddings/` is the current active runtime path used by the app.

## Number Convention

```text
01-18 = content source lanes
19    = merged RAG-ready documents
20    = embedding/index reference layer
21    = runtime/deployment reference layer
```

## File Naming Convention

Every content file should include the date at the beginning of the filename.

Use:

```text
YYYY_MM_DD_topic_short_description[_status_or_version].md
```

Examples:

```text
2026_06_27_doctor_chat_review_initial.md
2026_06_27_approved_clinic_qa_ivf_success_doctor_approved.md
2026_06_28_patient_journey_trying_for_4_years_draft.md
2026_06_28_myth_vs_fact_ivf_twins_doctor_review.md
2026_06_29_podcast_script_ivf_expectations_v1.md
```

Machine-ready and embedding files should also be dated when generated:

```text
2026_06_28_approved_clinic_qa.jsonl
2026_06_28_merged_rag_documents.jsonl
2026_06_28_embedding_manifest.json
2026_06_28_drmadhupatil_vertex_embeddings.jsonl
```

Status suffixes:

```text
_draft
_doctor_review
_doctor_approved
_needs_revision
_archived
_v1
_v2
```
