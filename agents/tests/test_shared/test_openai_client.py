from unittest.mock import MagicMock, patch

from agentic_ai.shared.openai_client import create_openai_client


def test_create_openai_client(config, mock_credential):
    with patch("agentic_ai.shared.openai_client.get_credential", return_value=mock_credential):
        client = create_openai_client(config)
        assert client is not None
        mock_credential.get_token.assert_called_once_with("https://cognitiveservices.azure.com/.default")
