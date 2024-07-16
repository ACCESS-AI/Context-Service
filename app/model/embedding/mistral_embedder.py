from typing import Type
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.embeddings import Embeddings
import os
from app.model.embedding.base_embedder import BaseEmbedder


class MistralEmbedder(BaseEmbedder):

    def __init__(self):
        self.__embedder = MistralAIEmbeddings(mistral_api_key = os.getenv("MISTRAL_API_KEY"), model= os.getenv("MISTRAL_EMBEDDING_MODEL"))

    def get_embedder(self, **kwargs) -> Type[Embeddings]:
        return self.__embedder