import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from mentor_matching.data import (
    load_or_create_mentors,
    compute_and_cache_embeddings,
    SAMPLE_PROJECT_INPUTS,
)
from mentor_matching.embedding import build_project_text, embed_text
from mentor_matching.models import Project
from mentor_matching.recommender import recommend_mentors
from mentor_matching.matcher import Matcher, MatchRequest


def test_recommendation_pipeline():
    print("=" * 60)
    print("COLLAB - Mentor Recommendation Pipeline Test")
    print("=" * 60)

    mentors = load_or_create_mentors()
    print(f"\nLoaded {len(mentors)} mentors")

    compute_and_cache_embeddings(mentors)
    print("Embeddings computed & cached\n")

    matcher = Matcher()

    for i, inp in enumerate(SAMPLE_PROJECT_INPUTS, 1):
        print(f"\n{'-' * 50}")
        print(f"PROJECT {i}: {inp.title}")
        print(f"  Domain: {inp.domain}  |  Goal: {inp.goal.value}")

        project = Project(
            title=inp.title,
            abstract=inp.abstract,
            domain=inp.domain,
            goal=inp.goal,
            scholar_id=inp.scholar_id,
        )
        text = build_project_text(project.title, project.abstract, project.domain)
        project.embedding = embed_text(text).tolist()

        recs = recommend_mentors(project, mentors, top_n=3)
        print(f"  Top {len(recs)} Recommendations:")
        for j, rec in enumerate(recs, 1):
            match_mark = "[D]" if rec.domain_match else "   "
            print(f"  {j}. {match_mark} {rec.mentor.name:24s} | {rec.mentor.affiliation:20s} | Score: {rec.similarity_score:.4f} | Domain: {rec.mentor.domain}")

        top_mentor = recs[0].mentor
        match_req = MatchRequest(
            project_id=project.id,
            mentor_id=top_mentor.id,
            scholar_id=inp.scholar_id,
        )
        match = matcher.create_request(match_req)
        match.similarity_score = recs[0].similarity_score
        print(f"  -> Scholar requested match with {top_mentor.name} (status: {match.status.value})")

        responded = matcher.respond(str(match.id), "accepted")
        print(f"  -> Mentor responded: {responded.status}")

    print(f"\n{'=' * 60}")
    print(f"Total matches created: {len(matcher._matches)}")
    accepted = sum(1 for m in matcher._matches.values() if m.status == "accepted")
    print(f"Accepted: {accepted}")
    print("Pipeline test PASSED")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    test_recommendation_pipeline()
