output "dynamo_db_arn" {
    description = "dynamodb_table_arn"
    value = module.dynamodb_table.dynamodb_table_arn
}