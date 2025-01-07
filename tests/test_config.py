import pytest
from src.code_review_ai.config import create_user_message, CandidateLevel


def test_candidate_level_enum():
    assert CandidateLevel.JUNIOR == "junior"
    assert CandidateLevel.MIDDLE == "middle"
    assert CandidateLevel.SENIOR == "senior"


@pytest.mark.parametrize(
    "assignment_description, candidate_level, repository_content, expected_message",
    [
        (
            "Implement a login feature",
            CandidateLevel.JUNIOR,
            '{"main.py": "def main(): pass"}',
            """
        Assignment: Implement a login feature
        Candidate level: junior
        Files in repository and their content: {"main.py": "def main(): pass"}
            """,
        ),
        (
            "Build a REST API",
            CandidateLevel.SENIOR,
            '{"code_review_ai.py": "from flask import Flask"}',
            """
        Assignment: Build a REST API
        Candidate level: senior
        Files in repository and their content: {"code_review_ai.py": "from flask import Flask"}
            """,
        ),
    ],
)
def test_create_user_message(assignment_description, candidate_level, repository_content, expected_message):
    result = create_user_message(assignment_description, candidate_level, repository_content)
    assert result.strip() == expected_message.strip()
