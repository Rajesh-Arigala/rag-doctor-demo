# Operating Log

Use this document as the step-by-step implementation and deployment log for the doctor RAG demo.

## Current Status

- Mobile-compatible RAG chat demo is deployed on Cloud Run.
- Current review URL:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app/review
```

- Current base URL:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app
```

- Clinic assistant prompt is documented.
- Final prompt spec is documented at repo root in `PROMPT_ENGINEERING_FINAL.md`.
- Continuous content improvement folder structure has been added.
- Doctor-facing overview, architecture diagrams, product/business outcomes, and handoff log have been added.
- Documentation-only updates do not require Cloud Run redeployment.

## Current Pause Point

The project is paused while the doctor tests the live demo and sends daily `.md` chat review files.

Next expected input:

```text
feedback/01_incoming_doctor_reviews/YYYY_MM_DD_doctor_chat_review_day_N.md
```

Next expected action:

```text
Triage the doctor Q&A file, create approved clinic Q&A, then batch it into RAG-ready documents and embeddings.
```

## How To Log Future Changes

Add entries in this format:

```text
Date:
Change:
Reason:
Files changed:
Validation:
Deployment:
Open issues:
```
