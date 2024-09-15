data "aws_caller_identity" "current" {}

locals {
    account_id = data.aws_caller_identity.current.account_id
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    actions = [
        "dynamodb:CreateTable",
        "dynamodb:DeleteTable",
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
    ]
    resources = ["arn:aws:dynamodb:${var.region}:${local.account_id}:table/*"]
  }

  statement {
    actions = [
        "bedrock:InvokeAgent",
        "bedrock:GetModel",
        "bedrock:CreateEvaluationJob"
    ]
    resources = ["arn:aws:bedrock:${var.region}:${local.account_id}:foundation-model/*"]
  }

  statement {
    actions = [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics"
    ]
    resources = ["*"]
  }
}