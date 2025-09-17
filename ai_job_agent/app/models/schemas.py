from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class JobLevel(str, Enum):
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    REMOTE = "remote"
    HYBRID = "hybrid"


class ResumeSection(BaseModel):
    section_name: str
    content: str
    order: int


class Resume(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    content: str
    sections: List[ResumeSection]
    skills: List[str]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Job(BaseModel):
    id: Optional[str] = None
    title: str
    company: str
    location: str
    job_type: JobType
    level: JobLevel
    description: str
    requirements: List[str]
    salary_range: Optional[str] = None
    posted_date: Optional[datetime] = None
    application_url: str
    match_score: Optional[float] = None


class CoverLetter(BaseModel):
    id: Optional[str] = None
    job_id: str
    resume_id: str
    content: str
    created_at: Optional[datetime] = None


class JobAlert(BaseModel):
    id: Optional[str] = None
    user_id: str
    keywords: List[str]
    locations: List[str]
    job_types: List[JobType]
    levels: List[JobLevel]
    min_salary: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    preferences: Dict[str, Any] = {}
    created_at: Optional[datetime] = None


class JobMatchRequest(BaseModel):
    resume_id: str
    job_preferences: Dict[str, Any] = {}
    location_preferences: List[str] = []
    max_results: int = 10


class ResumeUpdateRequest(BaseModel):
    resume_id: str
    job_description: str
    optimization_type: str = "skills_match"  # skills_match, keywords, ats_friendly


class CoverLetterRequest(BaseModel):
    resume_id: str
    job_id: str
    tone: str = "professional"  # professional, enthusiastic, creative
    length: str = "medium"  # short, medium, long