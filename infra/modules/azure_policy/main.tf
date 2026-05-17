resource "azurerm_policy_definition" "custom" {
  for_each = var.policy_definitions

  name         = each.key
  policy_type  = "Custom"
  mode         = each.value.mode
  display_name = each.value.display_name
  description  = each.value.description

  policy_rule = each.value.policy_rule
  parameters  = each.value.parameters
}

resource "azurerm_subscription_policy_assignment" "custom" {
  for_each = var.policy_assignments

  name                 = each.key
  policy_definition_id = azurerm_policy_definition.custom[each.value.policy_definition_key].id
  subscription_id      = "/subscriptions/${var.subscription_id}"
  display_name         = each.value.display_name
  description          = each.value.description
  parameters           = each.value.parameters
}

resource "azurerm_subscription_policy_assignment" "builtin" {
  for_each = var.builtin_policy_assignments

  name                 = each.key
  policy_definition_id = each.value.policy_definition_id
  subscription_id      = "/subscriptions/${var.subscription_id}"
  display_name         = each.value.display_name
  parameters           = each.value.parameters
}
