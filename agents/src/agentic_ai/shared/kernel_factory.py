from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from agentic_ai.shared.auth import get_credential
from agentic_ai.shared.config import AgentConfig


def create_kernel(config: AgentConfig, plugins: list | None = None) -> Kernel:
    kernel = Kernel()

    credential = get_credential()
    token = credential.get_token("https://cognitiveservices.azure.com/.default")

    chat_service = AzureChatCompletion(
        deployment_name=config.openai_deployment,
        endpoint=config.openai_endpoint,
        api_key=token.token,
        api_version="2024-08-01-preview",
    )
    kernel.add_service(chat_service)

    if plugins:
        for plugin in plugins:
            kernel.add_plugin(plugin)

    return kernel
