# Terraform Conventions

## Naming

All resources follow: `{abbreviation}-{project}-{environment}-{region_short}`

| Resource | Abbreviation | Example |
|----------|-------------|---------|
| Resource Group | rg | rg-agenticai-dev-eus2 |
| Key Vault | kv | kv-agenticai-dev-eus2 |
| Storage Account | st | stagenticaideveus2 |
| Log Analytics | log | log-agenticai-dev-eus2 |
| Function App | func | func-agenticai-finops-dev-eus2 |
| App Service Plan | asp | asp-agenticai-finops-dev-eus2 |
| Logic App | logic | logic-agenticai-approval-dev-eus2 |
| OpenAI Account | oai | oai-agenticai-dev-eus2 |
| Virtual Network | vnet | vnet-agenticai-dev-eus2 |

## Tagging

All resources MUST have:
- `project`: "agentic-ai-automation"
- `environment`: dev / staging / prod
- `managed_by`: "terraform"
- `phase`: "01-foundation" / "02-core-agents" / etc.

## Module Interface

Every module accepts:
- `project_name` (string)
- `environment` (string)
- `location` (string)
- `location_short` (string, default "eus2")
- `tags` (map(string))

Every module outputs at minimum:
- `id` (resource ID)
- `name` (resource name)

## State Management

- Backend: Azure Storage (created by `infra/scripts/init-backend.sh`)
- One state file per phase: `phase-01-foundation.tfstate`, etc.
- Cross-phase references via `terraform_remote_state` in `data.tf`

## Provider Versions

- Terraform >= 1.5.0
- azurerm ~> 3.100
- Pin versions in `providers.tf` of each phase

## Environment Files

- `environments/dev.tfvars` — development
- `environments/staging.tfvars` — staging
- `environments/prod.tfvars` — production

Pass via: `terraform plan -var-file=../../../environments/{env}.tfvars`
