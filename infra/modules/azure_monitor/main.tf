resource "azurerm_monitor_action_group" "this" {
  name                = "ag-${var.project_name}-${var.environment}-${var.location_short}"
  resource_group_name = var.resource_group_name
  short_name          = substr(var.project_name, 0, 12)
  tags                = var.tags

  dynamic "webhook_receiver" {
    for_each = var.webhook_receivers
    content {
      name                    = webhook_receiver.value.name
      service_uri             = webhook_receiver.value.uri
      use_common_alert_schema = true
    }
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert_v2" "agent_failures" {
  count               = var.log_analytics_workspace_id != null ? 1 : 0
  name                = "alert-agent-failures-${var.environment}"
  resource_group_name = var.resource_group_name
  location            = var.location
  description         = "Fires when any agent reports a failure"
  severity            = 1
  enabled             = true
  tags                = var.tags

  scopes                = [var.log_analytics_workspace_id]
  evaluation_frequency  = "PT5M"
  window_duration       = "PT5M"

  criteria {
    query = <<-KQL
      customEvents
      | where name startswith "agent_action"
      | where customDimensions.status == "failed"
      | summarize FailureCount = count() by AgentName = tostring(customDimensions.agent_name)
    KQL

    time_aggregation_method = "Count"
    threshold               = 1
    operator                = "GreaterThanOrEqual"
  }

  action {
    action_groups = [azurerm_monitor_action_group.this.id]
  }
}
