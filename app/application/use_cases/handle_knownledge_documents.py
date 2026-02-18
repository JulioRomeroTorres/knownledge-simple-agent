from typing import List, Any
from app.application.services.ai_source_manager import AiSourceManager
from fastapi import UploadFile

class HandleKnownledgeDocumentsUseCase:
    def __init__(self, ai_source_manager: AiSourceManager):
        self.ai_source_manager = ai_source_manager
        pass
    
    async def upload_document(self, file: UploadFile) -> str:
        local_file_path = await self.ai_source_manager.save_document_locally(file)
        return await self.ai_source_manager.upload_to_vector_store(local_file_path)

    async def get_documents(self) -> List[Any]:
        documents = await self.ai_source_manager.get_files_from_vector_store()
        return [ {"vector_store_file_id": doc.id, "created_at": doc.created_at} for doc in documents]

    async def delete_document(self, file_id: str):
        await self.ai_source_manager.delete_file_from_vector_store(file_id)



        