from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

if __name__ == '__main__':
    information = """
    My name is Ruiz. I killed my father, Carlos. I have a son named Lucas.
    """

    prompt_template = """
    Given the information {information}, who killed Carlos?
    """

    summary_prompt_template = PromptTemplate(template=prompt_template, input_variables=["information"])

    llm = ChatOllama(model="llama3")
    chain = summary_prompt_template | llm | StrOutputParser()
    print("Invoking chain....")
    res = chain.invoke(input={"information": information})

    print(res)
    print("Done.")
