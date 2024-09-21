data "aws_caller_identity" "current" {}

locals {
    account_id = data.aws_caller_identity.current.account_id
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    effect = "Allow"
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
    effect = "Allow"
    actions = [
        "bedrock:InvokeAgent",
        "bedrock:GetModel",
        "bedrock:CreateEvaluationJob"
    ]
    resources = ["arn:aws:bedrock:${var.region}:${local.account_id}:foundation-model/*"]
  }

  statement {
    effect = "Allow"
    actions = [
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "logs:*"
    ]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "bedrock:InvokeModel"   
    ]
    resources = ["arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"]
  }
}