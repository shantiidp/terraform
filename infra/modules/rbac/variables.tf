variable "custom_role_definitions" {
  type = map(object({
    name        = string
    description = string
    actions     = list(string)
    not_actions = optional(list(string), [])
  }))
  default = {}
}

variable "role_assignments" {
  type = map(object({
    scope                = string
    role_definition_name = string
    principal_id         = string
  }))
  default = {}
}
