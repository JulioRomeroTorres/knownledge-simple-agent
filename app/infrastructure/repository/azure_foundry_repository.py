from app.domain.repository.ai_project_repository import IAiProjectRepository
from typing import List, Any, Dict, Tuple, Optional
from azure.ai.projects.aio import AIProjectClient

from azure.identity.aio import DefaultAzureCredential
import asyncio

JsonType = Dict[str, Any]
JsonArrayType = List[JsonType]

class AzureFoundryRepository(IAiProjectRepository):
    def __init__(self, ai_project_client: AIProjectClient):
        self.ai_project_client = ai_project_client
        pass

    async def create_thread(self):
        async with self.ai_project_client.get_openai_client() as open_ai_client:
            created_conversation = await open_ai_client.conversations.create()
            return created_conversation
    
    @classmethod
    def format_user_input(cls, message: str, image_input_list: Optional[List[str]] = []) -> JsonType:
        
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

    async def index_document_into_vectorial_db(self, vector_store_id: str, file_full_path: str) -> str:
        async with self.ai_project_client.get_openai_client() as open_ai_client:
            file = await open_ai_client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store_id, file=open(file_full_path, "rb")
            )
            return file.id

    async def chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]) -> str:
        
        agent_name, agent_version = agent_information

        async with self.ai_project_client.get_openai_client() as open_ai_client:
            response = await open_ai_client.responses.create(
                conversation=conversation_id,
                input=formated_input,
                extra_body={
                    "agent": {
                        "name": agent_name, 
                        #"version": agent_version,
                        "type": "agent_reference"
                    }
                }
            )
            return response
    
    async def stream_chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]):
        agent_name, agent_version = agent_information

        async with self.ai_project_client.get_openai_client() as open_ai_client:
            async with open_ai_client.responses.create(
                conversation=conversation_id,
                input=formated_input,
                extra_body={
                    "agent": {
                        "name": agent_name, 
                        #"version": agent_version,
                        "type": "agent_reference"
                    }
                },
                stream=True
            ) as stream_response:
                for event in stream_response:
                    if event.type == "response.created":
                        print(f"Stream response created with ID: {event.response.id}\n")
                    elif event.type == "response.output_text.delta":
                        #yield(event.delta)
                        print("Delta Item", event.delta)
                    elif event.type == "response.text.done":
                        print(f"\n\nResponse text done. Access final text in 'event.text'")
                    elif event.type == "response.completed":
                        print(f"\n\nResponse completed. Access final text in 'event.response.output_text'")


async def main():
    ai_projet_client = AIProjectClient(endpoint="https://aaifaiaseu2d02.services.ai.azure.com/api/projects/AgentFramework", credential=DefaultAzureCredential())
    foundry_repository = AzureFoundryRepository(ai_projet_client)

    conversation = await foundry_repository.create_thread()
    formatted_data = AzureFoundryRepository.format_user_input("Holaaaaa")
    agent_information = ("simple-knownledge-base-agent", "v2")

    response = await foundry_repository.chat(conversation.id, formatted_data, agent_information)
    await foundry_repository.stream_chat(conversation.id, formatted_data, agent_information)
    print("Response Agent", response)

    await ai_projet_client.close()

if __name__ == "__main__":
    asyncio.run(main())



