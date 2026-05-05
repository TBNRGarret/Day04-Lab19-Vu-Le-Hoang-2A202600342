from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import numpy as np

client = openai.OpenAI()


class FlatRAG:
    def __init__(self, corpus: list[str]):
        self.corpus = corpus
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        """Lấy top_k đoạn văn liên quan nhất bằng TF-IDF."""
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        top_idx = np.argsort(scores)[::-1][:top_k]
        return [self.corpus[i] for i in top_idx]

    def answer(self, question: str) -> str:
        """Pipeline: retrieve → LLM answer."""
        docs = self.retrieve(question)
        context = "\n".join(docs)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Bạn là trợ lý thông minh. Dùng context sau để trả lời câu hỏi.",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nCâu hỏi: {question}",
                },
            ],
            temperature=0,
        )
        return response.choices[0].message.content.strip()
