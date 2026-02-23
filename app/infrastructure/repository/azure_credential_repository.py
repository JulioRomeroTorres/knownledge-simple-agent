from app.config import Settings
from enum import Enum
from azure.identity.aio import DefaultAzureCredential, ClientSecretCredential

class CredentialType(Enum):
    DEFAULT = "default"
    CLIENT = "client"

class AzureCredentialRepository:
    def get_credential(self, type: CredentialType) -> str:
        if type == CredentialType.CLIENT:
            print("Using ClientSecretCredential for Azure authentication")
            
            settings = Settings()
            return ClientSecretCredential(
                tenant_id=settings.azure_tenant_id,
                client_id=settings.azure_client_id,
                client_secret=settings.azure_client_secret
            )
        
        return DefaultAzureCredential()
            