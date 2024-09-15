variable "name" {
  description = "Dynamodb Name"
  type        = string
}

variable "hash_key" {
  description = "Default Hash Key"
  type        = string
}

variable "attribute_name" {
  description = "Default Attribute Name"
  type        = string
}

variable "billing_mode" {
    description = "Billing mode"
    type = string
    default = "PAY_PER_REQUEST"
}

variable "sse_specification" {
    description = "SSE"
    type = bool
    default = true
}