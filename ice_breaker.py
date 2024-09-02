from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

from third_parties.github_api import list_repositories

if __name__ == '__main__':
    prompt_template = """
    Given the following Github repositories {information} of a software engineer, provide the following:
    1. a short summary of the engineer
    2. the top list of programming languages used
    """
    summary_prompt_template = PromptTemplate(template=prompt_template, input_variables=["information"])
    username = "poolgolez"

    llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm | StrOutputParser()
    repos = list_repositories(username, limit=50, mock=True)

    print("The model is thinking...")
    repository_summary = "\n".join([f"* {str(repo)}" for repo in repos])
    res = chain.invoke(input={"information": repository_summary})
    print(res)
    print("Done.")
