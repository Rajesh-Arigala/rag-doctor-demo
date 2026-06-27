# Prompt Engineering Progress - Dr. Madhu Patil Clinic Assistant

Date: 2026-06-27  
Project: `rag-doctor-demo` / `rag-usecase-0`  
Purpose: Track the prompt engineering decisions, iterations, failures, and final direction for the Dr. Madhu Patil Clinic RAG demo. This document is intended to become reusable guidance for the main multi-agent `usecase-0` and later `usecase-1` builds.

## 1. Why This Document Exists

The first working demo proved that retrieval, metadata filtering, Vertex embeddings, and Cloud Run deployment were functional. The next challenge was not only technical retrieval quality; it was answer quality.

The assistant must feel like a clinic-facing knowledge assistant, not a raw document viewer. It should:

- Answer from the prepared clinic corpus before any web search.
- Sound warm, concise, and patient-friendly.
- Avoid exposing internal implementation language.
- Stay medically safe and avoid diagnosis, prescription, or guarantees.
- Provide visible grounding proof through source and confidence score.
- Be reusable as a prompt pattern in the main multi-agent architecture.

## 2. Current Product Intent

The current demo is a doctor-reviewable chat assistant for Dr. Madhu Patil's Clinic.

It should help patients and reviewers ask questions about:

- Fertility assessment.
- IVF, ICSI, and IUI.
- PCOS and endometriosis-related infertility.
- Fertility preservation.
- Immunotherapy in infertility.
- Appointment and clinic-related details.
- Doctor profile and experience.

The assistant should not behave like a general medical chatbot. It is a grounded clinic knowledge assistant.

## 3. Prompt Engineering Timeline

### v1 - Retrieval Review Page

Initial demo behavior:

- User entered a question in a text box.
- Backend returned top retrieved document content.
- UI displayed source, document id, mode, and score.

Issues found:

- Answers looked like raw scraped website text.
- Headings, metadata, and document fragments appeared in responses.
- The experience felt like a retrieval debugger, not a clinic assistant.
- Not suitable to send to the doctor for review.

### v2 - Chat Experience

Improvement:

- Converted the UI into a proper chat-style review experience.
- Added assistant and user message bubbles.
- Added mobile-compatible layout.
- Added source card below assistant responses.

Remaining issues:

- The assistant could still sound like it was reading from documents.
- Some answers were too long.
- Some responses exposed implementation phrasing.
- Follow-up behavior needed memory.

### v3 - Clinic Assistant Persona

Prompt direction changed from "RAG answer generator" to "clinic knowledge assistant".

Key decisions:

- Use the voice of `Dr. Madhu Patil's Clinic`.
- Use `Dr. Madhu Patil's Clinic offers...` for services.
- Use `Dr. Madhu Patil's team...` only for appointment, hospitality, reception, support, or coordination.
- Avoid saying `website`, `approved content`, `retrieved context`, `provided information`, or similar phrases to the patient.

Reason:

The patient should feel they are interacting with the clinic assistant, not with a document-processing system.

### v4 - System Instruction Structure

The prompt was organized into clear sections:

- `ROLE`
- `PRIMARY OBJECTIVE`
- `CONTEXT BOUNDARY`
- `MEDICAL SAFETY`
- `RESPONSE STYLE`
- `OUTPUT CONTRACT`
- `WHEN INFORMATION IS MISSING`
- `PRIVACY`

This structure made the prompt easier to maintain and easier to transfer into the main multi-agent project.

### v5 - Output Contract

After testing, the output style was constrained heavily.

Current rules:

- Maximum 4 bullet points.
- Every bullet starts with an icon or smiley.
- First bullet gives the direct answer.
- Use `**bold**` for important terms.
- Use `__underline__` for one key action or takeaway.
- Use `*italics*` for gentle emphasis when useful.
- No tables.
- No numbered lists.
- No nested bullets.
- No headings.
- No raw HTML.
- No separate source line inside the answer body.

Reason:

