from unittest.mock import AsyncMock, MagicMock

import pytest

from agentic_ai.security.agent import SecurityAgent
from agentic_ai.security.sentinel_connector import SecurityIncident
from agentic_ai.shared.models import ApprovalResponse, RiskLevel


@pytest.mark.asyncio
async def test_assess_incidents_empty(mock_kernel, mock_governance, logger):
    sentinel = MagicMock()
    sentinel.get_recent_incidents = AsyncMock(return_value=[])

    agent = SecurityAgent(mock_kernel, mock_governance, sentinel, logger)
    results = await agent.assess_incidents()

    assert results == []


@pytest.mark.asyncio
async def test_assess_incident_with_data(mock_kernel, mock_governance, logger):
    incident = SecurityIncident(
        incident_id="INC-001",
        title="Suspicious login",
        severity="High",
        status="Active",
        description="Multiple failed logins detected",
        related_alerts=[],
    )
    sentinel = MagicMock()
    sentinel.get_recent_incidents = AsyncMock(return_value=[incident])
    sentinel.get_incident_details = AsyncMock(return_value={"incident_id": "INC-001"})

    agent = SecurityAgent(mock_kernel, mock_governance, sentinel, logger)
    results = await agent.assess_incidents()

    assert len(results) == 1
    assert results[0]["incident_id"] == "INC-001"


@pytest.mark.asyncio
async def test_remediate_requires_approval(mock_kernel, mock_governance, logger):
    mock_governance.request_approval = AsyncMock(
        return_value=ApprovalResponse(approved=False, reason="Too risky")
    )
    sentinel = MagicMock()

    agent = SecurityAgent(mock_kernel, mock_governance, sentinel, logger)
    result = await agent.remediate("INC-001", "Block IP", RiskLevel.HIGH)

    assert result is False
