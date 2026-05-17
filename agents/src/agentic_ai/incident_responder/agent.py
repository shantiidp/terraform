import logging
from pathlib import Path
from typing import Any

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments

from agentic_ai.shared.governance import GovernanceGate
from agentic_ai.shared.models import AgentAction, IncidentDiagnosis, RiskLevel
from agentic_ai.incident_responder.runbooks import get_runbook, list_runbooks


PROMPTS_DIR = Path(__file__).parent / "prompts"


class IncidentResponderAgent:
    def __init__(self, kernel: Kernel, governance: GovernanceGate, logger: logging.Logger) -> None:
        self.kernel = kernel
        self.governance = governance
        self.logger = logger

    async def diagnose(self, alert_payload: dict[str, Any]) -> IncidentDiagnosis:
        self.logger.info("Diagnosing alert: %s", alert_payload.get("alertId", "unknown"))

        monitor_plugin = self.kernel.get_plugin("monitor_query")
        recent_logs = await monitor_plugin["run_kql_query"].invoke(
            self.kernel,
            query="AzureActivity | where TimeGenerated > ago(1h) | take 50",
            timespan_hours=1,
        )

        analysis_prompt = (PROMPTS_DIR / "diagnose.txt").read_text()

        response = await self.kernel.invoke_prompt(
            prompt=analysis_prompt,
            arguments=KernelArguments(
                alert_data=str(alert_payload),
                recent_logs=str(recent_logs),
                available_runbooks=list_runbooks(),
            ),
            template_format="semantic-kernel",
        )

        diagnosis = self._parse_diagnosis(str(response), alert_payload)
        self.logger.info(
            "Diagnosis: root_cause=%s severity=%s auto_remediate=%s",
            diagnosis.root_cause[:80],
            diagnosis.severity,
            diagnosis.auto_remediate,
        )

        if diagnosis.auto_remediate and diagnosis.runbook_id:
            await self._execute_runbook(diagnosis)

        return diagnosis

    async def _execute_runbook(self, diagnosis: IncidentDiagnosis) -> bool:
        runbook = get_runbook(diagnosis.runbook_id)
        if not runbook:
            self.logger.error("Runbook not found: %s", diagnosis.runbook_id)
            return False

        action = AgentAction(
            agent_name="incident_responder",
            action_type=runbook.action_type,
            description=f"Execute runbook '{runbook.name}': {diagnosis.recommended_action}",
            risk_level=runbook.risk_level,
        )

        approval = await self.governance.request_approval(action)
        if not approval.approved:
            self.logger.warning("Runbook execution rejected: %s", approval.reason)
            return False

        self.logger.info("Executing runbook: %s", runbook.id)
        return True

    def _parse_diagnosis(self, llm_output: str, alert: dict[str, Any]) -> IncidentDiagnosis:
        return IncidentDiagnosis(
            alert_id=alert.get("alertId", "unknown"),
            severity=alert.get("severity", "medium"),
            root_cause=llm_output[:500],
            recommended_action="See full diagnosis output",
            risk_level=RiskLevel.MEDIUM,
            auto_remediate=False,
            runbook_id="",
        )
