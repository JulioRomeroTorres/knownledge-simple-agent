import logging
from typing import Any, List
from app.domain.repository.ai_project_repository import IAiProjectRepository

logger = logging.getLogger(__name__)


class ThreadManager:

    def __init__(
            self, 
            ai_project_repository: IAiProjectRepository
        ):
        self.ai_project_repository = ai_project_repository

    async def get_threads(filters: Any) -> List[Any]:
        pass

    async def create_thread(self):
        return await self.ai_project_repository.create_thread()
        
    
