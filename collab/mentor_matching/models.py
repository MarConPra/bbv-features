from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
from enum import Enum


class ProjectGoal(str, Enum):
    paper = "paper"
    patent = "patent"
    invention = "invention"


class MatchStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Mentor(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    email: str
    affiliation: str
    department: str
    designation: str
    domain: str
    research_areas: list[str]
    bio: str
    h_index: int = 0
    total_publications: int = 0
    recent_publications_2yr: int = 0
    publication_titles: list[str] = []
    orcid_id: Optional[str] = None
    scopus_id: Optional[str] = None
    availability: bool = True
    verified: bool = False
    embedding: Optional[list[float]] = None


class ProjectInput(BaseModel):
    title: str
    abstract: str
    domain: str
    goal: ProjectGoal
    scholar_id: UUID


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    scholar_id: UUID
    title: str
    abstract: str
    domain: str
    goal: ProjectGoal
    embedding: Optional[list[float]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MentorRecommendation(BaseModel):
    mentor: Mentor
    similarity_score: float
    domain_match: bool


class RecommendationResult(BaseModel):
    project_id: UUID
    recommendations: list[MentorRecommendation]


class MatchRequest(BaseModel):
    project_id: UUID
    mentor_id: UUID
    scholar_id: UUID


class Match(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    project_id: UUID
    mentor_id: UUID
    scholar_id: UUID
    status: MatchStatus = MatchStatus.pending
    similarity_score: float = 0.0
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    responded_at: Optional[datetime] = None


class MatchResponse(BaseModel):
    action: MatchStatus  # accepted or rejected
