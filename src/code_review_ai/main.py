from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from github import UnknownObjectException

from src.code_review_ai.schemas import ReviewIn, ReviewOut
from src.code_review_ai.config import system_prompt, create_user_message
from src.code_review_ai.repo_handler import retrieve_repository_files
from src.code_review_ai.groq_request import fetch_llm_review
from src.code_review_ai.exceptions import RateLimitError


app = FastAPI()


@app.post("/review", response_model=ReviewOut)
async def get_review_to_code(project_info: ReviewIn):
    try:
        repo_content = retrieve_repository_files(project_info.github_repo_url)

        user_message = create_user_message(
            project_info.assignment_description,
            project_info.candidate_level,
            str(repo_content)
        )

        llm_response = fetch_llm_review(system_prompt, user_message)

        return {
            "found_files": list(repo_content.keys()),
            "downsides_and_comments": llm_response["downsides"],
            "conclusion": llm_response["conclusion"],
            "rating": llm_response["rating"]
        }
    except RateLimitError as e:
        return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content=str(e))
    except UnknownObjectException as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=str(e))
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))
