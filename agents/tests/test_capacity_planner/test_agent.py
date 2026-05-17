from unittest.mock import AsyncMock, MagicMock

import pytest

from agentic_ai.capacity_planner.agent import CapacityPlannerAgent
from agentic_ai.capacity_planner.forecaster import MetricPoint, simple_linear_forecast
from agentic_ai.shared.models import CapacityForecast


def test_linear_forecast_increasing():
    points = [MetricPoint(f"t{i}", 40 + i * 2) for i in range(10)]
    result = simple_linear_forecast(points, forecast_hours=24, threshold=80.0)
    assert result.trend == "increasing"
    assert result.predicted_value > 40


def test_linear_forecast_stable():
    points = [MetricPoint(f"t{i}", 50.0) for i in range(10)]
    result = simple_linear_forecast(points, forecast_hours=24)
    assert result.trend == "stable"


def test_linear_forecast_single_point():
    points = [MetricPoint("t0", 60.0)]
    result = simple_linear_forecast(points, forecast_hours=24)
    assert result.confidence == 0.1


@pytest.mark.asyncio
async def test_forecast_returns_capacity_forecast(mock_kernel, mock_governance, logger):
    monitor_plugin = MagicMock()
    monitor_plugin.__getitem__ = MagicMock(
        side_effect=lambda key: MagicMock(invoke=AsyncMock(return_value="mock metrics"))
    )
    mock_kernel.get_plugin.return_value = monitor_plugin

    agent = CapacityPlannerAgent(mock_kernel, mock_governance, logger)
    result = await agent.forecast("Processor", forecast_hours=24)

    assert isinstance(result, CapacityForecast)
    assert result.resource_type == "Processor"
