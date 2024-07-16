from abc import ABC, abstractmethod


class BaseVectorstore(ABC):
    
    @abstractmethod
    def save_embedded_document(self, docs) -> None:
        pass