# Governance Model

## Principles

1. **Governance-first**: All guardrails deployed before any agent
2. **Least privilege**: Agents get minimum required permissions
3. **Full audit trail**: Every action logged with correlation ID
4. **Human-in-the-loop**: Destructive actions require human approval
5. **Progressive trust**: Agents earn autonomous mode through proven track record

## Layers

### Azure Policy
- **Allowed regions**: Restrict deployments to approved Azure regions
- **Required tags**: All resources must have `project`, `environment`, `managed_by`
- **Allowed SKUs**: Limit VM sizes to approved list
- **Deny public IP**: Block public IP creation on production resources
- **Agent audit**: Resources modified by agents must have audit trail tag

### RBAC
- System-assigned managed identities for all agents
- Custom roles with minimal permissions per agent
- No delete permissions on resource groups or subscriptions
- See `governance/rbac/role_matrix.md` for full mapping

### Approval Workflows (Logic Apps)
- **High-risk approval**: Email-based approval for destructive actions
- **Cost threshold approval**: Auto-approve below threshold, human approval above
- Configurable approver lists and timeout periods

### Audit Logging
- All agent actions emit structured events to Log Analytics
- Every event includes: `agent_name`, `action_type`, `risk_level`, `correlation_id`, `timestamp`
- Sentinel monitors for anomalous agent behavior
- KQL queries in `analytics/kql_queries/` for standard reporting

## Trust Escalation (Phase 4)

After 6 months of operational data, low-risk actions with consistent success can graduate to auto-execute mode. Criteria:
- Agent success rate > 99% for the action type
- Zero rejected approvals in the last 30 days
- Action type classified as LOW risk
- Confidence score from the LLM > 0.9
