output "resource_group_name" {
  value = module.resource_group.name
}

output "resource_group_id" {
  value = module.resource_group.id
}

output "log_analytics_workspace_id" {
  value = module.log_analytics.id
}

output "log_analytics_workspace_guid" {
  value = module.log_analytics.workspace_id
}

output "key_vault_id" {
  value = module.key_vault.id
}

output "key_vault_uri" {
  value = module.key_vault.vault_uri
}

output "storage_account_name" {
  value = module.storage_account.name
}

output "storage_account_id" {
  value = module.storage_account.id
}

output "openai_endpoint" {
  value = module.azure_openai.endpoint
}

output "openai_deployment_name" {
  value = module.azure_openai.deployment_name
}

output "openai_resource_id" {
  value = module.azure_openai.id
}
