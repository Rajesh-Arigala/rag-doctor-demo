from __future__ import annotations

from app.rag.embeddings import HashEmbeddingClient, VertexEmbeddingClient, cosine
from app.rag.loader import save_vectors
from app.rag.models import Document, RetrievalHit
from app.rag.text import terms, tokenize

CONDITION_TERMS = {"pcos": "pcos", "endometriosis": "endometriosis", "irregular periods": "irregular periods", "hormonal": "hormonal issues", "hormonal issues": "hormonal issues"}
TREATMENT_TERMS = {"ivf": "ivf", "icsi": "icsi", "iui": "iui", "fertility preservation": "fertility preservation", "egg freezing": "egg freezing", "sperm freezing": "sperm freezing", "embryo freezing": "embryo freezing", "fertility assessment": "fertility assessment", "immunotherapy": "immunotherapy"}
APPOINTMENT_TERMS = {"appointment", "book", "consult", "consultation", "schedule", "visit"}

class RagRetriever:
    def __init__(self, documents: list[Document], vectors: dict[str, list[float]], embeddings_path, use_vertex: bool = True):
        self.documents = documents
        self.use_vertex = use_vertex
        self.embedding_client = VertexEmbeddingClient() if use_vertex else HashEmbeddingClient()
        self.vectors = vectors
        missing = [document for document in documents if document.doc_id not in self.vectors]
        if missing:
            self.vectors.update(self.embedding_client.embed_documents(missing))
            save_vectors(embeddings_path, self.vectors)

    def answer(self, question: str) -> dict:
        hit = self.search(question)
        if hit is None:
            return {
                "status": "not_found",
                "answer": "I could not find a confident answer in the approved clinic knowledge base. Please contact the clinic directly for guidance.",
                "retrieval": {},
            }
        return {"status": "success", "answer": format_answer(hit.document, question), "retrieval": hit_payload(hit)}

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

def format_answer(document: Document, question: str = "") -> str:
    metadata = document.metadata or {}
    page_type = str(metadata.get("page_type") or "").lower()
    service_name = str(metadata.get("service_name") or document.title).strip()
    treatments = listify(metadata.get("treatments"))
    conditions = listify(metadata.get("conditions"))
    appointment_eligible = bool(metadata.get("appointment_eligible"))

    if page_type == "service":
        focus_parts = []
        if treatments:
            focus_parts.append("treatments such as " + readable_list(treatments[:4]))
        if conditions:
            focus_parts.append("conditions such as " + readable_list(conditions[:4]))
        focus = " and ".join(focus_parts) if focus_parts else "this fertility care topic"
        lines = [
            f"Yes. Based on the clinic information, Dr. Madhu Patil's team covers {service_name}.",
            f"This page is relevant to {focus}.",
        ]
        if appointment_eligible:
            lines.append("For a personal recommendation, the safest next step is to book a consultation so the doctor can review history, reports, and goals.")
        else:
            lines.append("For personal medical advice, the clinic should review the patient's history and reports directly.")
        if document.url:
            lines.append(f"Source: {document.url}")
        return "\n\n".join(lines)

    snippet = clean_snippet(document.content, 420)
    lines = [
        "I found a relevant clinic page, but it is a broader overview rather than a specific service page.",
        snippet,
    ]
    if document.url:
        lines.append(f"Source: {document.url}")
    return "\n\n".join(lines)

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
