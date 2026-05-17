data "azurerm_client_config" "current" {}

locals {
  phase_tags = merge(var.tags, { phase = "01-foundation" })
}

module "resource_group" {
  source = "../../modules/resource_group"

  project_name   = var.project_name
  environment    = var.environment
  location       = var.location
  location_short = var.location_short
  tags           = local.phase_tags
}

module "log_analytics" {
  source = "../../modules/log_analytics"

  project_name        = var.project_name
  environment         = var.environment
  location            = var.location
  location_short      = var.location_short
  resource_group_name = module.resource_group.name
  retention_in_days   = var.log_analytics_retention_days
  tags                = local.phase_tags
}

module "key_vault" {
  source = "../../modules/key_vault"

  project_name               = var.project_name
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = module.resource_group.name
  log_analytics_workspace_id = module.log_analytics.id
  tags                       = local.phase_tags
}

module "storage_account" {
  source = "../../modules/storage_account"

  project_name               = var.project_name
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = module.resource_group.name
  log_analytics_workspace_id = module.log_analytics.id
  tags                       = local.phase_tags
}

module "azure_openai" {
  source = "../../modules/azure_openai"

  project_name               = var.project_name
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = module.resource_group.name
  sku_name                   = var.openai_sku
  model_name                 = var.openai_model_name
  model_version              = var.openai_model_version
  log_analytics_workspace_id = module.log_analytics.id
  tags                       = local.phase_tags
}

module "azure_policy" {
  source = "../../modules/azure_policy"

  subscription_id = data.azurerm_client_config.current.subscription_id

  policy_definitions = {
    allowed_regions = {
      mode         = "Indexed"
      display_name = "Restrict resource locations"
      description  = "Restricts Azure resources to approved regions"
      policy_rule  = file("${path.module}/../../../governance/policies/allowed_regions.json")
    }
    required_tags = {
      mode         = "Indexed"
      display_name = "Require mandatory tags"
      description  = "Enforces mandatory tags on all resources"
      policy_rule  = file("${path.module}/../../../governance/policies/required_tags.json")
    }
  }

  policy_assignments = {
    enforce_regions = {
      policy_definition_key = "allowed_regions"
      display_name          = "Enforce allowed regions"
    }
    enforce_tags = {
      policy_definition_key = "required_tags"
      display_name          = "Enforce required tags"
    }
  }
}

module "rbac" {
  source = "../../modules/rbac"

  custom_role_definitions = {
    agent_reader = {
      name        = "AgenticAI Agent Reader"
      description = "Read-only access for AI agents to query resources and metrics"
      actions = [
        "Microsoft.Resources/subscriptions/resourceGroups/read",
        "Microsoft.Resources/subscriptions/resources/read",
        "Microsoft.Insights/metrics/read",
        "Microsoft.Insights/logs/read",
        "Microsoft.CostManagement/query/action",
        "Microsoft.OperationalInsights/workspaces/query/read",
      ]
    }
    agent_operator = {
      name        = "AgenticAI Agent Operator"
      description = "Limited write access for AI agents to perform approved remediation"
      actions = [
        "Microsoft.Compute/virtualMachines/read",
        "Microsoft.Compute/virtualMachines/restart/action",
        "Microsoft.Compute/virtualMachines/deallocate/action",
        "Microsoft.Web/sites/restart/action",
        "Microsoft.Resources/tags/write",
      ]
      not_actions = [
        "Microsoft.Compute/virtualMachines/delete",
        "Microsoft.Resources/subscriptions/resourceGroups/delete",
      ]
    }
  }
}
