#!/bin/bash
# East Point Hospital - Automated EMR System & NMC Audit Simulator
# Launch Script

echo "================================================================="
echo "   EAST POINT HOSPITAL - AUTOMATED EMR & NMC AUDIT SIMULATOR     "
echo "================================================================="
echo ""

# Activate Python Virtual Environment
source .venv/bin/activate
export PYTHONPATH=backend

PORT=8050
echo "Starting EMR Application Server on http://localhost:${PORT}..."
echo "  • EMR Web Dashboard: http://localhost:${PORT}"
echo "  • Interactive API Docs: http://localhost:${PORT}/docs"
echo ""

uvicorn app.main:app --host 127.0.0.1 --port ${PORT} --reload
