import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AgentConfig:
    openai_endpoint: str
    openai_deployment: str
    key_vault_uri: str
    log_analytics_workspace_id: str
    agent_name: str
    environment: str
    approval_workflow_url: str

    @classmethod
    def from_env(cls) -> "AgentConfig":
        return cls(
            openai_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            openai_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
            key_vault_uri=os.environ["KEY_VAULT_URI"],
            log_analytics_workspace_id=os.environ.get("LOG_ANALYTICS_WORKSPACE_ID", ""),
            agent_name=os.environ.get("AGENT_NAME", "unknown"),
            environment=os.environ.get("ENVIRONMENT", "dev"),
            approval_workflow_url=os.environ.get("APPROVAL_WORKFLOW_URL", ""),
        )
