from collections.abc import Generator
from typing import Any

import requests
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class PromptShieldsTool(Tool):
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

        # Get Input Parameters
        input_text: str = tool_parameters.get("input_text") or ""

        if not input_text:
            raise Exception("Prompt is required")

        try:
            # make the request
            endpoint = f"{api_endpoint}//contentsafety/text:shieldPrompt?api-version=2024-09-01"
            headers = {
                "Ocp-Apim-Subscription-Key": api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "userPrompt": input_text,
                "documents": [],
            }
            response = requests.post(endpoint, headers=headers, json=payload)
            if response.status_code != 200:
                raise Exception(f"Error on api reqeust: {response.status_code}")

            # Yield the result
            yield self.create_json_message(response.json())

        except Exception as e:
            raise Exception(f"Error analyzing prompt: {str(e)}") from e
