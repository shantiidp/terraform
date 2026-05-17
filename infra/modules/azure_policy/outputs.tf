output "policy_definition_ids" {
  value = { for k, v in azurerm_policy_definition.custom : k => v.id }
}

output "policy_assignment_ids" {
  value = { for k, v in azurerm_subscription_policy_assignment.custom : k => v.id }
}
