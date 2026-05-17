output "custom_role_ids" {
  value = { for k, v in azurerm_role_definition.custom : k => v.role_definition_resource_id }
}

output "assignment_ids" {
  value = { for k, v in azurerm_role_assignment.assignments : k => v.id }
}
