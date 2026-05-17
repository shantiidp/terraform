import logging
from pathlib import Path

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, RiskLevel
from agentic_ai.security.sentinel_connector import SentinelConnector


PROMPTS_DIR = Path(__file__).parent / "prompts"


class SecurityAgent:
    def __init__(
        self,
        kernel: Kernel,
        governance: GovernanceGate,
        sentinel: SentinelConnector,
        logger: logging.Logger,
    ) -> None:
        self.kernel = kernel
        self.governance = governance
        self.sentinel = sentinel
        self.logger = logger

    async def assess_incidents(self) -> list[dict]:
        self.logger.info("Scanning for security incidents")
        incidents = await self.sentinel.get_recent_incidents(hours=4)

        results = []
        for incident in incidents:
            self.logger.info("Assessing incident: %s (%s)", incident.title, incident.severity)

            details = await self.sentinel.get_incident_details(incident.incident_id)
            prompt = (PROMPTS_DIR / "assess_threat.txt").read_text()

            response = await self.kernel.invoke_prompt(
                prompt=prompt,
                arguments=KernelArguments(
                    incident_data=str(details),
                    defender_data="",
                    rbac_state="",
                ),
                template_format="semantic-kernel",
            )

            results.append({
                "incident_id": incident.incident_id,
                "title": incident.title,
                "severity": incident.severity,
                "assessment": str(response)[:1000],
            })

        return results

    async def remediate(self, incident_id: str, action_description: str, risk: RiskLevel) -> bool:
        action = AgentAction(
            agent_name="security",
            action_type="security_remediation",
            description=f"Incident {incident_id}: {action_description}",
            risk_level=risk,
        )

        approval = await self.governance.request_approval(action)
        if not approval.approved:
            self.logger.warning("Security remediation rejected: %s", approval.reason)
            return False

        self.logger.info("Executing security remediation for incident %s", incident_id)
        return True
