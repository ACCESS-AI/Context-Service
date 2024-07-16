from app.model.embedding.base_embedder import BaseEmbedder
from app.model.output_adapter.base_vectorstore import BaseVectorstore
from langchain_milvus import Milvus
import os

class MilvusVectorstore(BaseVectorstore):
    def __init__(self, embedder: BaseEmbedder, collection_name: str, connection_args: dict = None) -> None:
        #TODO (mayble to do, might make sense to change drop_old and instead only update new files for efficiency reasons
        # but the embeddings generation is cheap, for mistral for instance around 1$ for around 20000 pages written text.
        index_params = {
        'metric_type': 'COSINE',
        'index_type': "IVF_FLAT",
        'params': {"nlist": 128}
        }
        search_params = {
        "metric_type": "COSINE",
        "params": {"nprobe": 12},
        }
        connection_args = {
            'uri': os.getenv('VECTOR_STORE_HOST', 'http://localhost:19530') 
        } 
        self.__db = Milvus(embedder, collection_name = collection_name, connection_args = connection_args , search_params = search_params, index_params=index_params,primary_field="id", auto_id = True,metadata_field="metadata", drop_old = True)

    def save_embedded_document(self, docs) -> None:
        self.__db.add_documents(docs)




