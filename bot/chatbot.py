import os
import openai

from llama_index.core import (
    StorageContext,
    ServiceContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool
from llama_index.agent.openai import OpenAIAgent

# Configurar la clave de API de OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")


class ChatBot:
    def __init__(
        self,
        llm: OpenAI = OpenAI(temperature=0.1, model="gpt-3.5-turbo"),
    ) -> None:
        # Crear directorios necesarios si no existen
        for directory in ["./data/storage", "./data/pdfs", "./data/latest"]:
            os.makedirs(directory, exist_ok=True)

        # Verificar si existe el almacenamiento persistente
        if not os.path.exists("./data/storage/docstore.json"):
            return

        # Crear contextos para el servicio y el almacenamiento
        storage_context = StorageContext.from_defaults(persist_dir="./data/storage")
        # service_context = ServiceContext.from_defaults(llm=llm)

        # Cargar el índice desde el almacenamiento
        index = load_index_from_storage(storage_context=storage_context)

        # Configurar memoria del chat
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

        # Configurar el motor de recuperación
        retriever = VectorIndexRetriever(index=index, similarity_top_k=5)
        query_engine = RetrieverQueryEngine(retriever=retriever)

        # Crear herramientas basadas en el motor de consulta
        query_engine_tool = QueryEngineTool.from_defaults(query_engine=query_engine)
        all_tools = [query_engine_tool]

        # Configurar el prompt del sistema
        system_prompt = "Sos el asistente virtual de un grupo de Telegram que tiene como contexto un documento."

        # Crear el agente
        self._agent = OpenAIAgent.from_tools(
            tools=all_tools,
            llm=llm,
            memory=memory,
            system_prompt=system_prompt,
            # service_context=service_context,
        )
        self._chat_history = []

    def reset(self) -> None:
        """Reinicia el historial de chat."""
        self._chat_history = []

    def get_sources_url(self, source_nodes: list) -> list:
        """Obtiene las URLs de las fuentes del chat."""
        sources = []
        for source in source_nodes:
            metadata = source.node.metadata
            if "url" in metadata:
                url = metadata["url"]
                if url not in sources:
                    sources.append(url)
        return sources

    def chat(self, input_text: str) -> object:
        """Envía un mensaje al agente y retorna la respuesta."""
        try:
            self._chat_history.append({"role": "user", "content": input_text})
            response = self._agent.chat(input_text)
            sources = self.get_sources_url(response.source_nodes)
            print(sources)
            return response.response

        except Exception as e:
            print(f"Error: {e}")
