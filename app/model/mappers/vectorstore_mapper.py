from typing import Type
from app.model.output_adapter.base_vectorstore import BaseVectorstore 
from app.model.output_adapter.milvus_vectorstore import MilvusVectorstore

class VectorstoreMapper:

    @staticmethod
    def get_vectorstore(vectorestore_name: str) -> Type[BaseVectorstore]:
        vectorstore: Type[BaseVectorstore] = {
            "Milvus": MilvusVectorstore
        }
        return vectorstore[vectorestore_name]
                           

    
 
    