Doctor-review and patient-facing answers need to be short, attractive, and easy to scan on mobile.

### v6 - Missing Information Policy

Old bad behavior:

- "The approved clinic information does not specify..."
- "The provided information..."
- "The website says..."

Final patient-facing fallback:

> At present, I’m not sure about that. I can help you with a doctor appointment for more information.

This keeps the assistant honest without exposing internal RAG mechanics.

### v7 - Conversation Controls

Added interaction-level prompt support:

- 25 conversational turns retained.
- New chat option clears visible messages and local memory.
- Retry API option added.
- Retry limit set to 3.
- Follow-up questions are expanded using recent chat context.

Reason:

The assistant should support normal chat flow while avoiding uncontrolled long-session drift.

### v8 - Grounding Proof

The UI displays grounding proof outside the answer body:

- Source page title.
- Source URL.
- Grounding confidence score.
- Retrieval mode.

The assistant itself must not mention retrieval, embeddings, scores, chunks, tools, or metadata.

Reason:

Reviewers and doctors need proof of grounding, but patients do not need implementation details in the answer.

### v9 - FAQ / Exact Answer Layer

Some important doctor-review questions were repeatedly asked and should not depend only on semantic retrieval.

Added deterministic FAQ answers before generative RAG for questions such as:

- How successful is IVF?
- What can I do to improve fertility before treatment?
- At what age should I start thinking about fertility?
- What can be done after a failed IVF cycle?
- Will I have a normal pregnancy and delivery after IVF?
- Treatment options for men with low sperm count.
- Treatment options for men with zero sperm count.
- Recurrent implantation failure.
- Poor ovarian reserve.
- PCOS/endometriosis transition from IUI or conservative treatment to IVF.
- Professional/interview-style doctor profile questions.

Reason:

For high-value clinic questions, deterministic answers improve consistency, reduce hallucination risk, and reduce unnecessary web search.

## 4. Current Prompt Contract

### Role

The assistant is `Dr. Madhu Patil's Clinic Knowledge Assistant`.

### Objective

Help users understand clinic services, fertility topics, appointment-relevant information, and doctor/clinic details using the clinic corpus first.

### Context Boundary

The assistant should use the prepared clinic content as the primary source of truth. It should not invent:

- Prices.
- Packages.
- Guarantees.
- Appointment slots beyond known schedule text.
- Insurance details.
- Doctor availability not present in the corpus.
- Personalized treatment recommendations.

### Medical Safety

The assistant must not:

- Diagnose.
- Prescribe.
- Interpret reports.
- Guarantee pregnancy or IVF success.
- Decide treatment suitability for a patient.

For symptoms, reports, failed cycles, urgent problems, or personal treatment choices, it should recommend direct consultation.

### Style

The assistant should be:

- Warm.
- Calm.
- Crisp.
- Patient-friendly.
- Mobile-readable.
- Presentation-style.

### Missing Information

The assistant should say:

- `At present, I’m not sure about that.`
- Then guide toward a doctor appointment or direct clinic consultation.

It should not say:

- `website`
- `provided information`
- `approved context`
- `retrieved page`
- `source`
- `documents`

## 5. Current User-Facing Language Rules

Use:

- `Dr. Madhu Patil's Clinic`
- `clinic`
- `Dr. Madhu Patil`
- `Dr. Madhu Patil's team` only for appointment or hospitality support

Avoid:

- `hospital` as the primary brand term
- `Dr. Madhu Patil's team covers`
- `approved clinic information`
- `provided information`
- `website content`
- `retrieved context`
- `source says`

Preferred service phrasing:

- `Dr. Madhu Patil's Clinic offers IVF and ICSI treatment.`

Preferred appointment phrasing:

- `Dr. Madhu Patil's team can help you with an appointment.`

## 6. Current Retrieval and Prompt Flow

Current answer flow:

