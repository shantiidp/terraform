output "id" {
  value = azurerm_cognitive_account.this.id
}

output "name" {
  value = azurerm_cognitive_account.this.name
}

output "endpoint" {
  value = azurerm_cognitive_account.this.endpoint
}

output "primary_access_key" {
  value     = azurerm_cognitive_account.this.primary_access_key
  sensitive = true
}

output "identity_principal_id" {
  value = azurerm_cognitive_account.this.identity[0].principal_id
}

output "deployment_name" {
  value = azurerm_cognitive_deployment.gpt4o.name
}
