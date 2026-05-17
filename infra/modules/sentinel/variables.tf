variable "environment" {
  type = string
}

variable "log_analytics_workspace_id" {
  type        = string
  description = "Azure resource ID of the Log Analytics workspace"
}

variable "subscription_id" {
  type = string
}
