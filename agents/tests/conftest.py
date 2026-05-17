import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.logging import get_logger


@pytest.fixture(autouse=True)
def mock_env():
    env_vars = {
        "AZURE_OPENAI_ENDPOINT": "https://test-openai.openai.azure.com/",
        "AZURE_OPENAI_DEPLOYMENT": "gpt-4o",
        "KEY_VAULT_URI": "https://test-keyvault.vault.azure.net/",
        "LOG_ANALYTICS_WORKSPACE_ID": "test-workspace-id",
        "AGENT_NAME": "test_agent",
        "ENVIRONMENT": "test",
        "APPROVAL_WORKFLOW_URL": "https://test-logic-app.azurewebsites.net/api/approve",
    }
    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def config():
    return AgentConfig.from_env()


@pytest.fixture
def logger():
    return get_logger("test")


@pytest.fixture
def mock_governance(config, logger):
    gate = GovernanceGate(config, logger)
    return gate


@pytest.fixture
def mock_kernel():
    kernel = MagicMock()
    kernel.invoke_prompt = AsyncMock(return_value="mock LLM response")
    return kernel


@pytest.fixture
def mock_credential():
    credential = MagicMock()
    token = MagicMock()
    token.token = "mock-token"
    credential.get_token.return_value = token
    return credential
