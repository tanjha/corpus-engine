from sentence_transformers import SentenceTransformer


class embed_engine:
    def __init__(self, embeddings):
        self.model = SentenceTransformer(
            "nomic-ai/nomic-embed-text-v1", trust_remote_code=True
        )
        self.embeddings = embeddings

    def embedDoc(self, raw_text):
        embedding = self.model.encode(
            f"search_document: {raw_text}", normalize_embeddings=True
        )
        return embedding

    def embedAll(self, texts: list[str]):
        prefixed = [f"search_document: {text}" for text in texts]
        embedding = self.model.encode(
            prefixed, normalize_embeddings=True, batch_size=32, show_progress_bar=True
        )
        return embedding

    def _embedQuery(self, raw_text):
        embedding = self.model.encode(
            f"search_query: {raw_text}", normalize_embeddings=True
        )
        return embedding

    def similarity(self, raw_question):
        query_embed = self._embedQuery(raw_question)
        similarity = self.model.similarity(query_embed, self.embeddings)
        return similarity

    def setEmbed(self, embeddings):
        self.embeddings = embeddings
        return
