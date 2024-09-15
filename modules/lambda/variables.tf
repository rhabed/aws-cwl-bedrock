variable "name" {
  description = "Lambda function name"
  type        = string
}

variable "description" {
  description = "The Lambda Function description"
  type        = string
  default = "Lambda Function"
}

variable "python_runtime" {
  description = "Pyhton runtime"
  type        = string
  default = "python3.12"
}

variable "source_path" {
    description = "Source Code of Lambda Function"
    type = string
}

variable "region" {
    description = "AWS Region"
    type = string
}

variable policy_json {
    description = "IAM Policy"
    type = string
}