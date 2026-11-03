from langchain_huggingface import HuggingFaceEmbeddings
from typing import Optional
from langchain_postgres import PGVector
from pydantic import dataclasses
from dataclasses import field
from sqlalchemy.engine import make_url
import os
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
from langchain_openrouter import ChatOpenRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class BAAIEmbedding:

    def __init__(self):
        self._model = None
    @property
    def model(self):
        if self._model is None:
            self._model = HuggingFaceEmbeddings(
                model_name = r"C:\Users\pc\.cache\huggingface\hub\models--BAAI--bge-large-en-v1.5\snapshots\d4aa6901d3a41ba39fb536a557fa166f842b0e09",
                model_kwargs = {"device" : "cpu"},
                encode_kwargs = {"normalize_embeddings" : True}
            )

        return self._model

@dataclasses.dataclass
class Config:

    subpase_connection :str = make_url(os.getenv("POSTGRES_CONNECTION_URI")).set(
        password=os.getenv("POSTGRES_PASSWORD"), drivername="postgresql+psycopg", query={"sslmode": "require"}
    ).render_as_string(hide_password=False)

    embedding_model_name :str = r""

    embedding_model_kwargs :dict = field(default_factory=lambda: {"device" : "cpu"})

    embedding_encode_kwargs :dict = field(default_factory=lambda: {"normalize_embeddings" : True})

    llm_model_name: str = "gpt-4o-mini"

    llm_temperature: float = 0.0

    search_k: int = 4

    collection_name: str = "production_rag"



class RagProduction:

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._chain = None
        self.embedding = BAAIEmbedding()
        self._vector_store = None

    @property
    def vector_store(self) -> PGVector:

        if self._vector_store is None:
            self._vector_store = PGVector(
                embeddings=self.embedding.model,
                collection_name="production_rag",
                connection=self.config.subpase_connection,
                use_jsonb=True
            )
        return self._vector_store

    @property
    def chain(self):

        if self._chain is None:

            self._chain = self._create_chain()

        return self._chain

    def _create_chain(self):

        retriever = self.vector_store.as_retriever(search_kwargs={"k" : self.config.search_k})

        prompt = ChatPromptTemplate.from_template("""
        Answer the question based only on the context provided.

        Contexnt:
        {context}

        Question: {question}

        Answer:        
        """)

        llm = ChatOpenRouter(
            model=self.config.llm_model_name
            ,temperature=self.config.llm_temperature
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        chain = (
            {"question" : RunnablePassthrough() , "context" : retriever | format_docs} |
            prompt |
            llm |
            StrOutputParser()
        )

        return chain
