from __future__ import annotations

from app.config import RAG_USE_GENERATION
from app.rag.answering import VertexAnswerClient, sanitize_answer
from app.rag.embeddings import HashEmbeddingClient, VertexEmbeddingClient, cosine
from app.rag.faq import find_faq_answer
from app.rag.loader import save_vectors
from app.rag.models import Document, RetrievalHit
from app.rag.text import terms, tokenize

CONDITION_TERMS = {"pcos": "pcos", "endometriosis": "endometriosis", "irregular periods": "irregular periods", "hormonal": "hormonal issues", "hormonal issues": "hormonal issues", "infertility": "infertility"}
TREATMENT_TERMS = {"ivf": "ivf", "icsi": "icsi", "iui": "iui", "fertility preservation": "fertility preservation", "egg freezing": "egg freezing", "sperm freezing": "sperm freezing", "embryo freezing": "embryo freezing", "fertility assessment": "fertility assessment", "fertility issue": "fertility assessment", "fertility issues": "fertility assessment", "issue with fertility": "fertility assessment", "immunotherapy": "immunotherapy"}
APPOINTMENT_TERMS = {"appointment", "book", "consult", "consultation", "schedule", "visit"}
PREP_TERMS = {"prepare", "preparation", "before visit", "before visiting", "before appointment", "first visit", "what should i bring", "what prep", "visit doctor"}
PROFILE_TERMS = {"experience", "clinical work", "obstetrics", "gynecology", "reproductive medicine", "drew you", "focused area", "practice", "doctor profile", "professional journey", "achievements"}
BROAD_FERTILITY_TERMS = {"fertility", "infertility", "fertility issue", "fertility issues", "issue with fertility"}
FOLLOWUP_TERMS = {"summary", "summarize", "short", "brief", "more", "more detail", "details", "explain simply", "simplify", "continue"}
IDENTITY_TERMS = {"who are you", "why are you here", "what do you do", "where do you work"}
GREETING_TERMS = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening"}
DEFINITION_TERMS = {"what", "what is", "explain", "meaning", "define", "tell me about"}
TREATMENT_DEFINITIONS = {
    "ivf": "IVF, or in vitro fertilization, is a fertility treatment where eggs are fertilized with sperm outside the body in a laboratory. A suitable embryo may then be transferred into the uterus.",
    "icsi": "ICSI, or intracytoplasmic sperm injection, is an IVF-related technique where a single sperm is injected directly into an egg in the laboratory.",
    "iui": "IUI, or intrauterine insemination, is a fertility treatment where prepared sperm is placed directly into the uterus around ovulation.",
    "fertility preservation": "Fertility preservation means saving eggs, sperm, or embryos for possible future pregnancy planning.",
}

class RagRetriever:
    def __init__(self, documents: list[Document], vectors: dict[str, list[float]], embeddings_path, use_vertex: bool = True):
        self.documents = documents
        self.use_vertex = use_vertex
        self.embedding_client = VertexEmbeddingClient() if use_vertex else HashEmbeddingClient()
        self.answer_client = VertexAnswerClient() if use_vertex and RAG_USE_GENERATION else None
        self.vectors = vectors
        missing = [document for document in documents if document.doc_id not in self.vectors]
        if missing:
            self.vectors.update(self.embedding_client.embed_documents(missing))
            save_vectors(embeddings_path, self.vectors)

    def answer(self, question: str, history: list[dict] | None = None) -> dict:
        history = history or []
        if is_greeting(question):
            return {
                "status": "success",
                "answer": "👋 **Hello!** I can help with IVF, ICSI, IUI, PCOS, endometriosis, fertility preservation, and appointments.\n🩺 Tell me what you’d like to know, and I’ll keep it crisp.",
                "retrieval": {},
            }

        if is_identity_question(question):
            return {
                "status": "success",
                "answer": "👋 **I’m Dr. Madhu Patil’s Clinic assistant.**\n✨ I help with clinic services, fertility topics, appointments, and general patient questions.\n🩺 I keep answers short, clear, and grounded in clinic information.\n📅 If you need personal guidance, Dr. Madhu Patil’s team can help with an appointment.",
                "retrieval": {},
            }
        faq = find_faq_answer(question)
        if faq is not None:
            answer, doc_id = faq
            document = self.document_by_id(doc_id)
            return {"status": "success", "answer": sanitize_answer(answer), "retrieval": hit_payload_for_document(document, "faq_exact") if document else {}}

        search_question = expand_followup_question(question, history)
        hit = self.search(search_question)
        if hit is None:
            return {
                "status": "not_found",
                "answer": "🤔 At present, I’m not sure about that.\n📅 Dr. Madhu Patil’s team can help you with a __doctor appointment__ for more information.",
                "retrieval": {},
            }
        return {"status": "success", "answer": self.compose_answer(question, hit.document, history), "retrieval": hit_payload(hit)}

    def document_by_id(self, doc_id: str) -> Document | None:
        for document in self.documents:
            if document.doc_id == doc_id:
                return document
        return None

    def compose_answer(self, question: str, document: Document, history: list[dict] | None = None) -> str:
        if self.answer_client is None:
            return format_answer(document, question)
        try:
            answer = self.answer_client.answer(question, document, history or [])
        except Exception:
            answer = ""
        return sanitize_answer(answer or format_answer(document, question))

    def search(self, question: str) -> RetrievalHit | None:
        filters = infer_filters(question)
        hit = self._search(question, filters, "metadata" if filters else "none")
        if hit is not None:
            return hit
        if filters:
            return self._search(question, {}, "metadata_fallback_unfiltered")
        return None

    def _search(self, question: str, filters: dict[str, object], filter_mode: str) -> RetrievalHit | None:
        query_terms = terms(question)
        query_vector = self.embedding_client.embed_query(question)
        best = None
        for document in [doc for doc in self.documents if matches_filters(doc, filters)]:
            keyword_score = keyword_overlap(query_terms, document)
            vector_score = cosine(query_vector, self.vectors.get(document.doc_id, []))
            score = min((0.55 * keyword_score) + (0.45 * vector_score) + title_boost(query_terms, document), 1.0)
            score = apply_service_boost(question, document, score)
            score = apply_broad_fertility_boost(question, document, score)
            score = apply_prep_boost(question, document, score)
            score = apply_profile_boost(question, document, score)
            if score < 0.35:
                continue
            hit = RetrievalHit(document, score, keyword_score, vector_score, filter_mode, "hybrid_vertex" if self.use_vertex else "hybrid_hash")
            if best is None or hit.score > best.score:
                best = hit
        return best

