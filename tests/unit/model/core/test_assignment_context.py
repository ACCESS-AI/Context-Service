from unittest.mock import MagicMock, Mock
import pytest
from app.model.core.assignment_context import AssignmentContext
from app.model.core.file_context import ContextCreationException

@pytest.fixture
def assignment_context():
    context_fakes_paths: str = 'tests/utils/fake_context'
    return AssignmentContext(context_fakes_paths)

@pytest.fixture
def valid_file():
    file = MagicMock()
    file.return_value = 'valid'
    file.create_context_chunks.return_value = None
    return file

@pytest.fixture
def invalid_file():
    file = MagicMock()
    file.file_identifier = 'invalid'
    file.create_context_chunks.side_effect = ContextCreationException("Error creating context chunks")
    return file

@pytest.fixture
def valid_vecstore():
    vectorstore = MagicMock()
    vectorstore.save_embedded_document.return_value = 2
    return vectorstore

@pytest.fixture
def invalid_vecstore():
    vectorstore = MagicMock()
    vectorstore.save_embedded_document.side_effect = Exception("Error saving document")
    return vectorstore

def test_good_bad_file(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("good_bad_file")
    assert len(list_files_with_valid_extension) == 1
    assert len(assignment_context.get_unsuccessfull_files) == 1
    assert list_files_with_valid_extension[0].file_identifier.split("/")[-1] == 'good.txt'
    assert assignment_context.get_unsuccessfull_files[0].split("/")[-1] == 'bad.bad'

def test_one_bad_file(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("one_bad_file")
    assert len(list_files_with_valid_extension) == 0
    assert len(assignment_context.get_unsuccessfull_files) == 1
    assert assignment_context.get_unsuccessfull_files[0].split("/")[-1] == 'bad.bad'
    
def test_one_good_file(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("one_good_file")
    assert len(list_files_with_valid_extension) == 1
    assert len(assignment_context.get_unsuccessfull_files) == 0
    assert list_files_with_valid_extension[0].file_identifier.split("/")[-1] == 'good.txt'

def test_multiple_bad_files(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("multiple_bad_files")
    assert len(list_files_with_valid_extension) == 0
    assert len(assignment_context.get_unsuccessfull_files) == 2
    assert assignment_context.get_unsuccessfull_files[0].split("/")[-1] == 'bad.bad'
    assert assignment_context.get_unsuccessfull_files[1].split("/")[-1] == 'bad2.bad'

def test_multiple_good_files(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("multiple_good_files")
    assert len(list_files_with_valid_extension) == 2
    assert len(assignment_context.get_unsuccessfull_files) == 0
    assert list_files_with_valid_extension[0].file_identifier.split("/")[-1] == 'good.txt'
    assert list_files_with_valid_extension[1].file_identifier.split("/")[-1] == 'very_good.txt'
    
def test_multiple_good_bad_files(assignment_context):
    list_files_with_valid_extension = assignment_context.load_files_context("multiple_good_bad_files")
    assert len(list_files_with_valid_extension) == 2
    assert len(assignment_context.get_unsuccessfull_files) == 2
    assert list_files_with_valid_extension[0].file_identifier.split("/")[-1] == 'good2.txt' 
    assert list_files_with_valid_extension[1].file_identifier.split("/")[-1] == 'good.txt'
    assert assignment_context.get_unsuccessfull_files[0].split("/")[-1] == 'bad.bad' 
    assert assignment_context.get_unsuccessfull_files[1].split("/")[-1] == 'bad2.bad2'

def test_create_context_valid_file(assignment_context, valid_file):
    valid_files = assignment_context.create_context([valid_file])
    assert len(valid_files) == 1
    
def test_create_context_no_file(assignment_context):  
    valid_files = assignment_context.create_context([])
    assert len(valid_files) == 0
    
def test_create_context_invalid_file(assignment_context, invalid_file):  
    valid_files = assignment_context.create_context([invalid_file])
    assert len(valid_files) == 0

def test_create_multiple_valid_invalid_files(assignment_context, valid_file,  invalid_file):  
    invalid_file.__eq__ = Mock(return_value=True)
    valid_files = assignment_context.create_context([valid_file,valid_file, invalid_file, invalid_file])
    assert len(valid_files) == 2
    assert len(assignment_context.get_unsuccessfull_files) == 2 
    for file in valid_files:
        assert file == 'valid'
    for identifier in assignment_context.get_unsuccessfull_files:
        assert identifier == "invalid"

    
def test_save_documents_valid(assignment_context, valid_vecstore,  valid_file):  
    statistics = assignment_context.save_context([valid_file],valid_vecstore)
    valid_vecstore.save_embedded_document.assert_called_once()
    assert len(statistics.get_successfull_paths()) == 1
    assert len(statistics.get_unsuccessfull_paths()) == 0

def test_save_documents_invalid(assignment_context, invalid_vecstore,  valid_file):  
    statistics = assignment_context.save_context([valid_file],invalid_vecstore)
    invalid_vecstore.save_embedded_document.assert_called_once()
    assert len(statistics.get_unsuccessfull_paths()) == 1
    assert len(statistics.get_successfull_paths()) == 0
    
