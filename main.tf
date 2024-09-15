module "cwl_dynamodb_cache" {
  source = "./modules/dynamodb"
  name = "Dynamodb_CWL"
  hash_key = var.hash_key
  attribute_name = var.attribute_name
}

module "bedrock_lambda_function" {
    source = "./modules/lambda"
    name = "Bedrock_Lambda"
    source_path = "./src/lambda_bedrock"
    region = var.region
    policy_json = data.aws_iam_policy_document.lambda_policy.json
}   
