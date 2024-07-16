from typing import Type
from app.model.embedding.base_embedder import BaseEmbedder
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.embeddings import Embeddings
import os

class OllamaEbedder(BaseEmbedder):

    def __init__(self) -> None:
        self.__embedder = OllamaEmbeddings(model = os.getenv('OLLAMA_EMBEDDING_MODEL') , num_gpu=1, base_url=os.getenv('OLLAMA_EMBEDDING_HOST')) 

    def get_embedder(self) -> Type[Embeddings]:
        return self.__embedder
