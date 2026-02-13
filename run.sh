#!/bin/bash
# Quick run script for development
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
