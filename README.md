# RAG Usecase 0 - Doctor Review Demo

Standalone, mobile-compatible RAG demo for reviewing answer quality with a doctor. This folder is intentionally separate from `implementation/usecase-0-v2`.

When reopening this project in a new session, start here:

```text
PROJECT_HANDOFF_LOG.md
```

For a fast personal restart after a short gap, read:

```text
AUTHOR_ONE_PAGER.md
```

For a simple clinic-facing explanation of the full project and content improvement loop, read:

```text
DOCTOR_README.md
```

For product vision, metrics, benchmarks, and business outcomes, read:

```text
PRODUCT_IDEATION_AND_BUSINESS_OUTCOMES.md
```

For architecture and execution diagrams, read:

```text
docs/03_ARCHITECTURE.md
```

## Doctor Experience

Share:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app/review
```

The doctor can ask patient-style questions and see:

```text
answer
matched document
retrieval mode
filter mode
score
source URL
```

## Full RAG Path

```text
Cloud Run FastAPI backend
-> attached GCP service account
-> approved enriched clinic corpus
-> Vertex text-embedding-005 document vectors, built if missing
-> Vertex text-embedding-005 query embedding
-> metadata filters
-> hybrid retrieval
-> mobile review page
```

## Local Tests

These avoid Vertex calls:

```bash
cd rag-usecase-0/backend
RAG_USE_VERTEX=false PYTHONPATH=. pytest -p no:cacheprovider
```

## Cloud Run Deployment

Use Cloud Run because service account JSON key creation is blocked by organization policy.

```bash
cd rag-usecase-0
chmod +x scripts/deploy_cloud_run.sh scripts/smoke_cloud_run.sh
./scripts/deploy_cloud_run.sh
```

Smoke:

```bash
./scripts/smoke_cloud_run.sh https://YOUR-CLOUD-RUN-URL
```

Expected:

```text
health 200
review 200
chat 200 WEB-DRMADHU-006 hybrid_vertex
```

See `CLOUD_RUN_DEPLOYMENT.md` for details.

## Current Deployment Status

The app is currently running on Cloud Run at:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app
```

Documentation-only changes do not require redeployment.

## Security Note

The deploy script uses `--allow-unauthenticated` so the doctor can open the review link. Use this for a controlled review window. Add auth before making it a long-lived public service.
