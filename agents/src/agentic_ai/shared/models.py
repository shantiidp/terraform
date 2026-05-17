from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ActionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    FAILED = "failed"


class AgentAction(BaseModel):
    agent_name: str
    action_type: str
    resource_id: str = ""
    description: str
    risk_level: RiskLevel = RiskLevel.LOW
    correlation_id: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ApprovalRequest(BaseModel):
    action: AgentAction
    requires_human_approval: bool = False
    timeout_seconds: int = 300


class ApprovalResponse(BaseModel):
    approved: bool
    approver: str = ""
    auto_approved: bool = False
    reason: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CostRecommendation(BaseModel):
    resource_id: str
    resource_name: str
    current_sku: str
    recommended_sku: str
    estimated_monthly_savings: float
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class IncidentDiagnosis(BaseModel):
    alert_id: str
    severity: str
    root_cause: str
    recommended_action: str
    risk_level: RiskLevel
    auto_remediate: bool = False
    runbook_id: str = ""


class DeploymentPlan(BaseModel):
    pipeline_id: str
    strategy: str
    target_environment: str
    changes_summary: str
    risk_level: RiskLevel
    rollback_plan: str


class CapacityForecast(BaseModel):
    resource_type: str
    current_utilization: float
    predicted_utilization: float
    forecast_window_hours: int
    scaling_recommendation: str
    confidence: float = Field(ge=0.0, le=1.0)
