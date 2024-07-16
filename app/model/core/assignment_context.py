
from dataclasses import dataclass
from typing import List, Type
import os
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from app.model.utils.constants import CONTEXT_FOLDER
from app.model.core.file_context import ContextCreationException, FileContext
from app.model.mappers.reader_mapper import ReaderMapper

@dataclass
class  AssignmentsStatistics:
    successfull_files: List[str]
    unsuccessfull_files: List[str]

    def get_successfull_paths(self) -> List[str]:
        return self.successfull_files

    def get_unsuccessfull_paths(self) -> List[str]:
        return self.unsuccessfull_files
    
class AssignmentContext:
    def __init__(self, path:str, metadata = {}):
        self.__path = path
        self.__metadata = metadata
        self.__unsuccessfull_files: List[str] = []

    def get_metadata(self):
        return self.__metadata
    
    @property
    def get_unsuccessfull_files(self) -> List[str]:
        return self.__unsuccessfull_files

    def load_files_context(self, context_folder: str = CONTEXT_FOLDER, file_context: Type[FileContext] = FileContext) -> List[FileContext]: 
        valid_extension_file_context: List[FileContext] = []
        for root, _, file_names in os.walk(self.__path + "/" + context_folder ):
            for filename in file_names:
                abs_path = os.path.join(root, filename)
                file_identifier = self.__path.split("/")[-1] + "/" + context_folder + "/" + filename 
                mapper = ReaderMapper.get_mapper(filename)
                if mapper:
                    file = file_context(abs_path, file_identifier, mapper)
                    valid_extension_file_context.append(file)
                else:
                    self.__unsuccessfull_files.append(file_identifier)
        return valid_extension_file_context
        
    def create_context(self, files_context: List[FileContext]) -> List[FileContext]:
        for file_context in files_context[:]:
            try:
                file_context.create_context_chunks(self.__metadata)
            except ContextCreationException as e:
                print(f"Error processing file_context {file_context}: {e}")
                self.__unsuccessfull_files.append(file_context.file_identifier)
                files_context.remove(file_context)
        return files_context
    
    def save_context(self, files_context: List[FileContext], vectorstore: BaseVectorstore) -> AssignmentsStatistics:
        for file_context in files_context[:]:
            
            try:
                vectorstore.save_embedded_document(file_context.context_chunks)
            except Exception as e:
                print(f"Error processing file_context {file_context}: {e}")
                self.__unsuccessfull_files.append(file_context.file_identifier)
                files_context.remove(file_context)
        return AssignmentsStatistics([file_context.file_identifier for file_context in files_context],self.__unsuccessfull_files)
