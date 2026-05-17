data "azurerm_subscription" "current" {}

resource "azurerm_role_definition" "custom" {
  for_each = var.custom_role_definitions

  name        = each.value.name
  scope       = data.azurerm_subscription.current.id
  description = each.value.description

  permissions {
    actions     = each.value.actions
    not_actions = each.value.not_actions
  }

  assignable_scopes = [data.azurerm_subscription.current.id]
}

resource "azurerm_role_assignment" "assignments" {
  for_each = var.role_assignments

  scope                = each.value.scope
  role_definition_name = each.value.role_definition_name
  principal_id         = each.value.principal_id
}
