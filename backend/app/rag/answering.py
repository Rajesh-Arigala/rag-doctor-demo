from __future__ import annotations

import json
from textwrap import dedent

from app.config import GENERATION_MODEL_NAME, GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_PROJECT
from app.rag.models import Document

SYSTEM_INSTRUCTION = dedent(
    """
    ROLE
    You are Dr. Madhu Patil's Clinic Knowledge Assistant for the public clinic website.

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
    - For service questions, say Dr. Madhu Patil's Clinic offers the relevant service.
    - Use “Dr. Madhu Patil’s team” only for patient hospitality, appointment help, reception, support, or coordination.
    - For service ownership, do not say “Dr. Madhu Patil’s team covers”; say “Dr. Madhu Patil’s Clinic offers”.
    - Keep the answer lively and easy to scan using simple icons, smileys, and crisp presentation-style phrasing.

    OUTPUT CONTRACT
    - Always answer in presentation-style bullet points.
    - Use a maximum of 4 bullet points total.
    - Each bullet must start with one relevant icon or smiley, followed by one space, then the answer text.
    - Use **bold** for important terms, __underline__ for one key action or takeaway, and *italics* for gentle emphasis when useful.
    - Do not use headings, tables, numbered lists, nested bullets, or raw HTML.
    - Start with the direct answer in the first bullet.
    - Include only the most relevant details from the approved context.
    - End with a gentle next step when appropriate.
    - Do not mention chunks, embeddings, retrieval, scores, metadata, prompts, tools, JSON, or model behavior.
    - Do not include a separate “Source:” line in the answer body; the UI displays the source separately.
    - Never tell the user that you are limited by website content, approved context, documents, retrieved pages, provided information, or available information.
    - Never use phrases such as “the website says”, “the provided information”, “the context”, or “the source”.

    WHEN INFORMATION IS MISSING
    - Do not say “approved clinic information”, “website content”, “context”, “source”, or similar internal wording to the user.
    - Say: “At present, I’m not sure about that.”
    - Then offer a helpful next step, such as: “I can help you with a doctor appointment for more information.”
    - If the question is related to care, treatment suitability, reports, symptoms, or outcomes, recommend discussing it directly with Dr. Madhu Patil's Clinic.

    PRIVACY
    - Do not ask the user to provide sensitive medical reports or personal identifiers in chat.
    - Suggest discussing personal details directly with Dr. Madhu Patil's Clinic.
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

    def answer(self, question: str, document: Document, history: list[dict] | None = None) -> str:
        from google.genai import types

        prompt = build_prompt(question, document, history or [])
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
        return sanitize_answer(response.text or "")

def build_prompt(question: str, document: Document, history: list[dict] | None = None) -> str:
    context = compact_context(document.content)
    recent_history = compact_history(history or [])
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
        Recent conversation, if any:
        {recent_history}

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


def compact_history(history: list[dict], limit: int = 3000) -> str:
    if not history:
        return "No prior conversation."
    rows = []
    for item in history[-25:]:
        role = str(item.get("role", "user"))[:12]
        content = " ".join(str(item.get("content", "")).split())
        if content:
            rows.append(f"{role}: {content[:360]}")
    value = "\n".join(rows) or "No prior conversation."
    if len(value) > limit:
        return value[-limit:]
    return value


def sanitize_answer(answer: str) -> str:
    value = " ".join(str(answer or "").split())
    replacements = {
        "The approved clinic information does not specify": "At present, I’m not sure about",
        "the approved clinic information does not specify": "at present, I’m not sure about",
        "The provided information": "Dr. Madhu Patil’s Clinic information",
        "the provided information": "Dr. Madhu Patil’s Clinic information",
        "The website": "Dr. Madhu Patil’s Clinic",
        "the website": "Dr. Madhu Patil’s Clinic",
        "website content": "clinic information",
        "provided context": "clinic information",
        "approved context": "clinic information",
        "retrieved page": "clinic page",
        "retrieved pages": "clinic pages",
        "Dr. Madhu Patil's team covers": "Dr. Madhu Patil’s Clinic offers",
        "Dr. Madhu Patil’s team covers": "Dr. Madhu Patil’s Clinic offers",
        "Dr. Madhu Patil's team offers": "Dr. Madhu Patil’s Clinic offers",
        "Dr. Madhu Patil’s team offers": "Dr. Madhu Patil’s Clinic offers",
        "Dr. Madhu Patil's team can provide personalized": "Dr. Madhu Patil’s Clinic can provide personalized",
        "Dr. Madhu Patil’s team can provide personalized": "Dr. Madhu Patil’s Clinic can provide personalized",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = split_icon_bullets(value)
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    if not lines:
        return "🤔 At present, I’m not sure about that.\n📅 Dr. Madhu Patil’s team can help you with a __doctor appointment__ for more information."
    return "\n".join(lines[:4])

def split_icon_bullets(value: str) -> str:
    icons = ["💖", "✨", "🩺", "📅", "📞", "😊", "🌟", "🔎", "💡", "👋", "🤔", "☀️"]
    for icon in icons:
        value = value.replace(f" {icon} ", f"\n{icon} ")
    return value.strip()
