project_name = "agenticai"
environment  = "prod"
location     = "eastus2"

tags = {
  project     = "agentic-ai-automation"
  environment = "prod"
  managed_by  = "terraform"
}

openai_sku           = "S0"
openai_model_name    = "gpt-4o"
openai_model_version = "2024-08-06"

log_analytics_retention_days = 365

function_app_sku = "EP2"
