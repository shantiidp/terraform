from unittest.mock import AsyncMock, patch

import pytest

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, RiskLevel


@pytest.mark.asyncio
async def test_low_risk_auto_approved(mock_governance):
    action = AgentAction(
        agent_name="test",
        action_type="read_resource",
        description="Read resource details",
        risk_level=RiskLevel.LOW,
    )
    response = await mock_governance.request_approval(action)
    assert response.approved is True
    assert response.auto_approved is True


@pytest.mark.asyncio
async def test_high_risk_requires_approval(config, logger):
    gate = GovernanceGate(config, logger)
    action = AgentAction(
        agent_name="test",
        action_type="restart_vm",
        description="Restart production VM",
        risk_level=RiskLevel.HIGH,
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None
        mock_post.return_value.json.return_value = {"approved": True, "approver": "admin@test.com"}

        response = await gate.request_approval(action)
        assert response.approved is True
        assert response.approver == "admin@test.com"


@pytest.mark.asyncio
async def test_medium_risk_requires_approval(config, logger):
    gate = GovernanceGate(config, logger)
    action = AgentAction(
        agent_name="test",
        action_type="resize_vm",
        description="Resize VM SKU",
        risk_level=RiskLevel.MEDIUM,
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = lambda: None
        mock_post.return_value.json.return_value = {"approved": False, "reason": "Rejected by admin"}

        response = await gate.request_approval(action)
        assert response.approved is False


@pytest.mark.asyncio
async def test_no_workflow_url_rejects(logger):
    from agentic_ai.shared.config import AgentConfig
    config = AgentConfig(
        openai_endpoint="https://test.openai.azure.com/",
        openai_deployment="gpt-4o",
        key_vault_uri="https://test.vault.azure.net/",
        log_analytics_workspace_id="test",
        agent_name="test",
        environment="test",
        approval_workflow_url="",
    )
    gate = GovernanceGate(config, logger)
    action = AgentAction(
        agent_name="test",
        action_type="delete_resource",
        description="Delete something",
        risk_level=RiskLevel.CRITICAL,
    )
    response = await gate.request_approval(action)
    assert response.approved is False
