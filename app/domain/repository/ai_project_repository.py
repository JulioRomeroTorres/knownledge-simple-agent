from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

JsonType = Dict[str, Any]
JsonArrayType = List[JsonType]

class IAiProjectRepository(ABC):
    @abstractmethod
    async def create_thread() -> str:
        pass

    async def upload_to_vector_store(self, vector_store_id: str, file_full_path: str) -> str:
        pass

    async def chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]) -> str:
        pass

    async def create_vector_store(self, name: str) -> None:
        pass
    
    async def stream_chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]):
        pass