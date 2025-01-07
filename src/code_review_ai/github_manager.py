from github import Github


class GithubManager:
    def __init__(self, auth):
        self.g = Github(auth=auth)

    def __enter__(self):
        return self.g

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.g.close()
