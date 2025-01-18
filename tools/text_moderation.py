from collections.abc import Generator
from typing import Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class TextModerationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Ensure runtime and credentials
        if not self.runtime or not self.runtime.credentials:
            raise Exception("Tool runtime or credentials are missing")

        api_endpoint = self.runtime.credentials.get("api_endpoint")
        api_key = self.runtime.credentials.get("api_key")

        if not api_endpoint:
            raise Exception("Azure Content Safety endpoint is required")
        if not api_key:
            raise Exception("Azure API key is required")

        # Get Input Parameters
        input_text: str = tool_parameters.get("input_text") or ""

        if not input_text:
            raise Exception("Input text is required")

        try:
            # Create the client
            client = ContentSafetyClient(
                endpoint=api_endpoint,
                credential=AzureKeyCredential(api_key),
            )

            request = AnalyzeTextOptions(text=input_text)

            # Analyze the text
            result = client.analyze_text(request)

            # Yield the result
            yield self.create_json_message(result.as_dict())

        except Exception as e:
            raise Exception(f"Error analyzing text: {str(e)}") from e
