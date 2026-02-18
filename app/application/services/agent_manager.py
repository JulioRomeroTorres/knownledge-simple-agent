import logging
from typing import List, Any, Dict, Coroutine, Optional, AsyncIterable
from app.domain.repository.item_sql_repository import IItemSqlRepository

from app.domain.repository.content_safety_repository import IContentSafetyRepository
from app.domain.repository.ai_project_repository import IAiProjectRepository
from app.domain.agent_core.service import IAgentCore, IBaseAgentFactory

from app.domain.contants import DecisionAction
from app.domain.exceptions import ThreadNotFound, GuardialError
from app.domain.utils import get_metadata_from_uri

from agent_framework import (
    ChatAgent, AgentRunResponse, AgentRunResponseUpdate,
    UriContent, TextContent, BaseContent, ChatMessage, DataContent
    )

from app.config import get_settings

logger = logging.getLogger(__name__)

JsonType = Dict[str, Any]
JsonArrayType = List[JsonType]

class AgentManager:
    def __init__(
                self,
                agent_core: IAiProjectRepository,
                content_safety_repository: IContentSafetyRepository
                ) -> None:
        settings = get_settings()

        self.content_safety_repository = content_safety_repository
        self.agent_core =  agent_core
        self.agent_name = "simple-knownledge-base-agent"
        self.agent_version = ""
        self.agent_information = (self.agent_name, self.agent_version)

    def prepare_content(
                    self, message: str, additional_files: Optional[List[str]] = []
                ) -> JsonArrayType:
        
        return self.agent_core.format_user_input(message, additional_files)

    async def generate_stream_content(self, message: str, additional_files: Optional[List[str]] = [], 
                                      conversation_id: str = "") -> AsyncIterable[AgentRunResponseUpdate]:
        content = self.prepare_content(message, additional_files)
        stream_response = self.agent_core.stream_chat(conversation_id, content, self.agent_information)
        async for event in stream_response:
            yield event
    
    async def generate_content(self, message: str, additional_files: Optional[List[str]] = [], conversation_id: str = "") -> AgentRunResponse:
        content = self.prepare_content(message, additional_files)
        agent_response = await self.agent_core.chat(conversation_id, content, self.agent_information)
        return agent_response
    
    async def apply_guardial(self, message: str, reject_thresholds: Dict[str, Any], blocklist_names: Optional[List[str]] = []) -> None:
        analysis_result = await self.content_safety_repository.analyze_text(message, blocklist_names)
        decision, thresholds_results = self.content_safety_repository.make_decision(analysis_result, reject_thresholds)

        print(f"Content Safety Analysis -> Decicion: {decision} results: {thresholds_results}")

        if decision == DecisionAction.REJECT:
            raise GuardialError(message, thresholds_results)
        
