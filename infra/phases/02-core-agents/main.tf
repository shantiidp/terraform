locals {
  foundation = data.terraform_remote_state.foundation.outputs
  phase_tags = merge(var.tags, { phase = "02-core-agents" })
}

module "finops_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "finops"
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  sku_name                   = var.function_app_sku
  storage_account_name       = local.foundation.storage_account_name
  storage_account_access_key = data.azurerm_storage_account.functions.primary_access_key
  openai_endpoint            = local.foundation.openai_endpoint
  openai_deployment_name     = local.foundation.openai_deployment_name
  key_vault_uri              = local.foundation.key_vault_uri
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_guid
  log_analytics_resource_id  = local.foundation.log_analytics_workspace_id
  tags                       = local.phase_tags

  extra_app_settings = {
    "AGENT_NAME" = "finops"
  }
}

module "incident_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "incident"
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  sku_name                   = var.function_app_sku
  storage_account_name       = local.foundation.storage_account_name
  storage_account_access_key = data.azurerm_storage_account.functions.primary_access_key
  openai_endpoint            = local.foundation.openai_endpoint
  openai_deployment_name     = local.foundation.openai_deployment_name
  key_vault_uri              = local.foundation.key_vault_uri
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_guid
  log_analytics_resource_id  = local.foundation.log_analytics_workspace_id
  tags                       = local.phase_tags

  extra_app_settings = {
    "AGENT_NAME" = "incident_responder"
  }
}

module "iac_generator_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "iacgen"
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  sku_name                   = var.function_app_sku
  storage_account_name       = local.foundation.storage_account_name
  storage_account_access_key = data.azurerm_storage_account.functions.primary_access_key
  openai_endpoint            = local.foundation.openai_endpoint
  openai_deployment_name     = local.foundation.openai_deployment_name
  key_vault_uri              = local.foundation.key_vault_uri
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_guid
  log_analytics_resource_id  = local.foundation.log_analytics_workspace_id
  tags                       = local.phase_tags

  extra_app_settings = {
    "AGENT_NAME" = "iac_generator"
  }
}

module "approval_workflow" {
  source = "../../modules/logic_app"

  project_name               = var.project_name
  workflow_name              = "approval"
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_id
  tags                       = local.phase_tags
}

module "azure_monitor" {
  source = "../../modules/azure_monitor"

  project_name               = var.project_name
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_id
  tags                       = local.phase_tags

  webhook_receivers = [
    {
      name = "incident-agent"
      uri  = "https://${module.incident_function.default_hostname}/api/incident"
    }
  ]
}

module "rbac_agents" {
  source = "../../modules/rbac"

  role_assignments = {
    finops_reader = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Reader"
      principal_id         = module.finops_function.identity_principal_id
    }
    finops_cost = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Cost Management Reader"
      principal_id         = module.finops_function.identity_principal_id
    }
    incident_reader = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Reader"
      principal_id         = module.incident_function.identity_principal_id
    }
    incident_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.incident_function.identity_principal_id
    }
    finops_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.finops_function.identity_principal_id
    }
    iacgen_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.iac_generator_function.identity_principal_id
    }
  }
}
