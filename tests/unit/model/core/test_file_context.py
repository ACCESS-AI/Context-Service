

import pytest
from unittest.mock import MagicMock
from app.model.core.file_context import ContextCreationException, FileContext
from langchain.docstore.document import Document


@pytest.fixture
def reader_valid():
    doc =  Document(page_content="text", metadata={"source": "local"})
    reader = MagicMock()
    reader.extract_data.return_value = [doc,doc]
    return reader

@pytest.fixture
def reader_raises():
    reader = MagicMock()
    reader.extract_data.side_effect = ValueError("error")
    return reader

def test_file_context_create_context_chunks_valid(reader_valid):
    file_context = FileContext('path','ident', reader=reader_valid)
    docs = file_context.create_context_chunks({"new":'metadata'})
    assert len(docs) == 2
    for doc in docs:
        assert doc.metadata['new'] == 'metadata'

def test_file_context_create_context_chunks_raises(reader_raises):
    file_context = FileContext('path','ident', reader=reader_raises)
    with pytest.raises(ContextCreationException):  # Replace SomeException with the specific exception you expect
        file_context.create_context_chunks({"new":'metadata'})
