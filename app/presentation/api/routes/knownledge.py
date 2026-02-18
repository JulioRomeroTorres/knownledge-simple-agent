import logging
from typing import Annotated, Optional
from fastapi import APIRouter, UploadFile, File, Form

from starlette.responses import JSONResponse

from app.presentation.api.dependencies import (
    get_handle_knownledge_use_case,

)
from app.presentation.api.dto import (
    UploadedDocumentResponse
)

logger = logging.getLogger(__name__)

BASE_PATH = "/api/v1/knownledge"

router = APIRouter(
    prefix=BASE_PATH
)

@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    username: Annotated[str, Form()] = "anonymous",
    description: Annotated[Optional[str], Form()] = None
    ):

    handle_knownlege = get_handle_knownledge_use_case()

    pdf_images_files = await handle_knownlege.upload_document(file)

    uploaded_document = UploadedDocumentResponse(
        generated_img_files=pdf_images_files,
        file_name=file.filename
    )
    
    return JSONResponse(uploaded_document.model_dump(), headers={"status_code": "200"})

@router.get("/")
async def get_documents(

    ):

    handle_document = get_handle_documents_use_case()

    return JSONResponse({}, headers={"status_code": "200"})

@router.delete("/{document_id}/")
async def delete_document(document_id: str):

    handle_document = get_handle_documents_use_case()

    pdf_images_files = await handle_document.index_document(file)

    uploaded_document = UploadedDocumentResponse(
        generated_img_files=pdf_images_files,
        file_name=file.filename
    )
    
    return JSONResponse(uploaded_document.model_dump(), headers={"status_code": "200"})

    
