from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional

JsonType = Dict[str, Any]
JsonArrayType = List[JsonType]

class IAiProjectRepository(ABC):
    
    @classmethod
    def format_user_input(cls, message: str, image_input_list: Optional[List[str]] = []) -> JsonArrayType:
        
        image_content = [ 
            {
                "type": "input_image",
                "detail": "auto",
                "image_url": image_input
            } for image_input in image_input_list
        ]

        text_content = [{"type": "input_text", "text": message}]

        return [
            {
                "type": "message",
                "role": "user",
                "content": [
                  *image_content,
                  *text_content
                ],
            }
        ]

    @abstractmethod
    async def create_thread() -> str:
        pass
    
    @abstractmethod
    async def upload_to_vector_store(self, vector_store_id: str, file_full_path: str) -> str:
        pass

    @abstractmethod
    async def delete_file_from_vector_store(self, vector_store_id: str, vector_store_file_id: str):
        pass

    @abstractmethod
    async def get_files_from_vector_store(self, vector_store_id: str) -> List[Any]:
        pass

    @abstractmethod
    async def chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]) -> str:
        pass

    @abstractmethod
    async def create_vector_store(self, name: str) -> None:
        pass
    
    @abstractmethod
    async def stream_chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]):
        pass