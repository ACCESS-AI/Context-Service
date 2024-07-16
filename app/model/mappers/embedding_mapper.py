from app.model.embedding.mistral_embedder import MistralEmbedder
from app.model.embedding.base_embedder import BaseEmbedder
from app.model.embedding.ollama_embedder import OllamaEbedder
from langchain_core.embeddings import Embeddings
from typing import Type


class EmbeddingMapper:
    @staticmethod
    def get_embedding_model(embedder_name: str) -> Embeddings:
        embedders: dict[str, Type[BaseEmbedder]] = {
                "Ollama" : OllamaEbedder, 
                'Mistral' : MistralEmbedder
            }
        embedder: BaseEmbedder = embedders[embedder_name]()
        return embedder.get_embedder()
            