import pytest
from unittest.mock import MagicMock
from app.services.context_service import ContextService

@pytest.fixture
def embedder():
    embedder = MagicMock()
    return embedder

@pytest.fixture
def extraction_statistic():
    extraction_statistic = MagicMock()
    return extraction_statistic

@pytest.fixture
def vectorstore_type():
    vectorstore_type = MagicMock()
    return_value = MagicMock()
    vectorstore_type.return_value = return_value
    return vectorstore_type

@pytest.fixture
def payload_parser():
    payload_parser = MagicMock()
    return payload_parser


@pytest.fixture
def repository_handler():
    repository_handler = MagicMock()
    return repository_handler


@pytest.fixture
def course_context():
    course_context = MagicMock()
    return course_context 

@pytest.fixture
def backgroud_task():
    backgroud_task = MagicMock()
    return backgroud_task 


def test_context_service_create_context(embedder, 
                                        extraction_statistic, 
                                        vectorstore_type, 
                                        payload_parser, 
                                        repository_handler,
                                        course_context, 
                                        backgroud_task):
    context_service = ContextService(embedder=embedder, 
                                    extraction_statistic=extraction_statistic, 
                                    vectorstore=vectorstore_type,
                                    payload_parser=payload_parser,
                                    repository_handler=repository_handler,
                                    course_context=course_context)
    context_service.create_context(backgroud_task, {})
  
