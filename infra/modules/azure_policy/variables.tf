variable "subscription_id" {
  type = string
}

variable "policy_definitions" {
  type = map(object({
    mode         = string
    display_name = string
    description  = string
    policy_rule  = string
    parameters   = optional(string)
  }))
  default = {}
}

variable "policy_assignments" {
  type = map(object({
    policy_definition_key = string
    display_name          = string
    description           = optional(string, "")
    parameters            = optional(string)
  }))
  default = {}
}

variable "builtin_policy_assignments" {
  type = map(object({
    policy_definition_id = string
    display_name         = string
    parameters           = optional(string)
  }))
  default = {}
}
