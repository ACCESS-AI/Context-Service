from abc import ABC, abstractmethod
from langchain_core.documents import Document
from typing import List

class BaseReader(ABC):
    
    @abstractmethod
    def extract_data(self, filepath: str) -> List[Document]:
        pass

