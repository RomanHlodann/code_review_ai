from fastapi.testclient import TestClient
from unittest.mock import patch
from github import UnknownObjectException

from src.code_review_ai.main import app
from src.code_review_ai.exceptions import RateLimitError



@patch("src.code_review_ai.main.retrieve_repository_files")
@patch("src.code_review_ai.main.fetch_llm_review")
@patch("src.code_review_ai.main.create_user_message")
def test_get_review_to_code_success(mock_create_user_message, mock_fetch_llm_review, mock_retrieve_repository_files):
    mock_retrieve_repository_files.return_value = {"file1.py": "content1", "file2.py": "content2"}
    mock_create_user_message.return_value = "User message"
    mock_fetch_llm_review.return_value = {
        "downsides": "Some downsides",
        "conclusion": "Overall conclusion",
        "rating": "Good"
    }

    project_info = {
        "assignment_description": "Implement feature X",
        "candidate_level": "middle",
        "github_repo_url": "https://github.com/user/repo"
    }

    with TestClient(app) as client:
        response = client.post("/review", json=project_info)

    assert response.status_code == 200
    response_data = response.json()
    assert "found_files" in response_data
    assert "rating" in response_data
    assert "downsides_and_comments" in response_data
    assert "conclusion" in response_data


@patch("src.code_review_ai.main.retrieve_repository_files")
def test_get_review_to_code_rate_limit_error(mock_retrieve_repository_files):
    mock_retrieve_repository_files.side_effect = RateLimitError("Rate limit exceeded. Try after 2024-12-31T23:59:59Z")

    project_info = {
        "assignment_description": "Implement feature X",
        "candidate_level": "middle",
        "github_repo_url": "https://github.com/user/repo"
    }

    with TestClient(app) as client:
        response = client.post("/review", json=project_info)

    assert response.status_code == 429
    assert "Rate limit exceeded" in response.text


@patch("src.code_review_ai.main.retrieve_repository_files")
def test_get_review_to_code_unknown_object_error(mock_retrieve_repository_files):
    mock_retrieve_repository_files.side_effect = UnknownObjectException("Repository not found.")

    project_info = {
        "assignment_description": "Implement feature X",
        "candidate_level": "middle",
        "github_repo_url": "https://github.com/user/repo"
    }

    with TestClient(app) as client:
        response = client.post("/review", json=project_info)

    assert response.status_code == 404
    assert "Repository not found" in response.text


@patch("src.code_review_ai.main.retrieve_repository_files")
def test_get_review_to_code_value_error(mock_retrieve_repository_files):
    mock_retrieve_repository_files.side_effect = ValueError("Invalid data.")

    project_info = {
        "assignment_description": "Implement feature X",
        "candidate_level": "middle",
        "github_repo_url": "https://github.com/user/repo"
    }

    with TestClient(app) as client:
        response = client.post("/review", json=project_info)

    assert response.status_code == 500
    assert "Invalid data." in response.text
