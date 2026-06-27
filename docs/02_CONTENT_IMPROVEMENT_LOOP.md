# Content Improvement Loop

This is the repeatable process for improving the clinic assistant.

## Loop

```text
1. Doctor tests the demo.
2. Doctor shares chat questions and feedback as a Markdown file.
3. Save raw feedback in feedback/01_incoming_doctor_reviews/.
4. Triage questions in feedback/02_triaged_questions/.
5. Write approved Q&A in feedback/03_approved_clinic_qa/.
6. Place approved content into the matching data content lane.
7. Convert approved content into RAG-ready documents.
8. Rebuild embeddings.
9. Run smoke tests.
10. Redeploy the demo.
11. Doctor tests again.
```

## Embedding Reference Point

The active embedding target is:

```text
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
```

Everything above this file is content preparation. Everything below this file is runtime usage.

## Required File Naming Convention

Every content file should start with the creation or review date.

Use:

```text
YYYY_MM_DD_topic_short_description[_status_or_version].md
```

Examples:

```text
feedback/01_incoming_doctor_reviews/2026_06_27_doctor_chat_review_initial.md
feedback/02_triaged_questions/2026_06_27_triage_notes_initial_review.md
feedback/03_approved_clinic_qa/2026_06_27_approved_clinic_qa_ivf_success_doctor_approved.md
data/05_patient_journey_scenarios/2026_06_28_patient_journey_trying_for_4_years_draft.md
data/15_podcast_and_video_scripts/2026_06_29_podcast_script_ivf_expectations_v1.md
```

Use status suffixes when helpful:

```text
_draft
_doctor_review
_doctor_approved
_needs_revision
_archived
_v1
_v2
```

Generated files should also be dated:

```text
data/19_rag_ready_documents/2026_06_28_merged_rag_documents.jsonl
data/embeddings/2026_06_28_drmadhupatil_vertex_embeddings.jsonl
data/embeddings/2026_06_28_embedding_manifest.json
```
