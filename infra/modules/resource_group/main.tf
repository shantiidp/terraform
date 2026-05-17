resource "azurerm_resource_group" "this" {
  name     = "rg-${var.project_name}-${var.environment}-${var.location_short}"
  location = var.location
  tags     = var.tags
}
