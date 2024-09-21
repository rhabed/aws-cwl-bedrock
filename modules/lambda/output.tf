output "lambda_function_arn" {
    description = "Lambda Function ARN"
    value = module.lambda_function.lambda_function_arn
}

output "lambda_function_name" {
    description = "Lambda Function Name"
    value = module.lambda_function.lambda_function_name
}