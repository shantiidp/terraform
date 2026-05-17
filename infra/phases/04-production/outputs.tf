output "vnet_id" {
  value = module.networking.vnet_id
}

output "function_subnet_id" {
  value = module.networking.function_subnet_id
}

output "private_endpoint_subnet_id" {
  value = module.networking.private_endpoint_subnet_id
}
