from pathlib import Path

from app.config import CORPUS_PATH, METADATA_MANIFEST_PATH
from app.rag.loader import load_documents, load_manifest
from app.rag.retriever import infer_filters, matches_filters


def test_demo_artifacts_exist():
    assert CORPUS_PATH.exists()
    assert METADATA_MANIFEST_PATH.exists()


def test_loads_approved_documents():
    documents = load_documents(CORPUS_PATH)
    assert len(documents) == 8
    assert any(document.doc_id == "WEB-DRMADHU-006" for document in documents)


def test_metadata_manifest_is_present():
    manifest = load_manifest(METADATA_MANIFEST_PATH)
    assert manifest["document_count"] == 8
    assert manifest["metadata_version"] == "v1_business_rules"


def test_pcos_filter_matches_service_page():
    documents = load_documents(CORPUS_PATH)
    filters = infer_filters("Can Dr Madhu help with PCOS and endometriosis?")
    matches = [document.doc_id for document in documents if matches_filters(document, filters)]
    assert "WEB-DRMADHU-006" in matches


def test_answer_is_doctor_friendly_not_raw_corpus():
    from app.rag.retriever import RagRetriever

    documents = load_documents(CORPUS_PATH)
    retriever = RagRetriever(documents, {}, Path('/tmp/rag-demo-test-vectors.jsonl'), use_vertex=False)
    result = retriever.answer('Can Dr Madhu help with PCOS and endometriosis?')

    assert result['status'] == 'success'
    assert 'Yes.' in result['answer']
    assert 'Headings:' not in result['answer']
    assert result['retrieval']['doc_id'] == 'WEB-DRMADHU-006'


def test_system_instruction_is_strict():
    from app.rag.answering import SYSTEM_INSTRUCTION

    required_sections = [
        "ROLE",
        "PRIMARY OBJECTIVE",
        "CONTEXT BOUNDARY",
        "MEDICAL SAFETY",
        "RESPONSE STYLE",
        "OUTPUT CONTRACT",
        "WHEN INFORMATION IS MISSING",
        "PRIVACY",
    ]
    for section in required_sections:
        assert section in SYSTEM_INSTRUCTION
    assert "approved website context" in SYSTEM_INSTRUCTION
    assert "Do not diagnose" in SYSTEM_INSTRUCTION
    assert "Never invent facts" in SYSTEM_INSTRUCTION
    assert "Do not mention chunks, embeddings, retrieval, scores" in SYSTEM_INSTRUCTION
    assert "At present, I’m not sure about that" in SYSTEM_INSTRUCTION
    assert "Never tell the user that you are limited by website content" in SYSTEM_INSTRUCTION
    assert "maximum of 4 bullet points" in SYSTEM_INSTRUCTION
    assert "Each bullet must start with one relevant simple icon" in SYSTEM_INSTRUCTION


def test_missing_answer_uses_clinic_assistant_voice():
    from app.rag.retriever import RagRetriever

    retriever = RagRetriever([], {}, Path('/tmp/rag-demo-empty-vectors.jsonl'), use_vertex=False)
    result = retriever.answer('What is the consultation fee?')

    assert result['status'] == 'not_found'
    assert 'At present' in result['answer']
    assert 'website' not in result['answer'].lower()
    assert 'approved' not in result['answer'].lower()
    assert 'appointment' in result['answer'].lower()


def test_fallback_answers_use_icon_bullets():
    from app.rag.retriever import RagRetriever

    documents = load_documents(CORPUS_PATH)
    retriever = RagRetriever(documents, {}, Path('/tmp/rag-demo-test-vectors.jsonl'), use_vertex=False)
    result = retriever.answer('what is IVF')
    lines = [line for line in result['answer'].splitlines() if line.strip()]

    assert 1 <= len(lines) <= 4
    assert lines[0].startswith('💡')


def test_followup_summary_uses_previous_topic():
    from app.rag.retriever import expand_followup_question

    expanded = expand_followup_question('give me summary', [{'role': 'assistant', 'content': 'IVF and ICSI Treatments'}])
    assert 'IVF and ICSI Treatments' in expanded

def test_prep_question_prefers_fertility_assessment():
    from app.rag.retriever import RagRetriever

    documents = load_documents(CORPUS_PATH)
    retriever = RagRetriever(documents, {}, Path('/tmp/rag-demo-test-vectors.jsonl'), use_vertex=False)
    result = retriever.answer('what prep should I do before visiting the doctor')
    assert result['retrieval']['doc_id'] == 'WEB-DRMADHU-002'


def test_compact_history_keeps_25_turns():
    from app.rag.answering import compact_history

    history = [{"role": "user", "content": f"turn {index}"} for index in range(30)]
    compacted = compact_history(history)

    assert "turn 5" in compacted
    assert "turn 4" not in compacted
    assert "turn 29" in compacted
