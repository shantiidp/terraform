# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CI/CD Layer                              │
│              GitHub Actions (OIDC -> Azure)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────────────────────────────┐  │
│  │  Governance   │    │          Agent Layer                  │  │
│  │              │    │                                        │  │
│  │ Azure Policy │    │  ┌─────────┐ ┌──────────┐ ┌────────┐ │  │
│  │ RBAC / MI    │◄───│  │ FinOps  │ │ Incident │ │ IaC    │ │  │
│  │ Logic Apps   │    │  │ Agent   │ │ Responder│ │ Gen    │ │  │
│  │ Audit Trail  │    │  └────┬────┘ └────┬─────┘ └───┬────┘ │  │
│  │              │    │       │            │           │       │  │
│  │              │    │  ┌────┴────┐ ┌────┴─────┐ ┌───┴────┐ │  │
│  │              │◄───│  │Security │ │ Deploy   │ │Capacity│ │  │
│  │              │    │  │ Agent   │ │ Agent    │ │Planner │ │  │
│  └──────┬───────┘    │  └─────────┘ └──────────┘ └────────┘ │  │
│         │            │                                        │  │
│         │            │  ┌────────────────────────────────────┐│  │
│         │            │  │    Semantic Kernel + Plugins       ││  │
│         │            │  │  (cost_query, monitor, terraform)  ││  │
│         │            │  └────────────────────────────────────┘│  │
│         │            └──────────────────────┬─────────────────┘  │
│         │                                   │                    │
├─────────┼───────────────────────────────────┼────────────────────┤
│         │           Azure Platform          │                    │
│  ┌──────▼───────┐  ┌──────────┐  ┌─────────▼─────────┐         │
│  │ Azure Policy │  │Key Vault │  │  Azure OpenAI     │         │
│  │ Defender     │  │Secrets   │  │  GPT-4o           │         │
│  └──────────────┘  └──────────┘  └───────────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────┐  ┌───────────────────┐         │
│  │Log Analytics │  │ Sentinel │  │ Azure Functions   │         │
│  │+ Monitor     │  │ SIEM     │  │ (Python 3.11)     │         │
│  └──────┬───────┘  └──────────┘  └───────────────────┘         │
│         │                                                       │
├─────────┼───────────────────────────────────────────────────────┤
│         │           Analytics Layer                              │
│  ┌──────▼───────┐  ┌──────────┐  ┌───────────────────┐         │
│  │ KQL Queries  │  │Workbooks │  │ Power BI / Fabric │         │
│  └──────────────┘  └──────────┘  └───────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **Trigger**: Azure Monitor alert, timer, or HTTP request triggers an Azure Function
2. **Agent Init**: Function creates Semantic Kernel with Azure OpenAI and plugins
3. **Data Gathering**: Agent uses plugins to query Azure APIs (Cost Management, Monitor, ARM)
4. **LLM Reasoning**: Agent sends gathered data + prompt to GPT-4o for analysis
5. **Governance Gate**: Before any action, agent passes through GovernanceGate
   - Low risk: auto-approved, logged
   - Medium/High risk: routed to Logic App for human approval
6. **Execution**: On approval, agent executes the action via Azure SDK
7. **Audit**: Every step logged to Log Analytics with correlation ID
8. **Analytics**: KQL queries, Workbooks, and Power BI surface insights

## State Management

- **Terraform state**: Azure Storage backend, separate state file per phase
- **Cross-phase references**: `terraform_remote_state` data sources
- **Agent state**: Stateless (Azure Functions), all persistence via Log Analytics
- **Secrets**: Azure Key Vault with managed identity access
