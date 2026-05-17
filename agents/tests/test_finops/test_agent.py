from unittest.mock import AsyncMock, MagicMock

import pytest

from agentic_ai.finops.agent import FinOpsAgent
from agentic_ai.shared.models import ApprovalResponse


@pytest.mark.asyncio
async def test_analyze_costs_returns_list(mock_kernel, mock_governance, logger):
    cost_plugin = MagicMock()
    cost_plugin.__getitem__ = MagicMock(
        side_effect=lambda key: MagicMock(invoke=AsyncMock(return_value="mock cost data"))
    )
    mock_kernel.get_plugin.return_value = cost_plugin

    agent = FinOpsAgent(mock_kernel, mock_governance, logger)
    result = await agent.analyze_costs("/subscriptions/test-sub")

    assert isinstance(result, list)
    mock_kernel.invoke_prompt.assert_called_once()


@pytest.mark.asyncio
async def test_execute_recommendation_requires_approval(mock_kernel, mock_governance, logger):
    mock_governance.request_approval = AsyncMock(
        return_value=ApprovalResponse(approved=False, reason="Denied")
    )

    from agentic_ai.shared.models import CostRecommendation
    rec = CostRecommendation(
        resource_id="/sub/rg/vm1",
        resource_name="vm1",
        current_sku="D4s_v3",
        recommended_sku="D2s_v3",
        estimated_monthly_savings=100,
        confidence=0.9,
        reasoning="Low utilization",
    )

    agent = FinOpsAgent(mock_kernel, mock_governance, logger)
    result = await agent.execute_recommendation(rec)
    assert result is False
