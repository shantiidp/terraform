from unittest.mock import AsyncMock, MagicMock

import pytest

from agentic_ai.incident_responder.agent import IncidentResponderAgent
from agentic_ai.shared.models import IncidentDiagnosis


@pytest.mark.asyncio
async def test_diagnose_returns_diagnosis(mock_kernel, mock_governance, logger):
    monitor_plugin = MagicMock()
    monitor_plugin.__getitem__ = MagicMock(
        side_effect=lambda key: MagicMock(invoke=AsyncMock(return_value="mock logs"))
    )
    mock_kernel.get_plugin.return_value = monitor_plugin

    agent = IncidentResponderAgent(mock_kernel, mock_governance, logger)
    alert = {"alertId": "test-123", "severity": "high", "description": "CPU spike"}

    result = await agent.diagnose(alert)

    assert isinstance(result, IncidentDiagnosis)
    assert result.alert_id == "test-123"
    mock_kernel.invoke_prompt.assert_called_once()
