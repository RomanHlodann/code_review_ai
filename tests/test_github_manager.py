from unittest.mock import MagicMock, patch

from src.code_review_ai.github_manager import GithubManager


@patch("src.code_review_ai.github_manager.Github")
def test_github_manager_initialization(mock_github):
    mock_auth = MagicMock()

    manager = GithubManager(auth=mock_auth)

    mock_github.assert_called_once_with(auth=mock_auth)
    assert isinstance(manager, GithubManager)


@patch("src.code_review_ai.github_manager.Github")
def test_github_manager_context_manager(mock_github):
    mock_auth = MagicMock()
    mock_github_instance = MagicMock()
    mock_github.return_value = mock_github_instance

    with GithubManager(auth=mock_auth) as g:
        assert g == mock_github_instance
        mock_github.assert_called_once_with(auth=mock_auth)

    mock_github_instance.close.assert_called_once()


@patch("src.code_review_ai.github_manager.Github")
def test_github_manager_exit_calls_close(mock_github):
    mock_auth = MagicMock()
    mock_github_instance = MagicMock()
    mock_github.return_value = mock_github_instance

    manager = GithubManager(auth=mock_auth)

    manager.__exit__(None, None, None)

    mock_github_instance.close.assert_called_once()
