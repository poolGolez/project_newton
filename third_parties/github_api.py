import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def list_repositories(username: str, limit: int = 8, mock: bool = False):
    if mock:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources/poolgolez_repos.json")
        file = open(file_path, "r")
        content = file.read()
        file.close()
        repos = [GithubRepo(**repo) for repo in json.loads(content)]
    else:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.getenv('GITHUB_API_KEY')}"
        }
        params = {
            "sort": "updated",
            "type": "all"
        }
        response = requests.get(f"https://api.github.com/users/{username}/repos", params=params, headers=headers)
        repos = [GithubRepo(**repo) for repo in json.loads(response.text)]

    repo_count = min(limit, len(repos))
    return repos[:repo_count]


class GithubRepo:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.name = kwargs['name']
        self.description = kwargs['description']
        self.language = kwargs['language']
        self.created_at = kwargs['created_at']
        self.updated_at = kwargs['updated_at']

    def __str__(self):
        return (f"{self.name}"
                f"\nDescription: {self.description}"
                f"\nLanguage used: {self.language}\n")

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    repos = list_repositories("poolgolez", mock=True)
    print(repos)
