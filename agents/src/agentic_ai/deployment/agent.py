import logging
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, DeploymentPlan, RiskLevel


PROMPTS_DIR = Path(__file__).parent / "prompts"


class DeploymentAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger) -> None:
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def plan_deployment(
        self,
        pipeline_info: str,
        target_env: str,
        changes: str,
    ) -> DeploymentPlan:
        self.logger.info("Planning deployment to %s", target_env)

        prompt = (PROMPTS_DIR / "plan_deploy.txt").read_text()

        response = await self.kernel.invoke_prompt(
            prompt=prompt,
            arguments=KernelArguments(
                pipeline_info=pipeline_info,
                target_env=target_env,
                changes=changes,
                deployment_history="",
                health_metrics="",
            ),
            template_format="semantic-kernel",
        )

        plan = DeploymentPlan(
            pipeline_id="pending",
            strategy="blue_green",
            target_environment=target_env,
            changes_summary=changes,
            risk_level=RiskLevel.HIGH if target_env == "prod" else RiskLevel.MEDIUM,
            rollback_plan=f"Revert to previous deployment in {target_env}",
        )

        action = AgentAction(
            agent_name="deployment",
            action_type="execute_deployment",
            description=f"Deploy to {target_env}: {changes[:100]}",
            risk_level=plan.risk_level,
        )
        approval = await self.governance.request_approval(action)

        if not approval.approved:
            self.logger.warning("Deployment rejected: %s", approval.reason)

        return plan
