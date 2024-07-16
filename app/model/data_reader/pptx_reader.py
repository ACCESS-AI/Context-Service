from app.model.data_reader.base_reader import BaseReader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_core.documents import Document
from typing import List

class PptxReader(BaseReader):
     
    def extract_data(self, filepath: str) -> List[Document]:
        loader = UnstructuredPowerPointLoader(filepath)
        return  loader.load()
   

        