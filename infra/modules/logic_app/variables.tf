variable "project_name" {
  type = string
}

variable "workflow_name" {
  type        = string
  description = "Name of the Logic App workflow (e.g., high-risk-approval)"
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

variable "log_analytics_workspace_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
