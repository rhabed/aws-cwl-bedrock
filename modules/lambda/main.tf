terraform {
  required_version = "~> 1.9.0"
}


module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"
  version = "7.9.0"

  function_name = var.name
  description   = var.description
  handler       = "function.lambda_handler"
  runtime       = var.python_runtime
  source_path = var.source_path
  attach_policy_json = true
  policy_json = var.policy_json
  environment_variables = {
    cache_name = var.cache_name
    model = var.model
  }
  timeout = 180
}

