from app.model.data_reader.base_reader import BaseReader
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextReader(BaseReader):
     
    def extract_data(self, filepath: str) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=705
        )
        loader = TextLoader(filepath)
        return  loader.load_and_split(text_splitter)
   

        