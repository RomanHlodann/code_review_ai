from pydantic import BaseModel

from src.code_review_ai.config import CandidateLevel


class ReviewIn(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: CandidateLevel


class ReviewOut(BaseModel):
    found_files: list[str]
    downsides_and_comments: str
    rating: str
    conclusion: str
