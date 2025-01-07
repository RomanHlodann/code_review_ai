import pytest

from unittest.mock import patch, MagicMock
from github import Repository, ContentFile

from src.code_review_ai.repo_handler import (
    retrieve_repository_files,
    get_repository_by_url,
    get_all_files_from_repository,
    get_repository_name_from_url
)
from src.code_review_ai.exceptions import RateLimitError


@pytest.fixture
def mock_github_manager(mocker):
    mock_manager = mocker.patch("github_manager.GithubManager", autospec=True)
    return mock_manager


def test_get_repository_name_from_url():
    url = "https://github.com/user/repo"
    repo_name = get_repository_name_from_url(url)
    assert repo_name == "user/repo"

    with pytest.raises(ValueError, match="Invalid repository url"):
        get_repository_name_from_url("invalid-url")


@patch("src.code_review_ai.repo_handler.GithubManager")
def test_get_repository_by_url(mock_github_manager):
    mock_github = mock_github_manager.return_value.__enter__.return_value

    mock_github.get_rate_limit.return_value.core.remaining = 1
    mock_github.get_rate_limit.return_value.core.reset = "2024-12-31T23:59:59Z"
    mock_github.get_repo.return_value = "mock_repo"

    url = "https://github.com/user/repo"
    repo = get_repository_by_url(url)

    mock_github.get_repo.assert_called_once_with("user/repo")

    assert repo == "mock_repo"


@patch("src.code_review_ai.repo_handler.GithubManager")
def test_get_repository_by_url_rate_limit_exceeded(mock_github_manager):
    mock_github = mock_github_manager.return_value.__enter__.return_value
    mock_github.get_rate_limit.return_value.core.remaining = 0
    mock_github.get_rate_limit.return_value.core.reset = "2024-12-31T23:59:59Z"

    url = "https://github.com/user/repo"

    with pytest.raises(RateLimitError, match="Rate limit exceeded. Try after 2024-12-31T23:59:59Z"):
        get_repository_by_url(url)


def test_get_all_files_from_repository():
    mock_repo = MagicMock(spec=Repository)
    mock_file1 = MagicMock(spec=ContentFile, type="file", path="file1.txt", decoded_content=b"content1")
    mock_file2 = MagicMock(spec=ContentFile, type="file", path="file2.txt", decoded_content=b"content2")
    mock_dir = MagicMock(spec=ContentFile, type="dir", path="dir")

    mock_repo.get_contents = MagicMock(side_effect=[
        [mock_file1, mock_dir],
        [mock_file2],
    ])

    files = get_all_files_from_repository(mock_repo)

    assert len(files) == 2
    assert files[0].path == "file1.txt"
    assert files[1].path == "file2.txt"
    mock_repo.get_contents.assert_any_call("")
    mock_repo.get_contents.assert_any_call("dir")


def test_retrieve_repository_files(mocker):
    mock_repo = MagicMock(spec=Repository)
    mocker.patch("src.code_review_ai.repo_handler.get_repository_by_url", return_value=mock_repo)

    mock_file1 = MagicMock(spec=ContentFile, path="file1.txt", decoded_content=b"content1")
    mock_file2 = MagicMock(spec=ContentFile, path="file2.txt", decoded_content=b"content2")
    mocker.patch("src.code_review_ai.repo_handler.get_all_files_from_repository", return_value=[mock_file1, mock_file2])

    files = retrieve_repository_files("https://github.com/user/repo")

    assert files == {"file1.txt": "content1", "file2.txt": "content2"}
