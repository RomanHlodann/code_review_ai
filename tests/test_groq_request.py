import pytest
from unittest.mock import MagicMock, patch
from src.code_review_ai.groq_request import fetch_llm_review, request_to_llm


@patch("src.code_review_ai.groq_request.api.chat.completions.create")
def test_fetch_llm_review_success(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"rating": 4, "downsides": "None", "conclusion": "Great job!"}'))
    ]
    mock_create.return_value = mock_response

    system_prompt = "System prompt"
    user_message = "User message"

    result = fetch_llm_review(system_prompt, user_message)

    assert result == {
        "rating": 4,
        "downsides": "None",
        "conclusion": "Great job!"
    }


@patch("src.code_review_ai.groq_request.api.chat.completions.create")
def test_fetch_llm_review_missing_parameter(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"rating": 4, "conclusion": "Great job!"}'))
    ]
    mock_create.return_value = mock_response

    system_prompt = "System prompt"
    user_message = "User message"

    with pytest.raises(ValueError, match="Failed to process LLM response"):
        fetch_llm_review(system_prompt, user_message)


@patch("src.code_review_ai.groq_request.api.chat.completions.create")
def test_fetch_llm_review_invalid_json(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Invalid JSON response"))
    ]
    mock_create.return_value = mock_response

    system_prompt = "System prompt"
    user_message = "User message"

    with pytest.raises(ValueError, match="Failed to process LLM response"):
        fetch_llm_review(system_prompt, user_message)


@patch("src.code_review_ai.groq_request.api.chat.completions.create")
def test_fetch_llm_review_max_attempts(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Invalid JSON response"))
    ]
    mock_create.return_value = mock_response

    system_prompt = "System prompt"
    user_message = "User message"

    with pytest.raises(ValueError, match="Failed to process LLM response"):
        fetch_llm_review(system_prompt, user_message, max_attempts=2)


@patch("src.code_review_ai.groq_request.api.chat.completions.create")
def test_request_to_llm(mock_create):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Test response"))
    ]
    mock_create.return_value = mock_response

    system_prompt = "Test system prompt"
    user_message = "Test user prompt"

    response = request_to_llm(system_prompt, user_message)

    assert response == "Test response"
    mock_create.assert_called_once_with(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]
    )
