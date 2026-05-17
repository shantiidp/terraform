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

variable "tags" {
  type    = map(string)
  default = {}
}

variable "openai_sku" {
  type    = string
  default = "S0"
}

variable "openai_model_name" {
  type    = string
  default = "gpt-4o"
}

variable "openai_model_version" {
  type    = string
  default = "2024-08-06"
}

variable "log_analytics_retention_days" {
  type    = number
  default = 30
}

variable "function_app_sku" {
  type    = string
  default = "Y1"
}
