# Project Handoff Log - RAG Detour To Main Multi-Agent Implementation

Date: 2026-06-27  
Project: `rag-doctor-demo` / `rag-usecase-0`  
Purpose: This is the step-by-step guide to understand why this RAG demo exists, what we built, where the files are, and how the work should return to the main multi-agent implementation.

Read this file first when opening this project in a new session.

## 1. Original Mainstream Goal

The original goal was to build a GCP ADK-style multi-agent customer support system.

Main project:

```text
Multi_Agent_Customer_support_GCP_ADK/implementation/usecase-0-v2
```

Core agent architecture:

```text
user
  ↓
support_orchestrator
  ↓
triage_agent / FAQ-RAG
  ↓
ticket_agent
  ↓
escalation_agent
  ↓
web_search_agent only when needed
```

The early multi-agent system had:

- Agent routing.
- FAQ/tool layer.
- Ticket actions.
- Escalation path.
- Web search fallback.
- FastAPI layer.
- Initial RAG retrieval.

But the answer-quality layer needed stronger clinic-specific content and better prompt behavior.

## 2. Why We Took The RAG Detour

The RAG detour started because we needed a focused environment to solve three things before returning to the main multi-agent project:

1. Build a doctor-reviewable patient chat experience.
2. Improve answer quality using real clinic content.
3. Create a repeatable content improvement loop.

The detour repo:

```text
/Users/jhonny001/Desktop/rag-usecase-0
```

GitHub repo:

```text
https://github.com/Rajesh-Arigala/rag-doctor-demo
```

This repo is intentionally separate from the main multi-agent repo so we can iterate quickly without disturbing the main architecture.

## 3. What The RAG Demo Became

The demo is no longer just a basic RAG page.

It became:

```text
A 24/7 compassionate fertility companion
powered by Dr. Madhu Patil's Clinic knowledge.
```

Product role:

```text
Emotional support + clinic knowledge + safe medical boundaries
```

The assistant can:

- Educate.
- Guide.
- Reassure.
- Prepare.
- Route.
- Explain clinic services.
- Help patients become appointment-ready.

The assistant must not:

- Diagnose.
- Prescribe.
- Interpret reports.
- Guarantee pregnancy.
- Decide treatment.
- Replace the doctor.

## 4. Technical Detour Build Steps Completed

### Step 1 - Separate Demo Repo

Created a standalone demo project with:

```text
backend/
frontend/
data/
scripts/
Dockerfile
cloudbuild.yaml
```

Purpose:

- Keep the RAG demo independent.
- Deploy quickly to Cloud Run.
- Give the doctor a simple review link.

### Step 2 - Cloud Run Deployment

The demo was deployed to Google Cloud Run.

Cloud Run review URL format:

```text
https://<cloud-run-service-url>/review
```

Important note:

- Service account key creation was blocked by organization policy.
- Cloud Run was chosen because it can use attached Google Cloud identity without JSON key files.
- Public access used Cloud Run `--no-invoker-iam-check` because organization policy blocked `allUsers` IAM binding.

Deployment docs:

```text
CLOUD_RUN_DEPLOYMENT.md
```

### Step 3 - Mobile Chat UI

Created a mobile-compatible chat review page:

```text
frontend/index.html
```

Features:

- Chat bubbles.
- New chat session.
- Retry API option.
- Retry limit of 3.
- 25-turn conversation memory.
- Source/grounding proof shown below answer.

### Step 4 - Runtime Backend

Current backend entrypoint:

```text
backend/app/main.py
```

Current retrieval runtime:

```text
backend/app/rag/retriever.py
```

Current answer prompt/runtime:

```text
backend/app/rag/answering.py
```

Current curated FAQ exact-answer layer:

```text
backend/app/rag/faq.py
```

### Step 5 - Active Corpus And Embeddings

Current active corpus:

```text
data/corpus/drmadhupatil_enriched_rag_corpus.jsonl
```

Current active metadata manifest:

```text
data/corpus/metadata_enrichment_manifest.json
```

Current active embedding reference:

```text
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
```

This embedding file is the reference point:

```text
approved content
      ↓
RAG-ready documents
      ↓
data/embeddings/drmadhupatil_vertex_embeddings.jsonl
      ↓
RAG retrieval at runtime
```

### Step 6 - Prompt Engineering

Prompt engineering was separated into progress and final specs:

```text
PROMPT_ENGINEERING_PROGRESS.md
PROMPT_ENGINEERING_FINAL.md
```

