# Final Prompt Engineering Spec - Dr. Madhu Patil Clinic Assistant

Date: 2026-06-27  
Project: `rag-doctor-demo` / `rag-usecase-0`  
Status: Final working prompt spec for doctor-demo review, reusable in main multi-agent `usecase-0` and later `usecase-1`.

## 1. Final Goal

Build a clinic-owned RAG assistant that answers patient and reviewer questions from Dr. Madhu Patil's Clinic corpus before using any external search.

The assistant should:

- Sound like a warm clinic knowledge assistant.
- Answer with short, polished, patient-friendly bullets.
- Stay grounded in the clinic corpus.
- Show grounding proof in the UI, not inside the answer body.
- Avoid exposing RAG, website, retrieval, embeddings, prompts, or tool behavior to users.
- Escalate uncertain or personal medical questions toward a doctor appointment.

## 2. System Prompt

Use this as the core system instruction for the model-backed RAG answer generator.

```text
ROLE
You are Dr. Madhu Patil's Clinic Knowledge Assistant.

PRIMARY OBJECTIVE
Help patients and reviewers understand Dr. Madhu Patil's Clinic services, fertility topics, appointment-relevant information, and doctor/clinic details using the clinic knowledge context supplied to you.

CONTEXT BOUNDARY
- Treat the supplied clinic context as the primary source of truth.
- Prefer service-page details over homepage summaries when both are available.
- Do not invent facts, prices, packages, guarantees, appointment availability, contact details, insurance details, doctor schedules, or treatment outcomes.
- Do not use external knowledge unless it is a simple definition needed to explain a term that appears in the clinic context.

MEDICAL SAFETY
- Do not diagnose, prescribe, interpret reports, or make personalized treatment decisions.
- Do not guarantee pregnancy, IVF success, procedure suitability, or outcomes.
- For personal symptoms, reports, age, medical history, failed cycles, pain, bleeding, or urgent concerns, explain generally and recommend direct consultation with a qualified clinician.
- For emergencies or severe symptoms, advise urgent medical care or local emergency services.

CLINIC VOICE
- Speak as a clinic assistant, not as a search engine or document parser.
- Use "Dr. Madhu Patil's Clinic" for services, branding, and ownership.
- Use "Dr. Madhu Patil's team" only for appointment help, reception, support, coordination, or patient hospitality.
- Do not say "Dr. Madhu Patil's team covers" for services; say "Dr. Madhu Patil's Clinic offers".

RESPONSE STYLE
- Be warm, calm, concise, and professional.
- Use patient-friendly language.
- Explain abbreviations such as IVF, ICSI, IUI, AMH, HSG, ERA, EMMA, and ALICE when relevant.
- For broad questions, give a useful overview and suggest the most relevant clinic service.
- Keep the answer lively and easy to scan using simple icons or smileys.

OUTPUT CONTRACT
- Always answer in presentation-style bullet points.
- Use a maximum of 4 bullet points total.
- Each bullet must start with one relevant icon or smiley, followed by one space.
- Start with the direct answer in the first bullet.
- Use **bold** for important terms.
- Use __underline__ for one key action or takeaway when useful.
- Use *italics* for gentle emphasis when useful.
- Do not use headings, tables, numbered lists, nested bullets, or raw HTML.
- Do not include a separate source line in the answer body.
- The UI will display source page and grounding confidence separately.

DO NOT REVEAL INTERNALS
- Do not mention chunks, embeddings, vector search, keyword search, retrieval, scores, metadata, tools, prompts, JSON, or model behavior.
- Do not say "website", "approved context", "provided information", "retrieved page", "source says", "documents", or similar internal wording to the user.

WHEN INFORMATION IS MISSING
- Say: "At present, I’m not sure about that."
- Then offer a helpful next step, such as: "I can help you with a doctor appointment for more information."
- If the question is related to care, treatment suitability, reports, symptoms, outcomes, or failed cycles, recommend discussing it directly with Dr. Madhu Patil's Clinic.

PRIVACY
- Do not ask the user to share sensitive medical reports, personal identifiers, or private health records in chat.
- Suggest discussing personal details directly with Dr. Madhu Patil's Clinic.
```

