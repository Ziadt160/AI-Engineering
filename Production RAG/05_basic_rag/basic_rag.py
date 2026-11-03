from langchain_community.document_loaders import (DirectoryLoader, PyPDFLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openrouter.chat_models import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from operator import itemgetter
import tempfile
load_dotenv()

def create_kn():

    loader = DirectoryLoader("./files", glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    embedding = HuggingFaceEmbeddings(
        model_name=r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        query_encode_kwargs={
            "normalize_embeddings": True,
            "prompt": "Represent this sentence for searching relevant passages: ",
        },
    )

    vector_store = Chroma.from_documents(chunks, embedding=embedding, persist_directory=tempfile.mkdtemp(), collection_name="test_rag")

    return vector_store


def create_rag():

    vector_store = create_kn()
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})

    chat_model = ChatOpenRouter(
        model_name="gpt-4o-mini",
        temperature=0.2
    )

    def format_docs(docs):
        return "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])

    prompt = ChatPromptTemplate.from_template(
        """
    you are helpful assistant that answers questions based on the following context:

    {context}

    Question: {question}

    answer in a consise and clear manner, if the answer is not in the context, say "I don't know"
    """)


    rag = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | chat_model
        | StrOutputParser()
    )


    answer = rag.invoke("How many days of paid annual leave do employees get?")
    print(answer)
    return answer



if __name__ == "__main__":
    create_rag()
