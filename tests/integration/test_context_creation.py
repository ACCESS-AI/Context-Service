import os
from unittest.mock import MagicMock
from langchain_community.embeddings import FakeEmbeddings
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from app.services.context_service import ContextService
from langchain_community.vectorstores.chroma import Chroma
import chromadb
import shutil

CHROM_DB_PATH = 'tests/tmp/chroma_db'


def clean_up_db():
    directory_path = CHROM_DB_PATH
    shutil.rmtree(directory_path)

class ChromaDb(BaseVectorstore):
    def __init__(self, embeddings, collection_name ):
        self.__persistent_client = chromadb.PersistentClient(path=CHROM_DB_PATH)
        self.__db = Chroma(
            persist_directory=CHROM_DB_PATH,
            client=self.__persistent_client,
            collection_name=collection_name,
            embedding_function=embeddings,
        )
        self.__collection_name = collection_name
    
    def save_embedded_document(self, docs) -> None:
        self.__db.add_documents(docs,collection_name =self.__collection_name)

def test_context_creation():
    background_tasks_mock = MagicMock()
    vectorstore = ChromaDb
    embedder = FakeEmbeddings(size=384)
    contextService = ContextService(embedder, MagicMock(), vectorstore)
    def side_effect(func, course_context, course_slug):
        return contextService._ContextService__create_context_background_task(course_context, course_slug)
    background_tasks_mock.add_task.side_effect = side_effect
    contextService.create_context(background_tasks_mock,{"course":'fake_course',"slug":'working'},'tests/utils/')  
    client = chromadb.PersistentClient(path=CHROM_DB_PATH)
    collection = client.get_collection("working")
    assert set(collection.peek()['documents']) == set(['This is context 3', 'This is context 2'])
    assert len(collection.peek()['documents']) == 2
    client._system.stop()
    clean_up_db()



