from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from agents.github_agent import lookup_github_username
from third_parties.github_api import list_repositories


def fetch_github_info(name: str):
    prompt_template = """
    Given the following Github repositories {repo_information} of {name}, provide the following:
    1. a short summary of the projects worked on
    2. the list of most common programming languages used
    """
    summary_prompt_template = PromptTemplate(template=prompt_template, input_variables=["repo_information"])
    username = lookup_github_username(name)

    print(f"Username of {name}: {username}")
    repos = list_repositories(username, limit=50)
    llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm | StrOutputParser()

    print("The model is thinking...")
    response = chain.invoke(input={
        "repo_information": ("\n".join([str(repo) for repo in repos])),
        "name": name
    })
    print(f"============================ Response ============================")
    print(response)
    print(f"===================================================================")


if __name__ == '__main__':
    fetch_github_info("Paul Edward Golez")
