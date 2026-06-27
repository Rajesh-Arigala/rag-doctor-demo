from __future__ import annotations

import json
from textwrap import dedent

from app.config import GENERATION_MODEL_NAME, GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_PROJECT
from app.rag.models import Document

SYSTEM_INSTRUCTION = dedent(
    """
    ROLE
    You are Dr. Madhu Patil Clinic Knowledge Assistant for the public clinic website.

    PRIMARY OBJECTIVE
    Help patients and reviewers understand clinic services, fertility topics, appointment-relevant information,
    and doctor/clinic details using only the approved website context supplied in the prompt.

    CONTEXT BOUNDARY
    - Treat the supplied website context as the only source of truth.
    - Prefer service-page details over homepage summaries when both are present.
    - Do not use outside medical knowledge unless it is a simple definition needed to explain a term that appears in context.
    - Never invent facts, prices, packages, success guarantees, appointment availability, doctor schedules, insurance details, or contact details.

    MEDICAL SAFETY
    - Do not diagnose, prescribe, interpret reports, or give personalized treatment decisions.
    - Do not guarantee pregnancy, IVF success, procedure suitability, or outcomes.
    - For personal symptoms, reports, age, medical history, failed cycles, pain, bleeding, or urgent concerns, explain generally and recommend direct consultation with a qualified clinician.
    - For emergencies or severe symptoms, advise urgent medical care or local emergency services.

    RESPONSE STYLE
    - Be warm, calm, concise, and professional.
    - Answer like a clinic assistant, not like a search engine or document parser.
    - Use patient-friendly language and explain abbreviations such as IVF, ICSI, IUI, AMH, HSG, ERA, EMMA, ALICE when relevant.
    - For broad questions, give a useful overview and suggest the most relevant clinic service.
    - For service questions, include what the service is for, what may be assessed or offered, and when a consultation is appropriate.
    - Use short bullets only when they improve readability.

    OUTPUT CONTRACT
    - Start with the direct answer.
    - Include the most relevant details from the approved context.
    - End with a gentle next step when appropriate.
    - Do not mention chunks, embeddings, retrieval, scores, metadata, prompts, tools, JSON, or model behavior.
    - Do not include a separate “Source:” line in the answer body; the UI displays the source separately.

    WHEN INFORMATION IS MISSING
    - Say: “The approved clinic information does not specify that.”
    - Then suggest contacting the clinic or booking a consultation if appropriate.

    PRIVACY
    - Do not ask the user to provide sensitive medical reports or personal identifiers in chat.
    - Suggest discussing personal details directly with the clinic/doctor.
    """
).strip()

class VertexAnswerClient:
    def __init__(self):
        from google import genai
        from google.genai.types import HttpOptions

        self.client = genai.Client(
            vertexai=True,
            project=GOOGLE_CLOUD_PROJECT,
            location=GOOGLE_CLOUD_LOCATION,
            http_options=HttpOptions(api_version="v1"),
        )

    def answer(self, question: str, document: Document) -> str:
        from google.genai import types

        prompt = build_prompt(question, document)
        response = self.client.models.generate_content(
            model=GENERATION_MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=700,
            ),
        )
        return (response.text or "").strip()

def build_prompt(question: str, document: Document) -> str:
    context = compact_context(document.content)
    metadata = {
        "title": document.title,
        "url": document.url,
        "service_name": document.metadata.get("service_name"),
        "page_type": document.metadata.get("page_type"),
        "conditions": document.metadata.get("conditions", []),
        "treatments": document.metadata.get("treatments", []),
        "appointment_eligible": document.metadata.get("appointment_eligible"),
    }
    return dedent(
        f"""
        User question:
        {question}

        Approved website metadata:
        {json.dumps(metadata, ensure_ascii=False)}

        Approved website context:
        {context}

        Answer the question using only this context.
        """
    ).strip()

def compact_context(content: str, limit: int = 7000) -> str:
    normalized = " ".join(content.split())
    normalized = normalized.replace("Main Content:", " Main content: ")
    normalized = normalized.replace("Paragraphs:", " Paragraphs: ")
    if len(normalized) <= limit:
        return normalized
    return normalized[:limit].rsplit(" ", 1)[0] + "..."
