# RAG Demo Architecture

This document explains the full project and execution flow using simple diagrams.

## 1. Overall Project Architecture

```mermaid
flowchart TD
    A["Doctor / Clinic Team"] --> B["Clinic Content + Demo Feedback"]
    B --> C["Content Review + Approval"]
    C --> D["RAG-Ready Documents"]
    D --> E["Embeddings"]
    E --> F["RAG Retriever"]
    F --> G["FastAPI Backend"]
    G --> H["Mobile Chat Review Page"]
    H --> A
```

## 2. Current Runtime Architecture

```mermaid
flowchart TD
    A["User opens Cloud Run review link"] --> B["frontend/index.html"]
    B --> C["POST /api/chat"]
    C --> D["backend/app/main.py"]
    D --> E["backend/app/rag/retriever.py"]
    E --> F["data/corpus/drmadhupatil_enriched_rag_corpus.jsonl"]
    E --> G["data/embeddings/drmadhupatil_vertex_embeddings.jsonl"]
    E --> H["Vertex AI / google-genai"]
    H --> I["Clinic answer"]
    I --> B
```

## 3. Content Improvement Loop

```mermaid
flowchart TD
    A["Doctor tests demo"] --> B["Doctor shares dated .md feedback"]
    B --> C["feedback/01_incoming_doctor_reviews"]
    C --> D["feedback/02_triaged_questions"]
    D --> E["feedback/03_approved_clinic_qa"]
    E --> F["data/01-18 content lanes"]
    F --> G["data/19_rag_ready_documents"]
    G --> H["data/embeddings"]
    H --> I["Cloud Run demo"]
    I --> A
```

## 4. Content Lane Sub-Architecture

```mermaid
flowchart LR
    A["Website Pages"] --> R["Merged RAG Documents"]
    B["Approved Q&A"] --> R
    C["Articles / Blogs / Interviews"] --> R
    D["Testimonials / Reviews"] --> R
    E["Patient Journey Scenarios"] --> R
    F["Consultation Guides"] --> R
    G["Treatment Explainers"] --> R
    H["Myth vs Fact"] --> R
    I["Podcast / Video Scripts"] --> R
    J["Safety Boundaries"] --> R
    K["Doctor Philosophy"] --> R
    R --> L["Embeddings"]
```

## 5. RAG Answer Runtime

```mermaid
flowchart TD
    A["Patient-style question"] --> B{"Greeting / Identity / FAQ?"}
    B -->|Yes| C["Curated direct answer"]
    B -->|No| D["Metadata filters"]
    D --> E["Hybrid retrieval"]
    E --> F["Clinic prompt"]
    F --> G["Model-generated answer"]
    G --> H["Answer sanitizer"]
    C --> I["Chat response"]
    H --> I
    I --> J["Source + grounding confidence shown separately"]
```

## 6. Embedding Reference Point

```mermaid
flowchart TD
    A["Approved content"] --> B["data/19_rag_ready_documents"]
    B --> C["data/embeddings/drmadhupatil_vertex_embeddings.jsonl"]
    C --> D["backend/app/rag/retriever.py"]
    D --> E["Assistant answer"]
```

## 7. Web Search Gating For Main Multi-Agent Project

```mermaid
flowchart TD
    A["User question"] --> B["Local FAQ / exact answers"]
    B --> C{"Confident answer?"}
    C -->|Yes| D["Answer from clinic knowledge"]
    C -->|No| E["Metadata-filtered RAG"]
    E --> F{"Confident answer?"}
    F -->|Yes| D
    F -->|No| G{"External/current info required?"}
    G -->|No| H["Safe appointment fallback"]
    G -->|Yes| I["web_search_agent allowed by policy"]
```

## 8. How This Connects Back To Multi-Agent Usecase-0

```mermaid
flowchart TD
    A["RAG Doctor Demo"] --> B["Final Prompt Spec"]
    A --> C["Approved Clinic Corpus"]
    A --> D["Feedback Loop"]
    B --> E["Main multi-agent usecase-0"]
    C --> E
    D --> E
    E --> F["triage_agent / FaqTools"]
    F --> G["local RAG first"]
    G --> H["web_search_agent only after gating"]
```

