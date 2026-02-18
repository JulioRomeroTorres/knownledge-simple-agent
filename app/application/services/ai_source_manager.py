from typing import List, Any
from app.domain.repository.document_repository import IDocumentRepository
from app.domain.repository.storage_repository import IStorageRepository
from app.domain.repository.ai_project_repository import IAiProjectRepository
from app.config import get_settings

class AiSourceManager:
    def __init__(
                self,
                document_repository: IDocumentRepository,
                ai_repository: IAiProjectRepository                
                ) -> None:
        self.document_repository = document_repository
        self.ai_repository = ai_repository
        self.settigs = get_settings()
        pass

    async def save_document_locally(self, file):
        return await self.document_repository.save_document_locally(file)

    async def upload_to_vector_store(self, file_path: str) -> str:
        return await self.ai_repository.upload_to_vector_store(self.settigs.vector_store_id, file_path)

    async def get_files_from_vector_store(self) -> List[Any]:
        return await self.ai_repository.get_files_from_vector_store(self.settigs.vector_store_id)

    async def delete_file_from_vector_store(self, document_id: str) -> List[Any]:
        return await self.ai_repository.delete_file_from_vector_store(self.settigs.vector_store_id, document_id)
