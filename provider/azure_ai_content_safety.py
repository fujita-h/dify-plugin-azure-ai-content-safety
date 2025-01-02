from typing import Any

from azure.ai.contentsafety import BlocklistClient
from azure.core.credentials import AzureKeyCredential
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AzureAiContentSafetyProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            api_endpoint = credentials.get("azure_ai_content_safety_api_endpoint")
            api_key = credentials.get("azure_ai_content_safety_api_key")

            # Ensure API key and endpoint are provided
            if not api_key:
                raise Exception("Azure AI Vision API key is missing")
            if not api_endpoint:
                raise Exception("Azure AI Vision API endpoint is missing")

            # Test the credentials by getting the blocklist
            client = BlocklistClient(
                endpoint=api_endpoint,
                credential=AzureKeyCredential(api_key),
            )
            _ = client.get_text_blocklist("")

        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e)) from e
