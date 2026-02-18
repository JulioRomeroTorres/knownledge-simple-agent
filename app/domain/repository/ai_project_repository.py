from abc import ABC, abstractmethod

class IAiProjectRepository(ABC):
    @abstractmethod
    async def create_thread() -> str:
        pass