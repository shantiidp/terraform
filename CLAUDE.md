# CLAUDE.md

## Project Overview
Azure Agentic AI Automation — 6 AI agents for Azure infrastructure automation, deployed in 4 phases over 12 months.

## Tech Stack
- **IaC**: Terraform (modules in `infra/modules/`, compositions in `infra/phases/`)
- **Agent Logic**: Python 3.11+ with Semantic Kernel
- **Hosting**: Azure Functions (Linux, Python runtime)
- **LLM**: Azure OpenAI GPT-4o
- **Governance**: Azure Policy, RBAC, Logic Apps approval gates

## Key Conventions
- Terraform modules follow standard interface: `project_name`, `environment`, `location`, `tags` inputs
- All Terraform resources named: `{abbreviation}-{project}-{environment}-{region_short}`
- Python package: `agentic_ai` (installed from `agents/src/`)
- Every agent action goes through `GovernanceGate` before execution
- Zero secrets in code — all via Key Vault references
- Tests in `agents/tests/`, run with `pytest`
- Lint with `ruff check agents/`

## Commands
- `terraform validate` — validate Terraform in any phase directory
- `cd agents && pip install -e ".[dev]" && pytest` — run Python tests
- `ruff check agents/` — lint Python code
