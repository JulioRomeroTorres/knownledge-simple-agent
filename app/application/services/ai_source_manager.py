import shutil
from typing import List
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

    async def get_files_from_vector_store(self) -> str:
        return await self.ai_repository.get_files_from_vector_store(self.settigs.vector_store_id)
