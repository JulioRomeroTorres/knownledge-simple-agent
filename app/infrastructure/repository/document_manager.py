import shutil
from typing import Any, List
from app.domain.repository.document_repository import IDocumentRepository
from app.domain.utils import parrallel_pdf_to_img

class DocumentManagerRepository(IDocumentRepository):
    def __init__(self):
        pass

    async def save_document_locally(self, file: Any) -> str:
        local_file_path = f"uploads/{file.filename}"
        try:
            with open(local_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            return local_file_path
        except Exception as e:
            print({"message": f"There was an error uploading the file: {e}"})
            raise
        finally:
            await file.close()

    def process_document(self, local_file_path: str) -> List[str]:
        return parrallel_pdf_to_img(local_file_path)

