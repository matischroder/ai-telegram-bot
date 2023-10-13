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
    documents = SimpleDirectoryReader("./data/md", exclude=["**/*.png"]).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.set_index_id("vector_index")
    index.storage_context.persist("./data/storage")
