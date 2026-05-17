import logging

import httpx

from agentic_ai.shared.config import AgentConfig
from agentic_ai.shared.logging import new_correlation_id
from agentic_ai.shared.models import (
    ActionStatus,
    AgentAction,
    ApprovalRequest,
    ApprovalResponse,
    RiskLevel,
)

AUTO_APPROVE_RISK_LEVELS = {RiskLevel.LOW}


class GovernanceGate:
    def __init__(self, config: AgentConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

    async def request_approval(self, action: AgentAction) -> ApprovalResponse:
        if not action.correlation_id:
            action.correlation_id = new_correlation_id()

        self.logger.info(
            "Governance gate: agent=%s action=%s risk=%s resource=%s cid=%s",
            action.agent_name,
            action.action_type,
            action.risk_level,
            action.resource_id,
            action.correlation_id,
        )

        if action.risk_level in AUTO_APPROVE_RISK_LEVELS:
            response = ApprovalResponse(
                approved=True,
                auto_approved=True,
                reason=f"Auto-approved: risk level {action.risk_level.value}",
            )
            self._log_decision(action, response, ActionStatus.APPROVED)
            return response

        return await self._request_human_approval(
            ApprovalRequest(action=action, requires_human_approval=True)
        )

    async def _request_human_approval(self, request: ApprovalRequest) -> ApprovalResponse:
        if not self.config.approval_workflow_url:
            self.logger.warning("No approval workflow URL configured; rejecting high-risk action")
            response = ApprovalResponse(approved=False, reason="No approval workflow configured")
            self._log_decision(request.action, response, ActionStatus.REJECTED)
            return response

        async with httpx.AsyncClient(timeout=request.timeout_seconds) as client:
            try:
                http_response = await client.post(
                    self.config.approval_workflow_url,
                    json=request.action.model_dump(mode="json"),
                )
                http_response.raise_for_status()
                data = http_response.json()

                response = ApprovalResponse(
                    approved=data.get("approved", False),
                    approver=data.get("approver", ""),
                    auto_approved=data.get("auto_approved", False),
                    reason=data.get("reason", ""),
                )
            except Exception as e:
                self.logger.error("Approval workflow failed: %s", e)
                response = ApprovalResponse(approved=False, reason=f"Workflow error: {e}")

        status = ActionStatus.APPROVED if response.approved else ActionStatus.REJECTED
        self._log_decision(request.action, response, status)
        return response

    def _log_decision(
        self, action: AgentAction, response: ApprovalResponse, status: ActionStatus
    ) -> None:
        self.logger.info(
            "Governance decision: cid=%s status=%s approved=%s approver=%s reason=%s",
            action.correlation_id,
            status.value,
            response.approved,
            response.approver,
            response.reason,
        )
