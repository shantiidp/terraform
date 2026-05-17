locals {
  foundation = data.terraform_remote_state.foundation.outputs
  phase_tags = merge(var.tags, { phase = "04-production" })
}

module "networking" {
  source = "../../modules/networking"

  project_name               = var.project_name
  environment                = var.environment
  location                   = var.location
  location_short             = var.location_short
  resource_group_name        = local.foundation.resource_group_name
  address_space              = var.vnet_address_space
  enable_private_endpoints   = var.enable_private_endpoints
  openai_resource_id         = local.foundation.openai_resource_id
  tags                       = local.phase_tags
}
