from abc import ABC, abstractmethod
from langchain_core.embeddings import Embeddings
from typing import Type

class BaseEmbedder(ABC):
    """
    We define the base class for the embedder. This class is an abstract class and it is used to define the interface for the embedder.
    if the method get_embedder is called This class so far should always return a langchain embedder, otherwise you have to select a vectorstore that can handle different embedders. 
    
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_embedder(self, **kwargs) -> Type[Embeddings]:
        pass