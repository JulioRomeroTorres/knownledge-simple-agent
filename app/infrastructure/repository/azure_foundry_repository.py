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

    async def upload_to_vector_store(self, vector_store_id: str, file_full_path: str) -> str:
        async with self.ai_project_client.get_openai_client() as open_ai_client:

            additional_attributes = {
                "file_name": file_full_path.split("/")[-1]
            }

            file = await open_ai_client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store_id, file=open(file_full_path, "rb"),
                attributes=additional_attributes
            )
            
            return file.id
        
    async def get_files_from_vector_store(self, vector_store_id: str) -> List[Any]:
        async with self.ai_project_client.get_openai_client() as open_ai_client:
            files = open_ai_client.vector_stores.files.list(vector_store_id)
            original_files = []

            async for file in files:
                original_files.append(file)

            return files
    
    async def delete_file_from_vector_store(self, vector_store_id: str, file_id: str) -> Any:
        async with self.ai_project_client.get_openai_client() as open_ai_client:
            return await open_ai_client.vector_stores.files.delete(file_id, vector_store_id)

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

    async def create_vector_store(self, name: str):
        async with self.ai_project_client.get_openai_client() as open_ai_client:
            vector_store = await open_ai_client.vector_stores.create(name="ProductInfoStore")
            print(f"Vector store created (id: {vector_store.id})")
            return vector_store
    
    async def stream_chat(
                self, conversation_id: str, 
                formated_input: JsonArrayType, agent_information: Tuple[str, str]):
        agent_name, agent_version = agent_information

        async with self.ai_project_client.get_openai_client() as open_ai_client:
            stream_response = await open_ai_client.responses.create(
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
            )

            async for event in stream_response:
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

    #vector_store = await foundry_repository.create_vector_store("Test")
    #await foundry_repository.upload_to_vector_store(vector_store.id, "tmp/JulioCv.pdf")
    #await foundry_repository.upload_to_vector_store("vs_JG7nBSCxIz9Oyz6uLcqjDaEC", "tmp/Julio2Cv.pdf")

    data = await foundry_repository.get_files_from_vector_store("vs_JG7nBSCxIz9Oyz6uLcqjDaEC")
    print("Datos", data)
    """conversation = await foundry_repository.create_thread()
    image_input_list = ["https://stacaiaseu2d05.blob.core.windows.net/ctnreu2aiasd02/page_0.jpg?se=2026-02-18T01%3A17%3A02Z&sp=r&sv=2026-02-06&sr=b&skoid=f3fcc274-7e1f-4823-83d3-da05e9c0cfe9&sktid=5d93ebcc-f769-4380-8b7e-289fc972da1b&skt=2026-02-18T00%3A35%3A02Z&ske=2026-02-18T01%3A37%3A02Z&sks=b&skv=2026-02-06&sig=GJfTX9QrcUn5SWfeDJUHAi/rvWM55bhqwNlbpEpMlaE%3D"]
    image_input_list = []

    formatted_data = AzureFoundryRepository.format_user_input("Holaaaaa ¿en que ha trabajado Maxiel Olano?", image_input_list)
    agent_information = ("simple-knownledge-base-agent", "2")

    response = await foundry_repository.chat(conversation.id, formatted_data, agent_information)
    await foundry_repository.stream_chat(conversation.id, formatted_data, agent_information)
    print("Response Agent", response)"""

    await ai_projet_client.close()

if __name__ == "__main__":
    asyncio.run(main())



