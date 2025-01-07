import os

from dotenv import load_dotenv
from github import Auth, Repository, ContentFile

from src.code_review_ai.exceptions import RateLimitError
from src.code_review_ai.github_manager import GithubManager

load_dotenv()

auth = Auth.Token(os.getenv("GITHUB_ACCESS_TOKEN"))


def retrieve_repository_files(url: str) -> dict[str, str]:
    repo = get_repository_by_url(url)
    files = get_all_files_from_repository(repo)

    result = {}
    for file in files:
        result[file.path] = file.decoded_content.decode("utf-8")

    return result


def get_repository_by_url(url: str) -> Repository:
    with GithubManager(auth=auth) as g:
        if g.get_rate_limit().core.remaining == 0:
            raise RateLimitError(f"Rate limit exceeded. Try after {str(g.get_rate_limit().core.reset)}.")
        repo_name = get_repository_name_from_url(url)
        return g.get_repo(repo_name)


def get_all_files_from_repository(repo: Repository) -> list[ContentFile]:
    contents = repo.get_contents("")

    result = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            result.append(file_content)

    return result


def get_repository_name_from_url(url: str) -> str:
    url_parts = url.split("/")

    if len(url_parts) < 2:
        raise ValueError("Invalid repository url")

    return "/".join(url_parts[-2:])
