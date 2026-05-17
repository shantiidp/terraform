locals {
  foundation = data.terraform_remote_state.foundation.outputs
  phase_tags = merge(var.tags, { phase = "03-expand-agents" })
}

module "security_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "security"
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
    "AGENT_NAME" = "security"
  }
}

module "deployment_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "deploy"
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
    "AGENT_NAME" = "deployment"
  }
}

module "capacity_function" {
  source = "../../modules/function_app"

  project_name               = var.project_name
  function_name              = "capacity"
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
    "AGENT_NAME" = "capacity_planner"
  }
}

module "sentinel" {
  source = "../../modules/sentinel"

  environment                = var.environment
  log_analytics_workspace_id = local.foundation.log_analytics_workspace_id
  subscription_id            = data.azurerm_client_config.current.subscription_id
}

module "rbac_agents" {
  source = "../../modules/rbac"

  role_assignments = {
    security_reader = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Security Reader"
      principal_id         = module.security_function.identity_principal_id
    }
    security_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.security_function.identity_principal_id
    }
    deploy_contributor = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Contributor"
      principal_id         = module.deployment_function.identity_principal_id
    }
    deploy_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.deployment_function.identity_principal_id
    }
    capacity_reader = {
      scope                = local.foundation.resource_group_id
      role_definition_name = "Reader"
      principal_id         = module.capacity_function.identity_principal_id
    }
    capacity_kv = {
      scope                = local.foundation.key_vault_id
      role_definition_name = "Key Vault Secrets User"
      principal_id         = module.capacity_function.identity_principal_id
    }
  }
}
