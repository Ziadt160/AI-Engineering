from dotenv import load_dotenv
load_dotenv()

from importlib.metadata import version
from langchain_openrouter import ChatOpenRouter

core_version = version("langchain-core")
lg_version = version("langgraph")

print(f"LangChain Core version: {core_version}")
print(f"LangGraph version: {lg_version}")

def main():

    llm = ChatOpenRouter(model="gpt-4o-mini", temperature=0)
    response = llm.invoke("Say 'setup complete' in a single line.")
    print(response)


if __name__ == "__main__":
    main()
