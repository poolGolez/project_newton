from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama

from agents.github_agent import lookup_github_username
from output_parsers.github_profile_summary import summary_parser
from third_parties.github_api import list_repositories


def fetch_github_info(name: str):
    prompt_template = """
    Given the following Github repositories {repo_information} of {name}, provide the following:
    1. a short summary of the projects worked on
    2. the list of most common programming languages used
    
    {format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        template=prompt_template,
        input_variables=["repo_information"],
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )
    username = lookup_github_username(name, mock=True)

    print(f"Username of {name}: {username}")
    repos = list_repositories(username, limit=50)
    llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm | summary_parser

    print("The model is thinking...")
    response = chain.invoke(input={
        "repo_information": ("\n".join([str(repo) for repo in repos])),
        "name": name
    })
    print(f"============================ Response ============================")
    print(response)
    print(f"===================================================================")
    return response.to_dict()


if __name__ == '__main__':
    fetch_github_info("Paul Edward Golez")
