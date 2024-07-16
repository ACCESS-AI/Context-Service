
from typing import Type
from fastapi import HTTPException
from app.model.core.course_context import CourseContext, CourseContextStatistics
from app.model.core.repository_handler import RepositoryHandler
from app.model.mappers.embedding_mapper import EmbeddingMapper
from app.model.mappers.vectorstore_mapper import VectorstoreMapper
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from app.model.output_adapter.posgres_stats_orm import ExtractionStatistic
from app.model.utils.config_parser import ConfigParser
from app.model.utils.constants import COURSES_PATH
from app.model.utils.payload_parser import PayloadParser
from langchain_core.embeddings import Embeddings

SUCCESSFULL_FILES_RESPONSE_KEY = "successfullFiles"
UNSUCCESSFULL_FILES_RESPONSE_KEY = "unsuccessfullFiles"
TIMESTAMP_RESPONSE_KEY = "timestamp"

class ContextService:
    
    def __init__(self, 
                embedder: Embeddings = None,
                extraction_statistic: ExtractionStatistic = ExtractionStatistic(),
                vectorstore: Type[BaseVectorstore] = VectorstoreMapper.get_vectorstore(ConfigParser().vectorstore_config.name),
                payload_parser: Type[PayloadParser] = PayloadParser,
                repository_handler: Type[RepositoryHandler] = RepositoryHandler,
                course_context: Type[CourseContext] = CourseContext
                 ):
        if not embedder:
            embedder = EmbeddingMapper.get_embedding_model(ConfigParser().embedder_config.name)
        self.__embedder = embedder
        self.__extraction_statistic = extraction_statistic
        self.__vectorstore = vectorstore
        self.__payload_parser = payload_parser
        self.__repository_handler = repository_handler
        self.__course_context = course_context

        
    def create_context(self, background_tasks, payload, courses_path:str = COURSES_PATH) -> str:
        payload_parser = self.__payload_parser(payload)
        repo_handler = self.__repository_handler(payload_parser.folder_name, courses_path)
        course_context = self.__course_context(repo_handler=repo_handler,
                            vectorstore = self.__vectorstore(self.__embedder, payload_parser.course_slug))
        background_tasks.add_task(self.__create_context_background_task,
                                  course_context=course_context,
                                  course_slug=payload_parser.course_slug)
        return {"message": "Context creation started in the background"}
        
    def get_context(self, course_slug: str): 
        print(course_slug)
        try:
            latest_statistic = ExtractionStatistic.select(ExtractionStatistic.successfull_files,ExtractionStatistic.unsuccessfull_files,ExtractionStatistic.timestamp).where(ExtractionStatistic.course_slug == course_slug).order_by(ExtractionStatistic.timestamp.desc()).limit(1).get()
            if latest_statistic:
                return {
                    SUCCESSFULL_FILES_RESPONSE_KEY: latest_statistic.successfull_files,
                    UNSUCCESSFULL_FILES_RESPONSE_KEY: latest_statistic.unsuccessfull_files,
                    TIMESTAMP_RESPONSE_KEY: latest_statistic.timestamp
                }
        except ExtractionStatistic.DoesNotExist:
            raise HTTPException(status_code=404, detail=f"No ExtractionStatistic found for course_slug: {course_slug}")

    def __create_context_background_task(self, course_context: CourseContext, course_slug: str) -> None:
        contextCreationStatistics = course_context.process_context(CourseContextStatistics([], []))         
        self.__extraction_statistic.create(course_slug = course_slug,
                                    successfull_files=contextCreationStatistics.successfull_files,
                                    unsuccessfull_files=contextCreationStatistics.unsuccessfull_files)

