from dataclasses import dataclass

from agentic_ai.shared.models import RiskLevel


@dataclass
class Runbook:
    id: str
    name: str
    description: str
    risk_level: RiskLevel
    auto_approve: bool
    action_type: str


RUNBOOKS: dict[str, Runbook] = {
    "restart_app_service": Runbook(
        id="restart_app_service",
        name="Restart App Service",
        description="Restarts an Azure App Service or Function App when health check fails",
        risk_level=RiskLevel.MEDIUM,
        auto_approve=False,
        action_type="Microsoft.Web/sites/restart/action",
    ),
    "restart_vm": Runbook(
        id="restart_vm",
        name="Restart Virtual Machine",
        description="Restarts a VM that is unresponsive",
        risk_level=RiskLevel.HIGH,
        auto_approve=False,
        action_type="Microsoft.Compute/virtualMachines/restart/action",
    ),
    "scale_up_app_service": Runbook(
        id="scale_up_app_service",
        name="Scale Up App Service Plan",
        description="Increases App Service Plan tier when CPU/memory consistently above 80%",
        risk_level=RiskLevel.MEDIUM,
        auto_approve=False,
        action_type="Microsoft.Web/serverfarms/write",
    ),
    "clear_disk_space": Runbook(
        id="clear_disk_space",
        name="Clear Temporary Files",
        description="Removes temporary files and old logs when disk usage exceeds 90%",
        risk_level=RiskLevel.LOW,
        auto_approve=True,
        action_type="custom/clear_disk",
    ),
}


def get_runbook(runbook_id: str) -> Runbook | None:
    return RUNBOOKS.get(runbook_id)


def list_runbooks() -> str:
    lines = []
    for rb in RUNBOOKS.values():
        lines.append(f"- {rb.id}: {rb.description} (risk: {rb.risk_level.value}, auto: {rb.auto_approve})")
    return "\n".join(lines)
