from agentic_ai.shared.config import AgentConfig


def test_config_from_env(config):
    assert config.openai_endpoint == "https://test-openai.openai.azure.com/"
    assert config.openai_deployment == "gpt-4o"
    assert config.key_vault_uri == "https://test-keyvault.vault.azure.net/"
    assert config.agent_name == "test_agent"
    assert config.environment == "test"


def test_config_is_frozen(config):
    import pytest
    with pytest.raises(AttributeError):
        config.agent_name = "changed"
