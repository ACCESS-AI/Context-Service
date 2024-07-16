from app.model.data_reader.base_reader import BaseReader
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from typing import List

class PDFReader(BaseReader):
    PAGE = 'page'
     
    def extract_data(self, filepath: str) -> List[Document]:
        loader = PyPDFLoader(filepath, extract_images=False)
        docs = loader.load_and_split()
        return  [self.__let_pagenumber_start_at_1(doc) for doc in docs]
    
    def __let_pagenumber_start_at_1(self, doc: Document):
        doc.metadata[self.PAGE]=doc.metadata[self.PAGE]+1
        return doc

   

        