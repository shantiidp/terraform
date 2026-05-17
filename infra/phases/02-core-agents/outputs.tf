output "finops_function_name" {
  value = module.finops_function.name
}

output "finops_function_hostname" {
  value = module.finops_function.default_hostname
}

output "incident_function_name" {
  value = module.incident_function.name
}

output "incident_function_hostname" {
  value = module.incident_function.default_hostname
}

output "iac_generator_function_name" {
  value = module.iac_generator_function.name
}

output "approval_workflow_endpoint" {
  value = module.approval_workflow.access_endpoint
}

output "action_group_id" {
  value = module.azure_monitor.action_group_id
}
