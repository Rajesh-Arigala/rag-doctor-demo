from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "backend"
sys.path.insert(0, str(BACKEND_ROOT))

from app.config import CORPUS_PATH, EMBEDDINGS_PATH, EMBEDDING_MODEL_NAME, GOOGLE_CLOUD_LOCATION, GOOGLE_CLOUD_PROJECT
from app.rag.embeddings import VertexEmbeddingClient
from app.rag.loader import load_documents, save_vectors


def main() -> None:
    documents = load_documents(CORPUS_PATH)
    client = VertexEmbeddingClient()
    vectors = client.embed_documents(documents)
    save_vectors(EMBEDDINGS_PATH, vectors)
    print("Vertex embeddings built")
    print(f"project={GOOGLE_CLOUD_PROJECT}")
    print(f"location={GOOGLE_CLOUD_LOCATION}")
    print(f"model={EMBEDDING_MODEL_NAME}")
    print(f"documents={len(documents)}")
    print(f"vectors={len(vectors)}")
    print(f"output={EMBEDDINGS_PATH}")


if __name__ == "__main__":
    main()

