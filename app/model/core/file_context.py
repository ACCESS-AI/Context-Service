from app.model.data_reader.base_reader import BaseReader
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from langchain_core.documents import Document
from typing import List

class ContextCreationException(Exception):
    pass

class FileContext:
    def __init__(self, file_path:str, file_identifier:str, reader: BaseReader):
        self.__file_path = file_path
        self.__file_identifier = file_identifier
        self.__reader = reader
        self.__context_chunks: List[Document] = []

    def __eq__(self, other):
        return self.file_identifier == other.file_identifier
    
    def create_context_chunks(self, metadata: dict) -> List[Document]:
        try:
            docs = self.__reader.extract_data(self.__file_path)
            self.__context_chunks = self.__update_metadata(docs=docs, metadata=metadata)
            return self.__context_chunks
        except Exception as e:
            raise ContextCreationException(f"Error creating context chunks for file {self.__file_identifier}: {e}")

    def __update_metadata(self, docs: List[Document], metadata: dict) -> List[Document]:
        for doc in docs:
            doc.metadata.update(metadata)
            doc.metadata["file_identifier"] = self.__file_identifier
        return docs
        
    @property
    def file_identifier(self) -> str:
        return self.__file_identifier
    
    @property
    def context_chunks(self)-> List[Document]:
        if not self.__context_chunks:
            raise ValueError("You need to first create the context chunks")
        else:
            return self.__context_chunks


    
    
        
