resource "azurerm_sentinel_log_analytics_workspace_onboarding" "this" {
  workspace_id                 = var.log_analytics_workspace_id
  customer_managed_key_enabled = false
}

resource "azurerm_sentinel_data_connector_azure_active_directory" "aad" {
  name                       = "dc-aad-${var.environment}"
  log_analytics_workspace_id = azurerm_sentinel_log_analytics_workspace_onboarding.this.workspace_id
}

resource "azurerm_sentinel_data_connector_azure_security_center" "asc" {
  name                       = "dc-asc-${var.environment}"
  log_analytics_workspace_id = azurerm_sentinel_log_analytics_workspace_onboarding.this.workspace_id
  subscription_id            = var.subscription_id
}

resource "azurerm_sentinel_alert_rule_scheduled" "suspicious_agent_action" {
  name                       = "Suspicious Agent Action Detected"
  log_analytics_workspace_id = azurerm_sentinel_log_analytics_workspace_onboarding.this.workspace_id
  display_name               = "Suspicious Agent Action Detected"
  severity                   = "High"
  query                      = <<-KQL
    customEvents
    | where name == "agent_action"
    | where customDimensions.risk_level == "high"
    | where customDimensions.approval_status == "auto_approved"
    | project TimeGenerated, AgentName=customDimensions.agent_name, Action=customDimensions.action_type
  KQL
  query_frequency            = "PT5M"
  query_period               = "PT5M"
  trigger_operator           = "GreaterThan"
  trigger_threshold          = 0
  enabled                    = true
}
