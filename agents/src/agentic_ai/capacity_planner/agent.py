import logging
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, CapacityForecast, RiskLevel


PROMPTS_DIR = Path(__file__).parent / "prompts"


class CapacityPlannerAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger) -> None:
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def forecast(self, resource_type: str, forecast_hours: int = 24) -> CapacityForecast:
        self.logger.info("Forecasting capacity for %s over %dh", resource_type, forecast_hours)

        monitor_plugin = self.kernel.get_plugin("monitor_query")
        metrics = await monitor_plugin["run_kql_query"].invoke(
            self.kernel,
            query=f"Perf | where ObjectName == '{resource_type}' | summarize avg(CounterValue) by bin(TimeGenerated, 1h) | order by TimeGenerated desc | take 168",
            timespan_hours=168,
        )

        prompt = (PROMPTS_DIR / "forecast.txt").read_text()

        response = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                metrics_data=str(metrics),
                resource_config="",
                forecast_hours=str(forecast_hours),
            ),
            template_format="semantic-kernel",
        )

        forecast = CapacityForecast(
            resource_type=resource_type,
            current_utilization=0.0,
            predicted_utilization=0.0,
            forecast_window_hours=forecast_hours,
            scaling_recommendation=str(response)[:500],
            confidence=0.7,
        )

        if forecast.predicted_utilization > 80:
            action = AgentAction(
                agent_name="capacity_planner",
                action_type="pre_scale_resource",
                description=f"Pre-scale {resource_type}: predicted {forecast.predicted_utilization}% utilization",
                risk_level=RiskLevel.MEDIUM,
            )
            await self.governance.request_approval(action)

        return forecast
