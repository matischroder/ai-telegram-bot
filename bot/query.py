from llama_index.llms.openai import OpenAI
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def query(query):
    llm = OpenAI(model="gpt-4o-mini")
    # Define el modelo de embeddings de Hugging Face
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # Crea el contexto de almacenamiento
    storage_context = StorageContext.from_defaults(persist_dir="./data/storage")

    # Carga el índice desde el almacenamiento
    index = load_index_from_storage(
        storage_context=storage_context,
        index_id="vector_index",
        embed_model=embed_model,
    )

    query_engine = index.as_query_engine(llm)
    response = query_engine.query(query)
    return response.response