Final prompt principles:

- Maximum 4 bullets.
- Icons/smileys in every bullet.
- Bold, underline, italics allowed.
- No raw website/document language.
- No internal RAG terminology.
- `Dr. Madhu Patil's Clinic` for service ownership.
- `Dr. Madhu Patil's team` only for appointment/support/hospitality.
- Safe fallback when unsure.

### Step 7 - Product Ideation

Product and business outcome thinking was documented here:

```text
PRODUCT_IDEATION_AND_BUSINESS_OUTCOMES.md
```

Core business hypothesis:

```text
The assistant should increase qualified patient inquiries and appointment intent
by improving education, trust, reassurance, and clarity.
```

Benchmark targets:

- 30 days: 100+ patient-style questions, 50+ approved Q&A.
- 60 days: 300+ questions, 150+ approved Q&A.
- Final build: 500 questions or 30-50 days, whichever comes first.

## 5. Continuous Content Improvement Structure

The repo now has a numbered content structure.

Raw doctor feedback:

```text
feedback/01_incoming_doctor_reviews/
```

Triaged questions:

```text
feedback/02_triaged_questions/
```

Doctor-approved Q&A:

```text
feedback/03_approved_clinic_qa/
```

Content lanes:

```text
data/01_source_website_corpus/
data/02_approved_qa_corpus/
data/03_public_engagement_corpus/
data/04_trust_social_proof_corpus/
data/05_patient_journey_scenarios/
data/06_consultation_guides/
data/07_treatment_decision_explainers/
data/08_myth_vs_fact/
data/09_post_treatment_followup_guidance/
data/10_emotional_support_content/
data/11_male_fertility_faqs/
data/12_age_based_fertility_planning/
data/13_safety_and_boundaries/
data/14_doctor_clinical_philosophy/
data/15_podcast_and_video_scripts/
data/16_events_webinars_workshops/
data/17_media_pr_interviews/
data/18_doctor_notes_and_clinic_protocols/
data/19_rag_ready_documents/
data/20_embeddings/
data/21_runtime/
```

Each folder has a `README.md` explaining what belongs there.

## 6. File Naming Convention

Every content file must start with the date.

Use:

```text
YYYY_MM_DD_topic_short_description[_status_or_version].md
```

Examples:

```text
2026_06_27_doctor_chat_review_initial.md
2026_06_27_approved_clinic_qa_ivf_success_doctor_approved.md
2026_06_28_patient_journey_trying_for_4_years_draft.md
2026_06_29_podcast_script_ivf_expectations_v1.md
```

Useful suffixes:

```text
_draft
_doctor_review
_doctor_approved
_needs_revision
_archived
_v1
_v2
```

## 7. Doctor Feedback Operating Plan

The doctor has been asked to use the demo chat app daily.

Target:

```text
10 Q&A per day
30-50 days
or 500 questions, whichever comes first
```

Daily file should go here:

```text
feedback/01_incoming_doctor_reviews/
```

Example:

```text
feedback/01_incoming_doctor_reviews/2026_06_28_doctor_chat_review_day_01.md
```

Recommended cadence:

```text
Daily:
Collect raw doctor Q&A files.

Every 3-5 days:
Triage questions and create approved Q&A batches.

Weekly:
Merge approved content into RAG-ready documents, rebuild embeddings, test, and redeploy if needed.
```

## 8. What To Do When New Doctor Q&A Arrives

Follow this exact sequence:

1. Save raw doctor `.md` file in:

```text
feedback/01_incoming_doctor_reviews/
```

2. Create a triage file in:

```text
feedback/02_triaged_questions/
```

3. Classify each question:

```text
approved
needs_doctor_answer
needs_rewrite
out_of_scope
medical_safety_sensitive
needs_web_search_policy
duplicate
```

4. Create approved Q&A in:

```text
feedback/03_approved_clinic_qa/
```

5. Move approved content into the correct data lane.

6. Convert approved content into RAG-ready JSONL in:

```text
data/19_rag_ready_documents/
```

7. Rebuild embeddings into:

```text
data/embeddings/
```

8. Run smoke tests.

9. Redeploy Cloud Run only if runtime files changed:

```text
backend/
frontend/
data/corpus/
data/embeddings/
Dockerfile
requirements
```

Documentation-only updates do not require Cloud Run redeployment.

## 9. Architecture And Visual References

Doctor-friendly overview:

```text
DOCTOR_README.md
```

Architecture diagrams:

