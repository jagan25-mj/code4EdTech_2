from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)  # pdf, docx, txt
    content = Column(Text, nullable=False)
    extracted_skills = Column(Text)  # JSON string
    location = Column(String(100))
    job_role = Column(String(100))
    experience_years = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="resume")
    
    def get_skills(self) -> List[str]:
        return json.loads(self.extracted_skills) if self.extracted_skills else []

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200))
    content = Column(Text, nullable=False)
    required_skills = Column(Text)  # JSON string
    location = Column(String(100))
    experience_required = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    evaluations = relationship("Evaluation", back_populates="job_description")
    
    def get_required_skills(self) -> List[str]:
        return json.loads(self.required_skills) if self.required_skills else []

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"))
    
    # Scores
    overall_score = Column(Float, nullable=False)
    skills_match_score = Column(Float, default=0.0)
    semantic_similarity_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    
    # Detailed analysis
    matched_skills = Column(Text)  # JSON string
    missing_skills = Column(Text)  # JSON string
    suggestions = Column(Text)
    verdict = Column(String(20))  # High, Medium, Low
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    job_description = relationship("JobDescription", back_populates="evaluations")
    
    def get_matched_skills(self) -> List[str]:
        return json.loads(self.matched_skills) if self.matched_skills else []
    
    def get_missing_skills(self) -> List[str]:
        return json.loads(self.missing_skills) if self.missing_skills else []

# Pydantic models for API
class ResumeUpload(BaseModel):
    filename: str
    content: str
    job_role: Optional[str] = None
    location: Optional[str] = None
    experience_years: Optional[int] = 0

class JobDescriptionUpload(BaseModel):
    title: str
    company: Optional[str] = None
    content: str
    location: Optional[str] = None
    experience_required: Optional[int] = 0

class EvaluationResult(BaseModel):
    id: int
    resume_id: int
    job_description_id: int
    overall_score: float
    skills_match_score: float
    semantic_similarity_score: float
    experience_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    suggestions: str
    verdict: str
    created_at: datetime

class ResumeDetail(BaseModel):
    id: int
    filename: str
    content: str
    extracted_skills: List[str]
    location: Optional[str]
    job_role: Optional[str]
    experience_years: int
    uploaded_at: datetime
    evaluations: List[EvaluationResult]

class DashboardStats(BaseModel):
    total_resumes: int
    total_jobs: int
    total_evaluations: int
    high_matches: int
    medium_matches: int
    low_matches: int
    average_score: float