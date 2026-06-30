import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import Mentor, MentorRecommendation, Project


def recommend_mentors(
    project: Project,
    mentors: list[Mentor],
    top_n: int = 5,
    domain_boost: float = 1.15,
) -> list[MentorRecommendation]:
    if not mentors:
        return []

    project_emb = np.array(project.embedding).reshape(1, -1) if project.embedding else None
    if project_emb is None:
        return []

    mentor_embs = np.array([m.embedding for m in mentors if m.embedding is not None])
    valid_mentors = [m for m in mentors if m.embedding is not None]

    if len(valid_mentors) == 0:
        return []

    similarities = cosine_similarity(project_emb, mentor_embs)[0]

    results = []
    for i, mentor in enumerate(valid_mentors):
        score = float(similarities[i])

        domain_match = mentor.domain.lower() == project.domain.lower()
        if domain_match:
            score *= domain_boost

        if not mentor.availability:
            score *= 0.5

        if mentor.recent_publications_2yr > 0:
            score += 0.05

        results.append(MentorRecommendation(
            mentor=mentor,
            similarity_score=round(score, 4),
            domain_match=domain_match,
        ))

    results.sort(key=lambda r: r.similarity_score, reverse=True)
    return results[:top_n]
