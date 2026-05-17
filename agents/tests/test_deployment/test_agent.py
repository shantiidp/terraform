from unittest.mock import AsyncMock

import pytest

from agentic_ai.deployment.agent import DeploymentAgent
from agentic_ai.shared.models import ApprovalResponse, DeploymentPlan


@pytest.mark.asyncio
async def test_plan_deployment_returns_plan(mock_kernel, mock_governance, logger):
    mock_governance.request_approval = AsyncMock(
        return_value=ApprovalResponse(approved=True, approver="admin@test.com")
    )

    agent = DeploymentAgent(mock_kernel, mock_governance, logger)
    plan = await agent.plan_deployment(
        pipeline_info="pipeline-123",
        target_env="staging",
        changes="Updated API version",
    )

    assert isinstance(plan, DeploymentPlan)
    assert plan.target_environment == "staging"


@pytest.mark.asyncio
async def test_prod_deployment_is_high_risk(mock_kernel, mock_governance, logger):
    mock_governance.request_approval = AsyncMock(
        return_value=ApprovalResponse(approved=True)
    )

    agent = DeploymentAgent(mock_kernel, mock_governance, logger)
    plan = await agent.plan_deployment(
        pipeline_info="pipeline-456",
        target_env="prod",
        changes="Hotfix",
    )

    assert plan.risk_level.value == "high"
