import os, openai

from llama_index import (
    load_index_from_storage,
    StorageContext,
)
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import QueryEngineTool
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.retrievers import VectorIndexRetriever
from llama_index.memory import ChatMemoryBuffer


openai.api_key = os.environ.get("OPENAI_API_KEY")


class ChatBot:
    def __init__(
        self,
        llm: OpenAI = OpenAI(temperature=0.1, model="gpt-3.5-turbo"),
    ) -> None:
        # check if ./data/storage exists
        if not os.path.exists("./data/storage"):
            print("here")
            os.makedirs("./data/storage", exist_ok=True)
        _storage_context = StorageContext.from_defaults(
            persist_dir=f"./data/storage",
        )
        _index = load_index_from_storage(storage_context=_storage_context)
        _memory = ChatMemoryBuffer.from_defaults(token_limit=3000)
        similarity_top_k = 5
        _retriever = VectorIndexRetriever(
            index=_index, similarity_top_k=similarity_top_k
        )

        _query_engine = RetrieverQueryEngine(retriever=_retriever)
        query_engine_tool = QueryEngineTool.from_defaults(
            query_engine=_query_engine,
        )

        _all_tools = [query_engine_tool]

        system_prompt = "Sos el asistente virtual un grupo de telegram que tiene como contexto un documento"

        self._agent = OpenAIAgent.from_tools(
            _all_tools,
            llm=llm,
            memory=_memory,
            system_prompt=system_prompt,
        )
        self._chat_history = []

    def reset(self) -> None:
        self._chat_history = []

    def get_sources_url(self, source_nodes: []) -> []:
        sources = []
        for source in source_nodes:
            metadata = source.node.metadata
            if "url" in metadata:
                url = metadata["url"]
                if url not in sources:
                    sources.append(url)
        return sources

    def chat(self, input_text: str) -> object:
        try:
            chat_history = self._chat_history
            chat_history.append(ChatMessage(role="user", content=input_text))
            response = self._agent.chat(input_text)
            sources = self.get_sources_url(response.source_nodes)
            print(sources)
            return response.response

        except Exception as e:
            print(f"Error: {e}")
