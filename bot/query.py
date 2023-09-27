from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index import (
    load_index_from_storage,
    StorageContext,
)


def query(query):
    vector_store = FaissVectorStore.from_persist_dir("./data/storage")
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store, persist_dir="./data/storage"
    )
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response.response