def infer_filters(question: str) -> dict[str, object]:
    query_terms = terms(question)
    filters = {}
    conditions = sorted({value for term, value in CONDITION_TERMS.items() if term in query_terms})
    treatments = sorted({value for term, value in TREATMENT_TERMS.items() if term in query_terms})
    if conditions:
        filters["conditions"] = conditions
    if treatments:
        filters["treatments"] = treatments
    if query_terms.intersection(APPOINTMENT_TERMS):
        filters["appointment_eligible"] = True
    if query_terms.intersection(PREP_TERMS):
        filters["appointment_eligible"] = True
    return filters

def matches_filters(document: Document, filters: dict[str, object]) -> bool:
    return all(value_matches(document.metadata.get(key), expected) for key, expected in filters.items())

def value_matches(candidate, expected) -> bool:
    if isinstance(expected, (list, tuple, set)):
        return any(value_matches(candidate, item) for item in expected)
    if isinstance(candidate, (list, tuple, set)):
        return any(str(item).lower() == str(expected).lower() for item in candidate)
    return str(candidate).lower() == str(expected).lower()

def keyword_overlap(query_terms: set[str], document: Document) -> float:
    document_terms = terms(document.searchable_text)
    return len(query_terms.intersection(document_terms)) / len(query_terms) if query_terms else 0.0

def title_boost(query_terms: set[str], document: Document) -> float:
    title_terms = set(tokenize(document.title))
    return 0.25 * (len(query_terms.intersection(title_terms)) / len(query_terms)) if query_terms else 0.0

def apply_service_boost(question: str, document: Document, score: float) -> float:
    query_terms = terms(question)
    service_terms = set(document.metadata.get("conditions", [])).union(set(document.metadata.get("treatments", [])))
    if query_terms.intersection(service_terms) and document.metadata.get("page_type") == "service":
        score += 0.12
    if document.metadata.get("page_type") == "homepage" and query_terms.intersection(service_terms):
        score -= 0.12
    return max(min(score, 1.0), 0.0)

def apply_broad_fertility_boost(question: str, document: Document, score: float) -> float:
    query_terms = terms(question)
    service_name = str(document.metadata.get("service_name") or "").lower()
    treatments = set(document.metadata.get("treatments", []))
    if query_terms.intersection(BROAD_FERTILITY_TERMS) and ("fertility assessment" in treatments or service_name == "fertility assessment"):
        score += 0.28
        if document.metadata.get("page_type") == "homepage":
            score -= 0.22
    return max(min(score, 1.0), 0.0)

def apply_prep_boost(question: str, document: Document, score: float) -> float:
    query_terms = terms(question)
    service_name = str(document.metadata.get("service_name") or "").lower()
    if query_terms.intersection(PREP_TERMS) and service_name == "fertility assessment":
        score += 0.35
    return max(min(score, 1.0), 0.0)

def apply_profile_boost(question: str, document: Document, score: float) -> float:
    query_terms = terms(question)
    if query_terms.intersection(PROFILE_TERMS):
        if document.metadata.get("page_type") == "homepage":
            score += 0.24
        elif document.metadata.get("page_type") == "service":
            score -= 0.08
    return max(min(score, 1.0), 0.0)