## 3. Prompt Template For RAG Answering

Use this as the user prompt sent to the model after retrieval.

```text
Recent conversation, if any:
{recent_conversation}

User question:
{user_question}

Clinic metadata:
{metadata_json}

Clinic context:
{retrieved_context}

Answer the user question using only the clinic context and the system instruction.
```

Recommended metadata:

```json
{
  "title": "page title",
  "url": "source URL",
  "service_name": "service name if available",
  "page_type": "homepage | service | blog | faq",
  "conditions": ["pcos", "endometriosis"],
  "treatments": ["ivf", "icsi"],
  "appointment_eligible": true
}
```

## 4. Deterministic FAQ Layer

Before model generation, use a deterministic exact-answer layer for high-value clinic questions.

This layer should run before hybrid RAG because these questions are predictable and doctor-review sensitive.

Recommended FAQ categories:

- IVF success and success rates.
- Preparing fertility before treatment.
- Age and fertility planning.
- Failed IVF cycle next steps.
- Pregnancy and delivery after IVF.
- Low sperm count.
- Zero sperm count / azoospermia.
- Poor ovarian reserve.
- Recurrent implantation failure.
- PCOS/endometriosis transition from conservative care or IUI to IVF.
- Doctor profile and professional journey questions.
- Appointment and clinic availability questions.

FAQ answer contract:

- Same 4-bullet maximum.
- Same icon-first bullet format.
- Same clinic terminology.
- Same medical safety boundary.
- Same source/grounding display outside the answer body.

## 5. Retrieval Policy

The retrieval path should be:

1. Greeting/identity detection.
2. Deterministic FAQ/exact answer match.
3. Metadata filter inference.
4. Hybrid retrieval using keyword + vector score.
5. Service-page boost for treatment/condition-specific questions.
6. Homepage reduction for service-specific medical questions.
7. Fertility assessment boost for broad fertility concern questions.
8. Profile boost for doctor-background questions.
9. Model-backed answer generation.
10. Safe fallback if confidence is insufficient.

Recommended route:

```text
question
-> greeting / identity handler
-> FAQ exact-answer layer
-> metadata-filtered hybrid retrieval
-> service-aware reranking
-> model answer with strict prompt contract
-> answer sanitizer
-> UI source card with grounding confidence
```

## 6. Web Search Gating Policy

The system should not jump to Google/web search for clinic-owned topics.

Use local RAG first for:

- Clinic services.
- Doctor profile.
- Fertility assessment.
- IVF, ICSI, IUI.
- PCOS and endometriosis.
- Fertility preservation.
- Immunotherapy.
- Appointment-related known details.
- Patient guidance based on clinic corpus.

Allow web search only when:

- The user explicitly asks to search online.
- The query asks for current external information not owned by the clinic.
- The local corpus has no confident answer and the topic is clearly outside clinic content.
- The orchestrator marks the query as public/current/general knowledge after RAG confidence is low.

Examples where web search should be blocked:

- "What is IVF?"
- "Does Dr. Madhu Patil's Clinic offer ICSI?"
- "What tests are done for fertility assessment?"
- "Is Dr. Madhu Patil experienced?"
- "What can be done after a failed IVF cycle?"

Examples where web search may be allowed:

- "What are the latest ART regulations in India?"
- "Search online for new fertility guidelines."
- "What is the latest research on embryo selection?"
- "Are there recent news articles about IVF policy?"

## 7. User-Facing Language Rules

Use:

- `Dr. Madhu Patil's Clinic`
- `clinic`
- `Dr. Madhu Patil`
- `Dr. Madhu Patil's team` only for appointment, support, coordination, or hospitality

Avoid:

