
from typing import Any, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.domain.utils import get_current_datetime

from enum import Enum

class OrderEnum(Enum):
    ASC = 'ASC'
    DESC = 'DESC'

class Message(BaseModel):
    role: str = Field(description="Role of the message sender (user, assistant, system)")
    content: str = Field(description="Message content")

class AgentTrace(BaseModel):
    enduser_id: Optional[str] = Field(
        default=None,
        description="User id"
    ),
    enduser_type: Optional[str] = Field(
        default=None,
        description="Bussiness Unit"
    ),
    biz_domain: Optional[str] = Field(
        default=None,
        description="Bussiness domian"
    ),
    biz_subdomain: Optional[str] = Field(
        default=None,
        description="Bussiness subdomian"
    ),
    biz_codapp: Optional[str] = Field(
        default=None,
        description="Bussiness Process"
    )
    
    def to_json(self)-> Dict[str, Any]:
        return {
            "identity.id": self.enduser_id,
            "identity.type": self.enduser_type,
            "identity.domain": self.biz_domain,
            "identity.subdomain": self.biz_subdomain,
            "identity.codapp": self.biz_codapp
        }

class PrimitiveConversationInformation(BaseModel):
    message: str = Field(description="Current user message")
    additional_files: Optional[List[str]] = Field(
        default_factory=list,
        description="List of attached files"
    )
class ConversationRequest(PrimitiveConversationInformation):
    trace: AgentTrace = Field(
        description="trace information"
    )
    additional_information: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional Params"
    )
    
class ConversationResponse(PrimitiveConversationInformation):
    timestamp: str = Field(description="Response timestamp", default=get_current_datetime())
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class CommonFilterParams(BaseModel):
    page: Optional[int] = 0
    limit: Optional[int] = 10
    order: Optional[str] = OrderEnum.DESC.value

class ConversationFilters(CommonFilterParams):
    pass
    
class UploadedDocumentResponse(BaseModel):
    generated_img_files: List[str] = Field(description="List of image file from pdf page")
    file_name: str = Field(description="File name")

class UploadedKnownledgeDocumentResponse(BaseModel):
    vector_store_file_id: str = Field(description="File id in vector store")
    file_name: str = Field(description="File name")
    id: str = Field(description="File id")
