from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

from third_parties.github_api import search_username



def lookup_github_username(full_name: str, mock:bool=False):
    if mock:
        return "poolGolez"
    template = """Given the full name of {name}, find their GitHub username. 
    Your answer should contain the username only.
    """
    prompt_template = PromptTemplate(template=template, input_variables=["name"])

    llm = ChatOllama(model="llama3")
    tools_for_agent = [
        # Tool(
        #     name="Github Repositories List",
        #     func=lambda username: list_repositories(username, limit=50, mock=False),
        #     description="List public GitHub repositories given username"
        # ),
        Tool(
            name="GitHub Username Query",
            func=search_username,
            description="Get GitHub username given the user's full name"
        ),
    ]
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)
    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name=full_name)})
    return result["output"]


if __name__ == "__main__":
    lookup_github_username("Paul Golez")
