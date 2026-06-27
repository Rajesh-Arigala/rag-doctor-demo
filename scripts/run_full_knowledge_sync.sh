#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DESTINATION="${1:-}"

if [[ -z "${DESTINATION}" ]]; then
  cat <<'USAGE'
Usage:
  scripts/run_full_knowledge_sync.sh <main-project-destination>

Example:
  scripts/run_full_knowledge_sync.sh "/Users/jhonny001/Desktop/GenAi Notes/Final_GenAi/Ai Agents/GCP/Customer_support_MultiAgents/implementation/usecase-0-v2/backend/knowledge/latest"
USAGE
  exit 2
fi

cd "${PROJECT_ROOT}"

PYTHON_BIN="${PYTHON_BIN:-backend/.venv/bin/python}"
if [[ ! -x "${PYTHON_BIN}" ]]; then
  PYTHON_BIN="python3"
fi

echo "Building Vertex embeddings..."
PYTHONPATH=backend "${PYTHON_BIN}" scripts/build_vertex_embeddings.py

echo "Exporting knowledge bundle..."
"${PYTHON_BIN}" scripts/export_knowledge_bundle.py

if [[ ! -f exports/latest/embeddings.jsonl ]]; then
  echo "ERROR: exports/latest/embeddings.jsonl is missing. Aborting import." >&2
  exit 1
fi

echo "Importing knowledge bundle..."
"${PYTHON_BIN}" scripts/import_knowledge_bundle.py exports/latest "${DESTINATION}"

echo "Knowledge sync complete."
echo "destination=${DESTINATION}"