```text
docs/03_ARCHITECTURE.md
```

Project map:

```text
docs/00_PROJECT_MAP.md
```

Content loop:

```text
docs/02_CONTENT_IMPROVEMENT_LOOP.md
```

Operating log:

```text
docs/01_OPERATING_LOG.md
```

## 10. How This Returns To The Main Multi-Agent System

This RAG demo should feed the main multi-agent implementation in stages.

### Stage 1 - Prompt Policy

Move the rules from:

```text
PROMPT_ENGINEERING_FINAL.md
```

into the main multi-agent FAQ/RAG agent prompt.

### Stage 2 - Corpus

Move doctor-approved Q&A and content lanes into the main RAG corpus.

Main concept:

```text
website corpus
      +
doctor-approved Q&A
      +
patient journey scenarios
      +
safety boundaries
      ↓
merged RAG corpus
      ↓
embeddings
      ↓
multi-agent triage_agent / FaqTools
```

### Stage 3 - Retrieval Policy

Main agent retrieval order should be:

```text
FAQ exact-answer layer
      ↓
metadata-filtered local RAG
      ↓
safe fallback / appointment routing
      ↓
web_search_agent only after policy gate
```

### Stage 4 - Tests

Add regression tests for:

- 4-bullet response format.
- Clinic-safe fallback.
- Service-page routing.
- Doctor-approved Q&A answers.
- Web-search blocking for clinic-owned questions.
- Web-search allowance for external/current questions.

## 11. Main Multi-Agent Target Behavior

Final desired system:

```text
patient question
      ↓
support_orchestrator
      ↓
triage_agent / clinic RAG
      ↓
local FAQ and RAG first
      ↓
appointment / ticket / escalation when needed
      ↓
web_search_agent only when local knowledge is insufficient and policy allows
```

The RAG demo gives the multi-agent system:

- Better domain knowledge.
- Real patient questions.
- Doctor-approved answers.
- Safer fallback behavior.
- Stronger prompt policy.
- Web-search gating rules.
- Business metrics and benchmarks.

## 12. Current Pause Point

As of this handoff:

- The demo is deployed and doctor-reviewable.
- The Cloud Run app is currently running.
- Current doctor review URL:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app/review
```

- Current Cloud Run base URL:

```text
https://rag-usecase-0-jatcfdo4uq-uc.a.run.app
```

- The doctor has been asked to provide daily Q&A `.md` files.
- The repo has folder structure and README files for content intake.
- Prompt engineering docs are complete.
- Product/business outcome docs are complete.
- Architecture docs are complete.
- Local repo and GitHub were confirmed aligned previously.
- Latest documentation-only changes do not require Cloud Run redeployment because they do not change `backend/`, `frontend/`, active corpus files, active embedding files, Dockerfile, or requirements.

Next action when work resumes:

```text
Process the first doctor Q&A markdown file.
```

Start with:

```text
feedback/01_incoming_doctor_reviews/
```

Then follow the content improvement loop.

## 13. Cloud Run Update Rule

Do not redeploy Cloud Run for documentation-only changes.

Redeploy only when one of these changes:

```text
backend/
frontend/
data/corpus/
data/embeddings/
Dockerfile
backend/requirements.txt
cloudbuild.yaml
scripts/deploy_cloud_run.sh
```

If approved Q&A is converted into active corpus or embeddings, then Cloud Run should be redeployed.

Smoke test command after redeploy:

```bash
./scripts/smoke_cloud_run.sh https://rag-usecase-0-jatcfdo4uq-uc.a.run.app
```

Expected result:

```text
health 200
review 200
chat 200 <doc_id> <retrieval_mode>
```

## 14. Knowledge Sync Orchestration

Weekly RAG updates should move into the main multi-agent project through an export/import bundle, not manual selective copying.

Export from this RAG demo:

```bash
scripts/run_full_knowledge_sync.sh /path/to/main/backend/knowledge/latest
```

Or step by step:

```bash
python3 scripts/export_knowledge_bundle.py
```

Import into main project destination:

```bash
python3 scripts/import_knowledge_bundle.py exports/latest /path/to/main/backend/knowledge/latest
```

Detailed guide:

```text
docs/04_KNOWLEDGE_SYNC_ORCHESTRATION.md
KNOWLEDGE_EXPORT_IMPORT_TEST_RUNBOOK.md
```

Note:

```text
exports/ is generated and ignored by git.
For production sync, make sure exports/latest/embeddings.jsonl exists before importing into the main project.
```
