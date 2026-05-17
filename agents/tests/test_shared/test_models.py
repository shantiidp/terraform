import pytest
from pydantic import ValidationError

from agentic_ai.shared.models import (
    AgentAction,
    ApprovalResponse,
    CapacityForecast,
    CostRecommendation,
    RiskLevel,
)


def test_agent_action_defaults():
    action = AgentAction(agent_name="test", action_type="read", description="test action")
    assert action.risk_level == RiskLevel.LOW
    assert action.correlation_id == ""


def test_cost_recommendation_confidence_bounds():
    rec = CostRecommendation(
        resource_id="/sub/rg/vm1",
        resource_name="vm1",
        current_sku="Standard_D4s_v3",
        recommended_sku="Standard_D2s_v3",
        estimated_monthly_savings=150.0,
        confidence=0.85,
        reasoning="Low CPU utilization",
    )
    assert 0 <= rec.confidence <= 1

    with pytest.raises(ValidationError):
        CostRecommendation(
            resource_id="x",
            resource_name="x",
            current_sku="x",
            recommended_sku="x",
            estimated_monthly_savings=0,
            confidence=1.5,
            reasoning="x",
        )


def test_capacity_forecast_confidence_bounds():
    with pytest.raises(ValidationError):
        CapacityForecast(
            resource_type="CPU",
            current_utilization=50.0,
            predicted_utilization=70.0,
            forecast_window_hours=24,
            scaling_recommendation="none",
            confidence=-0.1,
        )
