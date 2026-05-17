resource "azurerm_service_plan" "this" {
  name                = "asp-${var.project_name}-${var.function_name}-${var.environment}-${var.location_short}"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Linux"
  sku_name            = var.sku_name
  tags                = var.tags
}

resource "azurerm_linux_function_app" "this" {
  name                       = "func-${var.project_name}-${var.function_name}-${var.environment}-${var.location_short}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  service_plan_id            = azurerm_service_plan.this.id
  storage_account_name       = var.storage_account_name
  storage_account_access_key = var.storage_account_access_key
  tags                       = var.tags

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_stack {
      python_version = "3.11"
    }

    application_insights_connection_string = var.app_insights_connection_string
  }

  app_settings = merge(
    {
      "AZURE_OPENAI_ENDPOINT"       = var.openai_endpoint
      "AZURE_OPENAI_DEPLOYMENT"     = var.openai_deployment_name
      "KEY_VAULT_URI"               = var.key_vault_uri
      "LOG_ANALYTICS_WORKSPACE_ID"  = var.log_analytics_workspace_id
      "FUNCTIONS_WORKER_RUNTIME"    = "python"
      "AzureWebJobsFeatureFlags"    = "EnableWorkerIndexing"
    },
    var.extra_app_settings
  )
}

resource "azurerm_monitor_diagnostic_setting" "this" {
  count                      = var.log_analytics_workspace_id != null ? 1 : 0
  name                       = "diag-${azurerm_linux_function_app.this.name}"
  target_resource_id         = azurerm_linux_function_app.this.id
  log_analytics_workspace_id = var.log_analytics_resource_id

  enabled_log {
    category = "FunctionAppLogs"
  }

  metric {
    category = "AllMetrics"
  }
}
