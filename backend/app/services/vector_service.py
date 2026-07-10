import math
from typing import Dict, List, Tuple


class LocalVectorStore:
    def __init__(self) -> None:
        self.documents: List[Dict[str, object]] = []

    def _tokenize(self, text: str) -> List[str]:
        return [token for token in text.lower().replace("/", " ").replace("-", " ").split() if token.isalnum()]

    def _build_embedding(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        counts: Dict[str, int] = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1

        total_terms = len(tokens)
        embedding: Dict[str, float] = {}
        for token, count in counts.items():
            tf = count / total_terms if total_terms else 0.0
            idf = 1.0 + math.log((1 + len(self.documents)) / (1 + self._document_frequency(token)))
            embedding[token] = tf * idf
        return embedding

    def _document_frequency(self, token: str) -> int:
        count = 0
        for doc in self.documents:
            if token in doc["embedding"]:
                count += 1
        return count

    def add_document(self, doc_id: int, title: str, content_text: str) -> None:
        embedding = self._build_embedding(content_text)
        self.documents.append({"id": doc_id, "title": title, "content": content_text, "embedding": embedding})

    def rebuild(self, documents: List[Dict[str, object]]) -> None:
        self.documents = []
        for document in documents:
            self.add_document(int(document["id"]), str(document["title"]), str(document["content_text"]))

    def search(self, query: str, limit: int = 5) -> List[Tuple[int, float]]:
        query_embedding = self._build_embedding(query)
        scores: List[Tuple[int, float]] = []
        for document in self.documents:
            score = self._cosine_similarity(query_embedding, document["embedding"])
            if score > 0:
                scores.append((int(document["id"]), score))
        scores.sort(key=lambda item: item[1], reverse=True)
        return scores[:limit]

    def _cosine_similarity(self, left: Dict[str, float], right: Dict[str, float]) -> float:
        left_terms = set(left.keys())
        right_terms = set(right.keys())
        shared = left_terms & right_terms
        if not shared:
            return 0.0
        numerator = sum(left[word] * right[word] for word in shared)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)


vector_store = LocalVectorStore()
