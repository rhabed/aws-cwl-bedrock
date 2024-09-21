variable "region" {
  description = "The Region that we will be building the module in"
  type        = string
  default     = "ap-southeast-2"
}

variable "hash_key" {
  description = "Default Hash Key"
  type        = string
  default = "log_group_arn"
}

variable "attribute_name" {
  description = "Default Attribute Name"
  type        = string
  default = "log_group_arn"  
}

variable "policy_json" {
  description = "IAM Policy"
  type = string
  default = ""
}

variable cache_name {
    description = "Dynamodb ARN"
    type = string
    default = ""
}