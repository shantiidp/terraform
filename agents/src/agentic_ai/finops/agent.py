import logging
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, CostRecommendation, RiskLevel


PROMPTS_DIR = Path(__file__).parent / "prompts"


class FinOpsAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger) -> None:
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def analyze_costs(self, subscription_scope: str) -> list[CostRecommendation]:
        self.logger.info("Starting cost analysis for scope: %s", subscription_scope)

        cost_plugin = self.kernel.get_plugin("cost_query")
        cost_data = await cost_plugin["query_costs"].invoke(
            self.kernel, scope=subscription_scope
        )
        resource_costs = await cost_plugin["get_cost_by_resource"].invoke(
            self.kernel, scope=subscription_scope
        )

        system_prompt = (PROMPTS_DIR / "system.txt").read_text()
        analysis_prompt = (PROMPTS_DIR / "analyze_cost.txt").read_text()

        response = await self.kernel.invoke_prompt(
            prompt=analysis_prompt,
            arguments=KernelArguments(
                cost_data=str(cost_data),
                resource_details=str(resource_costs),
            ),
            template_format="semantic-kernel",
        )

        self.logger.info("Cost analysis complete")
        return self._parse_recommendations(str(response))

    async def execute_recommendation(self, recommendation: CostRecommendation) -> bool:
        action = AgentAction(
            agent_name="finops",
            action_type="apply_cost_recommendation",
            resource_id=recommendation.resource_id,
            description=f"Right-size {recommendation.resource_name}: {recommendation.current_sku} -> {recommendation.recommended_sku}",
            risk_level=RiskLevel.MEDIUM if recommendation.confidence > 0.8 else RiskLevel.HIGH,
        )

        approval = await self.governance.request_approval(action)
        if not approval.approved:
            self.logger.warning("Recommendation rejected: %s", approval.reason)
            return False

        self.logger.info("Executing recommendation for %s", recommendation.resource_name)
        return True

    def _parse_recommendations(self, llm_output: str) -> list[CostRecommendation]:
        # Placeholder: in production, parse structured LLM output into CostRecommendation objects
        self.logger.info("Parsing %d characters of LLM output", len(llm_output))
        return []
