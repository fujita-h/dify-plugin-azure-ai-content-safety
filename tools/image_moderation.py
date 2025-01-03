import io
from collections.abc import Generator
from typing import Any

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData
from azure.core.credentials import AzureKeyCredential
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class ImageModerationTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # Ensure runtime and credentials
        if not self.runtime or not self.runtime.credentials:
            raise Exception("Tool runtime or credentials are missing")

        api_endpoint = self.runtime.credentials.get("azure_ai_content_safety_api_endpoint")
        api_key = self.runtime.credentials.get("azure_ai_content_safety_api_key")

        if not api_endpoint:
            raise Exception("Azure Content Safety endpoint is required")
        if not api_key:
            raise Exception("Azure API key is required")

        # Get file
        file = tool_parameters.get("input_file")
        if not file:
            raise ValueError("File is required")

        try:
            # Create the client
            client = ContentSafetyClient(
                endpoint=api_endpoint,
                credential=AzureKeyCredential(api_key),
            )

            file_binary = io.BytesIO(file.blob)
            request = AnalyzeImageOptions(image=ImageData(content=file_binary.getvalue()))

            # Analyze the image
            result = client.analyze_image(request)

            # Yield the result
            yield self.create_json_message(result.as_dict())

        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}") from e
