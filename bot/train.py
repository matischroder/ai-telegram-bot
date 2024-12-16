import os
import nest_asyncio
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Define a local Hugging Face embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def train_bot():
    documents = SimpleDirectoryReader("./data/md", exclude=["**/*.png"]).load_data()
    print("llego 1")
    print(documents)
    index = VectorStoreIndex.from_documents(
        documents, show_progress=True, use_async=True, embed_model=embed_model
    )
    print("llego 2")
    index.set_index_id("vector_index")
    print("llego 3")
    index.storage_context.persist("./data/storage")
    print("llego 4")


train_bot()
