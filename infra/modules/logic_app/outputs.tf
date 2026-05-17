output "id" {
  value = azurerm_logic_app_workflow.this.id
}

output "name" {
  value = azurerm_logic_app_workflow.this.name
}

output "access_endpoint" {
  value = azurerm_logic_app_workflow.this.access_endpoint
}

output "identity_principal_id" {
  value = azurerm_logic_app_workflow.this.identity[0].principal_id
}
