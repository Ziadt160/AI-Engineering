import threading
import time
from collections import OrderedDict
from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openrouter import ChatOpenRouter

load_dotenv()


def default_embeddings() -> Embeddings:
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-large-en-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


@dataclass(frozen=True)
class CacheHit:
    query: str  # the cached query that matched, not the incoming one
    response: str
    score: float  # cosine similarity; 1.0 for an exact text match


@dataclass
class _CacheEntry:
    query: str
    response: str
    vector: np.ndarray
    created_at: float


class SemanticCache:
    """Cache LLM responses by query meaning rather than exact text.

    A lookup returns the stored response whose query is most similar to the
    incoming one, if the cosine similarity reaches `threshold`. Entries are
    evicted least-recently-used once `max_size` is reached, and dropped after
    `ttl_seconds` if set. Safe to share across threads.
    """

    def __init__(
        self,
        embeddings: Embeddings | None = None,
        *,
        threshold: float = 0.9,
        max_size: int = 1_000,
        ttl_seconds: float | None = None,
    ):
        if not 0.0 < threshold <= 1.0:
            raise ValueError(f"threshold must be in (0, 1], got {threshold}")
        if max_size < 1:
            raise ValueError(f"max_size must be >= 1, got {max_size}")

        self.embeddings = embeddings or default_embeddings()
        self.threshold = threshold
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

        self._entries: OrderedDict[str, _CacheEntry] = OrderedDict()  # least recently used first
        self._keys: list[str] = []  # row i of _matrix belongs to _entries[_keys[i]]
        self._matrix: np.ndarray | None = None  # rebuilt lazily after any write
        self._lock = threading.Lock()

    def __len__(self) -> int:
        with self._lock:
            return len(self._entries)

    def get(self, query: str) -> CacheHit | None:
        hit, _ = self._lookup(query)
        return hit

    def set(self, query: str, response: str) -> None:
        self._store(query, response, self._embed(query))

    def get_or_compute(self, query: str, compute: Callable[[str], str]) -> str:
        """Return the cached response, or call `compute` and cache its result.

        Embeds the query only once, unlike calling get() then set().
        """
        hit, vector = self._lookup(query)
        if hit is not None:
            return hit.response
        response = compute(query)
        self._store(query, response, vector)  # vector is always set on a miss
        return response

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._invalidate()

    def _lookup(self, query: str) -> tuple[CacheHit | None, np.ndarray | None]:
        key = self._normalize(query)
        with self._lock:
            self._evict_expired()
            entry = self._entries.get(key)
            if entry is not None:
                self._entries.move_to_end(key)
                return CacheHit(entry.query, entry.response, 1.0), None

        vector = self._embed(query)  # outside the lock: this is the slow part

        with self._lock:
            if not self._entries:
                return None, vector
            if self._matrix is None:
                self._keys = list(self._entries)
                self._matrix = np.stack([self._entries[k].vector for k in self._keys])

            scores = self._matrix @ vector  # unit vectors, so dot product == cosine
            best = int(np.argmax(scores))
            score = float(scores[best])
            if score < self.threshold:
                return None, vector

            key = self._keys[best]
            entry = self._entries[key]
            self._entries.move_to_end(key)
            return CacheHit(entry.query, entry.response, score), vector

    def _store(self, query: str, response: str, vector: np.ndarray) -> None:
        key = self._normalize(query)
        with self._lock:
            self._entries[key] = _CacheEntry(query, response, vector, time.monotonic())
            self._entries.move_to_end(key)
            while len(self._entries) > self.max_size:
                self._entries.popitem(last=False)
            self._invalidate()

    def _evict_expired(self) -> None:
        if self.ttl_seconds is None:
            return
        cutoff = time.monotonic() - self.ttl_seconds
        expired = [k for k, e in self._entries.items() if e.created_at < cutoff]
        for k in expired:
            del self._entries[k]
        if expired:
            self._invalidate()

    def _invalidate(self) -> None:
        self._matrix = None
        self._keys = []

    def _embed(self, text: str) -> np.ndarray:
        # Normalize here too, so injected embedding models that don't normalize still work.
        vector = np.asarray(self.embeddings.embed_query(text), dtype=np.float32)
        norm = np.linalg.norm(vector)
        return vector / norm if norm else vector

    @staticmethod
    def _normalize(query: str) -> str:
        return " ".join(query.lower().split())


class ModelRouting:

    def __init__(self):
        self.expensive = ChatOpenRouter(model="gpt-4o")
        self.cheap = ChatOpenRouter(model="gpt-4o-mini")
        self.classifier = ChatOpenRouter(model="gpt-4o-mini")

    def classifiy(self, query: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            """
Classify this query's complexity as 'simple' or 'complex'.

Simple: Basic facts, short answers, simple calculations
Complex: Analysis, reasoning, creative tasks, multi-step problems

Query: {query}

Respond with only: simple or complex
"""
        )

        response = self.classifier.invoke(prompt.invoke(query))

        return response.content.strip().lower()

    def invoke(self, query: str) -> tuple[str, str, float]:

        complexity = self.classifiy(query)

        if complexity == "simple":
            model = self.cheap
            model_name = "gpt-4o-mini"
            cost_per_1k = 0.00015

        elif complexity == "complex":
            model = self.expensive
            model_name = "gpt-4o"
            cost_per_1k = 0.00040

        response = model.invoke(query)

        tokens = int(len(query.split(" ")) * 1.3)

        cost = (tokens / 1000) * cost_per_1k

        return response.content, model_name, cost 

class TokenBudget:

    def __init__(self, max_token_per_request : int = 4000):
        self.max_token_per_request = max_token_per_request
        self.usage = {
            "input_tokens" : 0,
            "output_tokens" : 0,
            "requests" : 0
        }

    def estimate_token(self, text: str) -> int:
        return int(len(text.split(" ")) * 1.3)

    def check_token_budget(self, text: str) -> tuple[bool, int]:
        """ check token budget based on the maximum token per request"""
        output_tokens = self.estimate_token(text)
        return output_tokens >= self.max_token_per_request, output_tokens

    def record_usage(self, input_tokens: int, output_tokens: int):
        self.usage["input_tokens"] += input_tokens
        self.usage["output_tokens"] +- output_tokens
        self.usage["requests"] += 1


class LLMBudgeted:

    def __init__(self, max_tokens : int = 4000):
        self.token_budget = TokenBudget(max_tokens)
        self.llm = ChatOpenRouter(
            model="gpt-4o-mini",
            temperature=0.2
        )

    def invoke(self, text: str):

        within_budget, tokens = self.token_budget.check_token_budget(text)

        if not within_budget:
            raise ValueError(
                 f"Query exceeds token budget: {tokens} > {self.budget.max_per_request}"
            )

        # Execute 
        response = self.llm.invoke(text)
        content = response.content


        # Record Usage
        output_tokens = self.token_budget.estimate_token(tokens)
        self.token_budget.record_usage(tokens, output_tokens)

