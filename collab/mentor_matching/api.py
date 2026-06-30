from uuid import UUID
from fastapi import APIRouter, HTTPException

from .models import (
    MatchRequest, MatchResponse, MatchStatus,
    ProjectInput, Project, MentorRecommendation,
)
from .data import (
    load_or_create_mentors, compute_and_cache_embeddings,
    SAMPLE_PROJECT_INPUTS, embed_projects,
)
from .embedding import build_project_text, embed_text
from .recommender import recommend_mentors
from .matcher import Matcher


router = APIRouter(prefix="/api", tags=["collab"])

_mentors = load_or_create_mentors()
_projects: dict[str, Project] = {}
_matcher = Matcher()


def _ensure_mentor_embeddings():
    if _mentors and _mentors[0].embedding is None:
        compute_and_cache_embeddings(_mentors)


@router.get("/mentors")
def list_mentors():
    _ensure_mentor_embeddings()
    return [m.model_dump(mode="json", exclude={"embedding"}) for m in _mentors]


@router.get("/mentors/{mentor_id}")
def get_mentor(mentor_id: UUID):
    _ensure_mentor_embeddings()
    for m in _mentors:
        if m.id == mentor_id:
            return m.model_dump(mode="json", exclude={"embedding"})
    raise HTTPException(404, "Mentor not found")


@router.post("/projects")
def create_project(inp: ProjectInput):
    _ensure_mentor_embeddings()
    project = Project(
        title=inp.title,
        abstract=inp.abstract,
        domain=inp.domain,
        goal=inp.goal,
        scholar_id=inp.scholar_id,
    )
    text = build_project_text(project.title, project.abstract, project.domain)
    project.embedding = embed_text(text).tolist()
    _projects[str(project.id)] = project

    recs = recommend_mentors(project, _mentors)
    return {
        "project": project.model_dump(mode="json", exclude={"embedding"}),
        "recommendations": [r.model_dump(mode="json") for r in recs],
    }


@router.get("/projects/{project_id}/recommendations")
def get_recommendations(project_id: UUID):
    project = _projects.get(str(project_id))
    if not project:
        raise HTTPException(404, "Project not found")
    recs = recommend_mentors(project, _mentors)
    return {
        "project_id": str(project_id),
        "recommendations": [r.model_dump(mode="json") for r in recs],
    }


@router.get("/projects")
def list_projects():
    return [p.model_dump(mode="json", exclude={"embedding"}) for p in _projects.values()]


@router.post("/matches")
def request_match(req: MatchRequest):
    project = _projects.get(str(req.project_id))
    if not project:
        raise HTTPException(404, "Project not found")
    mentor = next((m for m in _mentors if m.id == req.mentor_id), None)
    if not mentor:
        raise HTTPException(404, "Mentor not found")

    recs = recommend_mentors(project, [mentor])
    score = recs[0].similarity_score if recs else 0.0

    match = _matcher.create_request(req)
    match.similarity_score = score
    return match.model_dump(mode="json", default=str)


@router.get("/matches/{match_id}")
def get_match(match_id: str):
    match = _matcher.get_match(match_id)
    if not match:
        raise HTTPException(404, "Match not found")
    return match.model_dump(mode="json", default=str)


@router.patch("/matches/{match_id}/respond")
def respond_to_match(match_id: str, body: MatchResponse):
    match = _matcher.respond(match_id, body.action)
    if not match:
        raise HTTPException(400, "Match not found or already responded")
    return match.model_dump(mode="json", default=str)


@router.get("/scholars/{scholar_id}/matches")
def scholar_matches(scholar_id: UUID):
    return [m.model_dump(mode="json", default=str) for m in _matcher.get_matches_for_scholar(str(scholar_id))]


@router.get("/debug/sample-projects")
def load_sample_projects():
    _ensure_mentor_embeddings()
    results = []
    for inp in SAMPLE_PROJECT_INPUTS:
        project = Project(
            title=inp.title,
            abstract=inp.abstract,
            domain=inp.domain,
            goal=inp.goal,
            scholar_id=inp.scholar_id,
        )
        text = build_project_text(project.title, project.abstract, project.domain)
        project.embedding = embed_text(text).tolist()
        recs = recommend_mentors(project, _mentors)
        results.append({
            "project": project.model_dump(mode="json", exclude={"embedding"}),
            "recommendations": [
                {
                    "mentor_name": r.mentor.name,
                    "affiliation": r.mentor.affiliation,
                    "score": r.similarity_score,
                    "domain_match": r.domain_match,
                }
                for r in recs
            ],
        })
    return results
