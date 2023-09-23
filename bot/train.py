import openai
import os

import faiss


from llama_index import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
)
from llama_index.vector_stores.faiss import FaissVectorStore

openai.api_key = os.environ.get("OPENAI_API_KEY")

d = 1536
faiss_index = faiss.IndexFlatL2(d)


def train_bot():
    documents = SimpleDirectoryReader("../data/latest").load_data()

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    index.storage_context.persist("../data/storage")
