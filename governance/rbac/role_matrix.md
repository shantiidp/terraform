# Agent RBAC Role Matrix

| Agent | Custom Role | Built-in Roles | Scope |
|-------|-------------|----------------|-------|
| FinOps | Agent Reader | Cost Management Reader | Subscription |
| Incident Responder | Agent Reader, Agent Operator | - | Resource Group |
| IaC Generator | Agent Reader | - | Resource Group |
| Security | Agent Security Reader | Security Reader | Subscription |
| Deployment | Agent Operator | Contributor (scoped) | Resource Group |
| Capacity Planner | Agent Reader | Reader | Resource Group |

## Principles

- **Least privilege**: Each agent gets only the permissions it needs
- **No delete**: No agent has delete permissions on resource groups or subscriptions
- **Scoped access**: Prefer resource group scope over subscription scope
- **Managed identity**: All agents authenticate via system-assigned managed identity
- **Key Vault**: All agents get Key Vault Secrets User for secret retrieval
