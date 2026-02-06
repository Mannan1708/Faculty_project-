from pydantic import BaseModel
from typing import Optional, List

class FacultyBase(BaseModel):
    name: str
    faculty_type: str
    education: str
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None

class Faculty(FacultyBase):
    id: int

    class Config:
        from_attributes = True

class FacultyRecommendation(Faculty):
    similarity_score: float
    recommendation_type: str # 'Expertise', 'Collaborator', or 'Subject'
    matched_keywords: Optional[List[str]] = []
