# tests/test_retrieval.py
import pytest
from app.services.retrieval import retrieve

def test_retrieve():
    """Test if retrieval works"""
    results = retrieve("What is FAN?", top_k=3)
    assert len(results) > 0
    assert "text" in results[0]
    assert "score" in results[0]
