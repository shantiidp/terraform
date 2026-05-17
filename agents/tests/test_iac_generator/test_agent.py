from unittest.mock import AsyncMock, patch

import pytest

from agentic_ai.iac_generator.agent import IaCGeneratorAgent
from agentic_ai.iac_generator.validator import ValidationResult
from agentic_ai.shared.models import ApprovalResponse


@pytest.mark.asyncio
async def test_generate_calls_llm_and_validates(mock_kernel, mock_governance, logger):
    mock_governance.request_approval = AsyncMock(
        return_value=ApprovalResponse(approved=True, auto_approved=True)
    )

    mock_validation = ValidationResult(valid=True, errors=[], warnings=[])
    with patch("agentic_ai.iac_generator.agent.validate_terraform", return_value=mock_validation):
        agent = IaCGeneratorAgent(mock_kernel, mock_governance, logger)
        result = await agent.generate("Create a storage account", "eastus2", "dev")

    assert "hcl" in result
    assert result["valid"] is True
    mock_kernel.invoke_prompt.assert_called_once()
