data "terraform_remote_state" "foundation" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stagenticaiterraform"
    container_name       = "tfstate"
    key                  = "phase-01-foundation.tfstate"
  }
}

data "terraform_remote_state" "core_agents" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stagenticaiterraform"
    container_name       = "tfstate"
    key                  = "phase-02-core-agents.tfstate"
  }
}

data "terraform_remote_state" "expand_agents" {
  backend = "azurerm"
  config = {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stagenticaiterraform"
    container_name       = "tfstate"
    key                  = "phase-03-expand-agents.tfstate"
  }
}
