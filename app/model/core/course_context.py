from dataclasses import dataclass
from typing import List
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from app.model.core.repository_handler import RepositoryHandler

@dataclass
class CourseContextStatistics :
    successfull_files: List[str]
    unsuccessfull_files: List[str]

class CourseContext:
    def __init__(self, repo_handler: RepositoryHandler, vectorstore: BaseVectorstore ) -> None:
        self.__repo_handler = repo_handler
        self.__vectorstore = vectorstore

    def process_context(self, courseContextStatistics: CourseContextStatistics ) -> CourseContextStatistics :
        assignments_contexts = self.__repo_handler.get_assignment_contexts()
        for assignment_context in assignments_contexts:
            files = assignment_context.load_files_context()
            files = assignment_context.create_context(files)
            assignment_statistics = assignment_context.save_context(files, self.__vectorstore)
            courseContextStatistics.successfull_files.extend(assignment_statistics.get_successfull_paths())
            courseContextStatistics.unsuccessfull_files.extend(assignment_statistics.get_unsuccessfull_paths())
        return courseContextStatistics
