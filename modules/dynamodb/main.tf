terraform {
  required_version = "~> 1.9.0"
}

module "dynamodb_table" {
  source   = "terraform-aws-modules/dynamodb-table/aws"
  version = "4.1.0"

  name     = var.name
  hash_key = var.hash_key
  billing_mode = var.billing_mode
  server_side_encryption_enabled = var.sse_specification

  attributes = [
    {
      name = var.attribute_name
      type = "S"
    }
  ]
}