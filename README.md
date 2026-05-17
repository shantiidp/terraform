# Azure Agentic AI Automation

A phased platform for deploying AI-powered infrastructure automation on Microsoft Azure. Six specialized agents handle FinOps, IaC generation, incident response, deployments, capacity planning, and security — all governed by Azure Policy, RBAC, and human-in-the-loop approval gates.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Governance Layer                    │
│  Azure Policy │ RBAC │ Audit Logging │ Approval Gates│
├─────────────────────────────────────────────────────┤
│                   Agent Layer                        │
│  FinOps │ IaC Gen │ Incident │ Deploy │ Cap │ Sec   │
│         (Azure Functions + Semantic Kernel)           │
├─────────────────────────────────────────────────────┤
│                  Analytics Layer                      │
│  Log Analytics │ Azure Monitor │ Power BI / Fabric   │
├─────────────────────────────────────────────────────┤
│                 Azure Infrastructure                  │
│  OpenAI │ Key Vault │ Storage │ Networking │ Sentinel│
└─────────────────────────────────────────────────────┘
```

## Project Structure

| Directory | Purpose |
|-----------|---------|
| `infra/` | Terraform modules and phase-based deployments |
| `agents/` | Python agent code, Semantic Kernel plugins, Azure Functions |
| `governance/` | Azure Policy definitions, RBAC roles, approval workflows |
| `analytics/` | KQL queries, Monitor Workbooks, Power BI templates |
| `.github/` | CI/CD workflows |
| `docs/` | Architecture and design documentation |

## Phased Deployment

| Phase | Months | Focus |
|-------|--------|-------|
| 1 - Foundation | 1-3 | Governance, Key Vault, Log Analytics, Azure OpenAI |
| 2 - Core Agents | 4-6 | Incident Responder, FinOps, IaC Generator |
| 3 - Expand | 7-9 | Security, Deployment, Capacity Planner |
| 4 - Production | 10-12 | Networking hardening, autonomous mode, Fabric |

## Quick Start

### Prerequisites

- Terraform >= 1.5
- Python >= 3.11
- Azure CLI (`az login`)
- Azure Functions Core Tools

### Deploy Phase 1

```bash
# Initialize Terraform backend
cd infra/scripts && bash init-backend.sh

# Deploy foundation
cd ../phases/01-foundation
terraform init
terraform plan -var-file=../../../environments/dev.tfvars
terraform apply -var-file=../../../environments/dev.tfvars
```

### Run Agents Locally

```bash
cd agents
pip install -e ".[dev]"
pytest

cd function_apps/finops_func
func start
```

## Contributing

See [docs/runbook-onboarding.md](docs/runbook-onboarding.md) for adding new agents.
