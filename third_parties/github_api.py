import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('GITHUB_API_KEY')

def search_username(name):
    user = search_user(name)
    return user.username if user is not None else None

def search_user(name: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {"q": name}
    response = requests.get(f"https://api.github.com/search/users", params=params, headers=headers)
    users = [User(**user, username=user["login"]) for user in (json.loads(response.text)["items"])]
    return users[0] if len(users) > 0 else None


def list_repositories(username: str, limit: int = 50, mock: bool = False):
    if mock:
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources/poolgolez_repos.json")
        file = open(file_path, "r")
        content = file.read()
        file.close()
        repos = [Repository(**repo) for repo in json.loads(content)]
    else:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {API_KEY}"
        }
        params = {
            "sort": "updated",
            "type": "all"
        }
        response = requests.get(f"https://api.github.com/users/{username}/repos", params=params, headers=headers)
        repos = [Repository(**repo) for repo in json.loads(response.text)]

    print(f"There are originally {len(repos)} repositories.")
    repo_count = min(limit, len(repos))
    return repos[:repo_count]


class Repository:
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

class User:
    def __init__(self, **kwargs):
        self.id = kwargs["id"]
        self.username = kwargs["username"]

if __name__ == '__main__':
    username = search_username("Paul Edward Golez")
    repos = list_repositories(username, mock=True)
    print(repos)
