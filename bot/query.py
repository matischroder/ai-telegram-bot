from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index import (
    load_index_from_storage,
    StorageContext,
)


def query(query):
    storage_context = StorageContext.from_defaults(persist_dir="./data/storage")
    index = load_index_from_storage(
        storage_context=storage_context, index_id="vector_index"
    )
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response.response
