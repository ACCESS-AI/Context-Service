from typing import List, Type
from app.model.data_reader.csv_reader import CSVReader
from app.model.data_reader.docs_reader import DocsReader
from app.model.data_reader.ipynb_reader import IpynbReader
from app.model.data_reader.pptx_reader import PptxReader
from app.model.data_reader.txt_reader import TextReader
from app.model.data_reader.base_reader import BaseReader
from app.model.data_reader.pdf_reader import PDFReader

class ReaderMapper:

    @staticmethod
    def get_mapper(file_path: str) -> List[BaseReader]|None:
        file_extension = file_path.split(".")[-1]
        reader: Type[BaseReader] = {
            "csv" : CSVReader,
            "pdf" : PDFReader, 
            "docs" : DocsReader,  
            "ipynb" : IpynbReader,
            "pptx" : PptxReader,
            "txt" : TextReader, 
            'md': TextReader
        }
        if file_extension.lower() not in reader:
            return None
        return reader[file_extension]()


