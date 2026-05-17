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

variable "address_space" {
  type    = list(string)
  default = ["10.0.0.0/16"]
}

variable "function_subnet_prefix" {
  type    = string
  default = "10.0.1.0/24"
}

variable "private_endpoint_subnet_prefix" {
  type    = string
  default = "10.0.2.0/24"
}

variable "enable_private_endpoints" {
  type    = bool
  default = false
}

variable "openai_resource_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}
