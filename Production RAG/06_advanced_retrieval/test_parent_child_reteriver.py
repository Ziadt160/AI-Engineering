from langchain_community.vectorstores.chroma import Chroma
from langchain_classic.retrievers import ParentDocumentRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.storage import InMemoryStore
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor


embeddings = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
)



long_doc = Document(
        page_content="""
# Complete Guide to Building AI Agents

## Chapter 1: Introduction to AI Agents

AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve goals. Unlike simple chatbots, agents can use tools, maintain state, and execute multi-step plans.

The key components of an AI agent include:
- A language model for reasoning
- Tools for interacting with external systems
- Memory for maintaining context
- A planning mechanism for complex tasks

## Chapter 2: Agent Frameworks

Several frameworks exist for building AI agents:

LangChain provides the foundational abstractions for chains and simple agents. It excels at straightforward tool-calling patterns and integrates with many LLM providers.

LangGraph extends LangChain for complex, stateful agents. It introduces graph-based state management, enabling cycles, human-in-the-loop workflows, and persistent execution.

CrewAI focuses on multi-agent collaboration, allowing teams of specialized agents to work together on complex tasks.

## Chapter 3: Production Considerations

Deploying agents to production requires careful attention to:
- Error handling and fallbacks
- Token usage optimization
- Observability and tracing
- Security and access control
- State persistence and recovery

LangSmith provides observability for LangChain/LangGraph applications, offering tracing, evaluation, and monitoring capabilities.
        """,
        metadata={"source": "ai_agents_guide.md"},
    )

separators = ["\n\n", "\n", ". ", " "]

parent_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap= 200,
    separators=separators)

child_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=20,
    separators=separators
)

vector_store = Chroma(embedding_function=embeddings, collection_name="parent_child_demo")

docstore= InMemoryStore()

parent_child_retrierver = ParentDocumentRetriever(
    vectorstore=vector_store,
    docstore=docstore,
    parent_splitter=parent_text_splitter,
    child_splitter=child_text_splitter
)

parent_child_retrierver.add_documents([long_doc])

query = "What is langchain"

print(parent_child_retrierver.invoke(query))

