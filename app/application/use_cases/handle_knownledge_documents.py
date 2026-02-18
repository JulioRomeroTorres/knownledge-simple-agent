from typing import List
from app.application.services.ai_source_manager import AiSourceManager
from fastapi import UploadFile

class HandleKnownledgeDocumentsUseCase:
    def __init__(self, ai_source_manager: AiSourceManager):
        self.ai_source_manager = ai_source_manager
        pass
    
    async def upload_document(self, file: UploadFile) -> List[str]:
        local_file_path = await self.ai_source_manager.save_document_locally(file)

        processed_files = self.process_file_by_content_type(file, local_file_path)
        return await self.document_manager.upload_to_bucket(processed_files)


        