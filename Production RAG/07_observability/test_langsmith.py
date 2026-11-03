from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


@traceable(name="testing", tags=["quantum"])
def explain_topic(topic: str) -> str:

    prompt = ChatPromptTemplate.from_template(""" Please explain this topic : {topic}, in simple terms""")

    llm = ChatOpenRouter(
        model="gpt-4o-mini",
        temperature=0
    )

    chain = (
        prompt | llm | StrOutputParser()
    )

    response = chain.invoke(topic)

    return response 


if __name__ == "__main__":

    explain_topic("quantum computing")