1. Detect greetings and identity questions.
2. Check deterministic FAQ / exact answer layer.
3. Infer metadata filters from the question.
4. Run hybrid retrieval with keyword + vector scoring.
5. Apply service, fertility assessment, prep, and profile boosts.
6. Use Vertex generation when enabled.
7. Sanitize final answer.
8. Display source and grounding proof separately in the UI.

This creates a layered path:

`FAQ exact answer -> metadata-filtered RAG -> fallback -> web search only later if explicitly allowed`

## 7. Web Search Limiting Strategy

The final multi-agent system should not jump to Google/web search for clinic questions.

Recommended policy:

- First use structured FAQ and exact answers.
- Then use metadata-filtered local RAG.
- Then use hybrid retrieval with service-page preference.
- Then ask a safe follow-up or recommend appointment if confidence is low.
- Use web search only when the user explicitly asks for public/current information or when the local corpus is insufficient and the query is clearly outside clinic-owned content.

Examples where web search should not be used:

- What is IVF?
- Does the clinic offer ICSI?
- What tests are done for fertility assessment?
- What is Dr. Madhu Patil's experience?
- What can be done after failed IVF?

Examples where web search may be allowed later:

- Latest government fertility regulation.
- Current insurance coverage rules.
- Latest city-wide clinic timings not in corpus.
- New external research or news.
- Explicit user request: "search online".

## 8. Current Known Test Coverage

The prompt and answer behavior has been tested against:

- Identity questions: `who are you`, `why are you here`.
- Clinic profile: speciality, experience, patient count.
- Patient-style questions: trying to conceive for 4 years, fertility tests, appointment availability.
- Trust questions: `is she good?`, prior bad hospital experience.
- Family/hospitality questions: coming with in-laws.
- Doctor-review questions about infertility trends, counselling expectations, poor ovarian reserve, RIF, PCOS/endometriosis transition.
- FAQ questions about IVF success, fertility preparation, failed IVF, pregnancy after IVF, low sperm count, and zero sperm count.

Current desired output for all of these:

- Maximum 4 icon bullets.
- No internal RAG terminology.
- Source proof shown only in the UI card.
- Safe appointment handoff when details are missing.

## 9. Issues Already Identified and Addressed

Addressed:

- Raw scraped text in answers.
- Homepage winning over service pages for PCOS/endometriosis.
- Overuse of `team` for service ownership.
- Mentioning website/context/provided information to users.
- Long paragraph answers.
- Missing retry behavior.
- Missing new chat behavior.
- Missing conversation memory.
- Lack of deterministic answers for repeated high-value FAQ questions.
- Source and score mixed into answer body.

## 10. Open Items Before Final Prompt Consolidation

Recommended next improvements:

- Add prompt version metadata in API responses for audit.
- Add a formal answer evaluation rubric.
- Add a regression test set for the 25-30 doctor-review questions.
- Convert hand-curated FAQ patterns into a maintained clinic FAQ registry.
- Add confidence bands for source display, such as high/medium/low.
- Add an explicit web-search gating policy in the main orchestrator.
- Add a separate internal developer prompt and external patient prompt boundary.
- Add doctor-review mode vs patient mode if the doctor wants more technical detail.

## 11. Final Consolidated Prompt Artifact Plan

The final prompt engineering artifact should include:

- System prompt.
- Developer/tool instruction prompt.
- Retrieval policy.
- Metadata filtering policy.
- FAQ exact-answer policy.
- Reranking and service-page preference policy.
- Response format contract.
- Medical safety contract.
- Missing-information fallback policy.
- Appointment handoff policy.
- Web-search gating policy.
- Evaluation checklist.
- Test question set.

This final artifact should then be copied into:

- Main multi-agent `usecase-0`.
- Later `usecase-1`.
- The web search agent routing policy, so web search is limited and only used after local RAG confidence is insufficient.

## 12. Current Decision

The prompt strategy is no longer just "answer from RAG".

The working strategy is:

> Clinic-owned corpus first, deterministic FAQ where possible, metadata-filtered hybrid RAG next, safe fallback when uncertain, and web search only after explicit gating.

This is the direction to preserve for the main multi-agent implementation.
