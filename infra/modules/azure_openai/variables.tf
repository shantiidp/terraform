variable "project_name" {
  type = string
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
  default = "S0"
}

variable "model_name" {
  type    = string
  default = "gpt-4o"
}

variable "model_version" {
  type    = string
  default = "2024-08-06"
}

variable "model_capacity" {
  type    = number
  default = 10
}

variable "log_analytics_workspace_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
