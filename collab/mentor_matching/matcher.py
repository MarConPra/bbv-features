from datetime import datetime, timezone
from .models import Match, MatchStatus, MatchRequest


class Matcher:
    def __init__(self):
        self._matches: dict[str, Match] = {}

    def create_request(self, req: MatchRequest) -> Match:
        match = Match(
            project_id=req.project_id,
            mentor_id=req.mentor_id,
            scholar_id=req.scholar_id,
        )
        self._matches[str(match.id)] = match
        return match

    def respond(self, match_id: str, action: MatchStatus | str) -> Match | None:
        match = self._matches.get(match_id)
        if match is None or match.status != MatchStatus.pending:
            return None
        match.status = MatchStatus(action) if isinstance(action, str) else action
        match.responded_at = datetime.now(timezone.utc)
        return match

    def get_match(self, match_id: str) -> Match | None:
        return self._matches.get(match_id)

    def get_matches_for_scholar(self, scholar_id: str) -> list[Match]:
        return [m for m in self._matches.values() if str(m.scholar_id) == scholar_id]

    def get_matches_for_mentor(self, mentor_id: str) -> list[Match]:
        return [m for m in self._matches.values() if str(m.mentor_id) == mentor_id]