def format_answer(document: Document, question: str = "") -> str:
    metadata = document.metadata or {}
    page_type = str(metadata.get("page_type") or "").lower()
    service_name = str(metadata.get("service_name") or document.title).strip()
    treatments = listify(metadata.get("treatments"))
    conditions = listify(metadata.get("conditions"))
    appointment_eligible = bool(metadata.get("appointment_eligible"))

    if page_type == "service":
        definition = treatment_definition_for(question, treatments)
        focus_parts = []
        if treatments:
            focus_parts.append("treatments such as " + readable_list(treatments[:4]))
        if conditions:
            focus_parts.append("conditions such as " + readable_list(conditions[:4]))
        focus = " and ".join(focus_parts) if focus_parts else "this fertility care topic"
        if definition:
            lines = [
                f"💡 {definition}",
                f"🩺 **Dr. Madhu Patil’s Clinic** offers {service_name}.",
                f"🔎 This is relevant to {focus}.",
            ]
        else:
            lines = [
                f"🩺 **Yes.** Dr. Madhu Patil’s Clinic offers {service_name}.",
                f"🔎 This is relevant to {focus}.",
            ]
        if appointment_eligible:
            lines.append("📅 For personal guidance, __booking a consultation__ is the best next step.")
        else:
            lines.append("📅 For personal medical advice, please discuss directly with Dr. Madhu Patil's Clinic.")
        return "\n".join(lines[:4])

    lines = [
        "ℹ️ **Dr. Madhu Patil’s Clinic** provides gynecology and fertility care across routine women’s health and advanced fertility services.",
        "🩺 Dr. Madhu Patil is described as a Gynecologist and IVF Specialist with 13+ years in obstetrics and gynecology and 9+ years in infertility and ART.",
        "🌟 The clinic highlights fertility assessment, IVF/ICSI, IUI, fertility preservation, PCOS/endometriosis care, and immunotherapy in infertility.",
        "📅 For personal guidance, __booking a consultation__ is the best next step.",
    ]
    return "\n".join(lines[:4])

def expand_followup_question(question: str, history: list[dict]) -> str:
    query_terms = terms(question)
    if not query_terms.intersection(FOLLOWUP_TERMS):
        return question
    for item in reversed(history[-25:]):
        content = str(item.get("content", "")).strip()
        if content and str(item.get("role", "")).lower() in {"assistant", "user"}:
            return f"{question} Previous topic: {content[:500]}"
    return question

def is_identity_question(question: str) -> bool:
    stripped = question.strip().lower().rstrip("?.!")
    query_terms = terms(question)
    if stripped in IDENTITY_TERMS:
        return True
    return bool(query_terms.intersection(IDENTITY_TERMS))

def is_greeting(question: str) -> bool:
    query_terms = terms(question)
    stripped = question.strip().lower()
    return stripped in GREETING_TERMS or bool(query_terms.intersection(GREETING_TERMS)) and len(query_terms) <= 3

def treatment_definition_for(question: str, treatments: list[str]) -> str:
    query_terms = terms(question)
    if not query_terms.intersection(DEFINITION_TERMS):
        return ""
    treatment_terms = set(treatments).intersection(TREATMENT_DEFINITIONS)
    requested_terms = query_terms.intersection(TREATMENT_DEFINITIONS)
    for term in sorted(requested_terms.union(treatment_terms)):
        if term in query_terms:
            return TREATMENT_DEFINITIONS[term]
    return ""

def listify(value) -> list[str]:
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    if value:
        return [str(value).strip()]
    return []

def readable_list(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f", and {items[-1]}"

def clean_snippet(content: str, limit: int = 420) -> str:
    snippet = " ".join(content.split())
    prefixes = ["Title:", "Source URL:", "Headings:"]
    for prefix in prefixes:
        snippet = snippet.replace(prefix, "")
    if len(snippet) > limit:
        snippet = snippet[:limit].rsplit(" ", 1)[0] + "..."
    return snippet.strip()

def hit_payload(hit: RetrievalHit) -> dict:
    return {"doc_id": hit.document.doc_id, "title": hit.document.title, "url": hit.document.url, "score": round(hit.score, 4), "keyword_score": round(hit.keyword_score, 4), "vector_score": round(hit.vector_score, 4), "mode": hit.mode, "filter_mode": hit.filter_mode, "metadata": hit.document.metadata}

def hit_payload_for_document(document: Document | None, mode: str) -> dict:
    if document is None:
        return {}
    return {"doc_id": document.doc_id, "title": document.title, "url": document.url, "score": 1.0, "keyword_score": 1.0, "vector_score": 1.0, "mode": mode, "filter_mode": "faq", "metadata": document.metadata}
