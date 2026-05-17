variable "project_name" {
  type = string
}

variable "function_name" {
  type        = string
  description = "Unique name for this function app (e.g., finops, incident)"
}

variable "environment" {
  type = string
}

variable "location" {
  type = string
}

variable "location_short" {
  type    = string
  default = "eus2"
}

variable "resource_group_name" {
  type = string
}

variable "sku_name" {
  type    = string
  default = "Y1"
}

variable "storage_account_name" {
  type = string
}

variable "storage_account_access_key" {
  type      = string
  sensitive = true
}

variable "openai_endpoint" {
  type = string
}

variable "openai_deployment_name" {
  type = string
}

variable "key_vault_uri" {
  type = string
}

variable "log_analytics_workspace_id" {
  type        = string
  description = "Log Analytics workspace ID (GUID) for app settings"
  default     = ""
}

variable "log_analytics_resource_id" {
  type        = string
  description = "Log Analytics workspace Azure resource ID for diagnostic settings"
  default     = null
}

variable "app_insights_connection_string" {
  type    = string
  default = ""
}

variable "extra_app_settings" {
  type    = map(string)
  default = {}
}

variable "tags" {
  type    = map(string)
  default = {}
}
