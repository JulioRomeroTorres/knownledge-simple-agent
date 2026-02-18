import logging
from typing import Annotated, Optional
from fastapi import APIRouter, UploadFile, File, Form

from starlette.responses import JSONResponse

from app.presentation.api.dependencies import (
    get_handle_knownledge_use_case,

)
from app.presentation.api.dto import (
    UploadedKnownledgeDocumentResponse
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

    handle_knownlege_documents = get_handle_knownledge_use_case()

    vector_store_file_id = await handle_knownlege_documents.upload_document(file)

    uploaded_document = UploadedKnownledgeDocumentResponse(
        vector_store_file_id=vector_store_file_id,
        file_name=file.filename,
        id=""
    )
    
    return JSONResponse(uploaded_document.model_dump(), headers={"status_code": "200"})

@router.get("/")
async def get_documents():

    handle_knownlege_documents = get_handle_knownledge_use_case()
    vector_store_documents = handle_knownlege_documents.get_documents()

    return JSONResponse(vector_store_documents, headers={"status_code": "200"})

@router.delete("/{document_id}/")
async def delete_document(document_id: str):

    handle_knownlege_documents = get_handle_knownledge_use_case()
    handle_knownlege_documents.delete_document(document_id)

    return JSONResponse({}, headers={"status_code": "200"})

    
