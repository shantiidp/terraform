from openai import AsyncAzureOpenAI

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig


def create_openai_client(config: AgentConfig) -> AsyncAzureOpenAI:
    credential = get_credential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")

    return AsyncAzureOpenAI(
        azure_endpoint=config.openai_endpoint,
        azure_deployment=config.openai_deployment,
        api_version="2024-08-01-preview",
        api_key=token.token,
    )
