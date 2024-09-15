variable "region" {
  description = "The Region that we will be building the module in"
  type        = string
  default     = "ap-southeast-2"
}

variable "hash_key" {
  description = "Default Hash Key"
  type        = string
}

variable "attribute_name" {
  description = "Default Attribute Name"
  type        = string
}

variable "policy_json" {
  description = "IAM Policy"
  type = string
  default = ""
}
