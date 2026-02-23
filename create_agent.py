import asyncio
import os
import argparse
from typing import Optional
from azure.ai.projects.aio import AIProjectClient

from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool
from app.infrastructure.repository.azure_credential_repository import AzureCredentialRepository, CredentialType

async def create_agent(
    azure_foundry_endpoint: str,
    model_deployment_name: str,
    agent_name: str,
    instructions: str,
    description: Optional[str] = None,
    vector_store_name: Optional[str] = None, 
    vector_store_ids: Optional[str] = None
):
    credentials = AzureCredentialRepository().get_credential(CredentialType.CLIENT)
    ai_project_client = AIProjectClient(endpoint=azure_foundry_endpoint, credential=credentials)
    vector_stores_ids_list = []

    async with ai_project_client.get_openai_client() as open_ai_client:

        ai_project_client

        if vector_store_name is not None:
            vector_store = await open_ai_client.vector_stores.create(name=vector_store_name)
            print(f"Vector store created with id {vector_store.id}")
            vector_stores_ids_list.append(vector_store.id)

        if vector_store_ids is not None:
            vector_store_ids = vector_store_ids.split(",")
            vector_stores_ids_list = [*vector_stores_ids_list, *vector_store_ids]

        tool = FileSearchTool(vector_store_ids=vector_stores_ids_list)
    
        agent = await ai_project_client.agents.create_version(
            agent_name=agent_name,
            definition=PromptAgentDefinition(
                model=model_deployment_name,
                instructions=instructions,
                tools=[tool],
            ),
            description=description,
        )
        
        print("Total vector stores", vector_stores_ids_list)
        print(f"Agent created with (id: {agent.id}, name: {agent.name}, version: {agent.version})")
        print(f"Please set agent name: {agent_name} and version {agent.version} as env variable")

    await ai_project_client.close()

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Descripción de mi programa')
    parser.add_argument('--agent-name', help='Agent Name, recomend to finish with -agent')
    parser.add_argument('--agent-instructions', help='Prompt Agent')
    parser.add_argument('--agent-description', help='Little description of agent')
    parser.add_argument('--vs-name', help='Little description of agent')
    parser.add_argument('--vs-ids', help='Little description of agent')

    args = parser.parse_args()

    azure_foundry_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME")
    
    asyncio.run(create_agent(
        azure_foundry_endpoint,
        model_deployment_name,
        args.agent_name,
        args.agent_instructions,
        args.agent_description,
        args.vs_name,
        args.vs_ids
    ))
