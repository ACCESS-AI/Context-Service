import pytest
from unittest.mock import MagicMock
from app.model.core.assignment_context import AssignmentsStatistics
from app.model.core.course_context import CourseContext, CourseContextStatistics
from app.model.core.repository_handler import RepositoryHandler

@pytest.fixture
def assignment_mock():
    assignment = MagicMock()
    file = MagicMock()
    assignment_statistics = AssignmentsStatistics(["success"], ["unsuccess"])
    assignment.load_files_context.return_value = [file]
    assignment.create_context.return_value = [file]
    assignment.save_context.return_value = assignment_statistics
    return assignment

@pytest.fixture
def repo_handler_mock(assignment_mock):
    repo_handler = MagicMock(spec=RepositoryHandler)
    repo_handler.get_assignment_contexts.return_value = [assignment_mock]
    return repo_handler

@pytest.fixture
def repo_handler_multiple_mock(assignment_mock):
    repo_handler = MagicMock(spec=RepositoryHandler)
    repo_handler.get_assignment_contexts.return_value = [assignment_mock, assignment_mock, assignment_mock]
    return repo_handler

def test_process_context_single(repo_handler_mock):
    course_context = CourseContext(repo_handler_mock, None)
    courseContextStatistics = course_context.process_context(CourseContextStatistics ([], []))
    assert courseContextStatistics.successfull_files == ["success"]
    assert courseContextStatistics.unsuccessfull_files == ["unsuccess"]
    
def test_process_context_multiple(repo_handler_multiple_mock):
    course_context = CourseContext(repo_handler_multiple_mock, None)
    courseContextStatistics = course_context.process_context(CourseContextStatistics ([], []))
    assert courseContextStatistics.successfull_files == ["success", "success", "success"]
    assert courseContextStatistics.unsuccessfull_files == ["unsuccess", "unsuccess", "unsuccess"]



