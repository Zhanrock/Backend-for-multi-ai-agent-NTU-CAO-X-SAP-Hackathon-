# app/schemas/api_models.py
from pydantic import BaseModel

class QueryRequest(BaseModel):
    """Request model for asking Arai questions"""
    question: str
    style: str = "bullet"

class IdeaRequest(BaseModel):
    """Request model for submitting ideas"""
    idea_text: str
    employee: str
    branch: str

class KudosRequest(BaseModel):
    """Request model for posting kudos"""
    from_emp: str
    to_emp: str
    message: str
