terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stagenticaiterraform"
    container_name       = "tfstate"
    key                  = "phase-01-foundation.tfstate"
  }
}