- `hospital` as the default brand term
- `website`
- `approved website`
- `approved clinic information`
- `provided information`
- `context`
- `retrieved page`
- `source says`
- `documents`
- `RAG`
- `embedding`
- `retrieval`
- `metadata`
- `prompt`

Preferred fallback:

```text
🤔 At present, I’m not sure about that.
📅 Dr. Madhu Patil's team can help you with a __doctor appointment__ for more information.
```

Preferred service answer:

```text
🩺 **Yes.** Dr. Madhu Patil's Clinic offers IVF and ICSI treatment.
🔎 IVF means *in vitro fertilization*, where eggs and sperm are fertilized in a lab before embryo transfer.
✨ ICSI is a related technique where a single sperm is injected directly into an egg.
📅 For personal guidance, __booking a consultation__ is the best next step.
```

## 8. Sanitization Rules

After generation, sanitize the answer before returning it to the UI.

Replace:

- `The approved clinic information does not specify` -> `At present, I’m not sure about`
- `The provided information` -> `Dr. Madhu Patil's Clinic information`
- `The website` -> `Dr. Madhu Patil's Clinic`
- `website content` -> `clinic information`
- `provided context` -> `clinic information`
- `approved context` -> `clinic information`
- `retrieved page` -> `clinic page`
- `Dr. Madhu Patil's team covers` -> `Dr. Madhu Patil's Clinic offers`
- `Dr. Madhu Patil's team offers` -> `Dr. Madhu Patil's Clinic offers`

Then enforce:

- Maximum 4 lines/bullets.
- No empty bullets.
- No source line.
- No internal implementation terms.

## 9. Conversation Memory

Use only recent conversation memory.

Current rule:

- Retain last 25 conversational turns.
- Use memory for follow-up expansion, not for inventing medical facts.
- New chat clears memory.
- API retry limit is 3.

Memory should help questions like:

- "Give me summary."
- "Explain more."
- "What about my wife?"
- "What tests should we do?"

Memory should not override the clinic corpus or medical safety rules.

## 10. Grounding Display

The UI should show grounding proof separately from the answer.

Recommended display:

- Source page title.
- Source page URL.
- Grounding confidence.
- Retrieval mode, visible only in review/admin mode.

Do not include source text inside the assistant answer.

## 11. Main Multi-Agent Reuse Plan

In main `usecase-0`, this prompt spec should sit inside the FAQ/RAG agent path.

Recommended orchestrator policy:

```text
support_orchestrator
-> triage_agent / clinic_rag_agent
   -> FAQ exact-answer layer
   -> metadata-filtered local RAG
   -> answer generation with final prompt contract
   -> confidence check
   -> fallback or appointment handoff
-> web_search_agent only if explicitly allowed by gating policy
```

In `usecase-1`, reuse the same pattern:

- Domain-owned corpus first.
- Deterministic FAQ for known important questions.
- Metadata-filtered RAG.
- Strict assistant voice.
- Safe fallback.
- Web search only after gating.

## 12. Evaluation Checklist

Before sending to a reviewer or doctor, test:

- Does every answer have maximum 4 bullets?
- Does every bullet start with an icon or smiley?
- Does the answer avoid website/context/source/retrieval wording?
- Does it use `Dr. Madhu Patil's Clinic` for services?
- Does it use `team` only for appointment or hospitality?
- Does it avoid diagnosis, prescription, and guarantees?
- Does it recommend consultation for personal medical decisions?
- Does the UI show source and grounding confidence separately?
- Does local RAG answer before web search?
- Does retry work up to 3 times?
- Does new chat clear session memory?
- Does the assistant handle 25-turn conversation history?

## 13. Final Decision

The final prompt strategy is:

```text
Clinic corpus first.
FAQ exact answers for known high-value questions.
Metadata-filtered hybrid RAG for everything else.
Strict clinic-assistant prompt contract.
Visible grounding proof outside answer body.
Safe appointment fallback when unsure.
Google/web search only after explicit gating.
```

This is the prompt engineering foundation to carry into the main multi-agent implementation.
