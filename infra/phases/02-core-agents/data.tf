data "terraform_remote_state" "foundation" {
  backend = "azurerm"

  config = {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stagenticaiterraform"
    container_name       = "tfstate"
    key                  = "phase-01-foundation.tfstate"
  }
}

data "azurerm_storage_account" "functions" {
  name                = data.terraform_remote_state.foundation.outputs.storage_account_name
  resource_group_name = data.terraform_remote_state.foundation.outputs.resource_group_name
}
