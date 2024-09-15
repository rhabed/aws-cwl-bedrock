terraform {
  required_version = "~> 1.9.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.67.0"
    }
  }
  backend "s3" {
    bucket = "mypulpfiction"
    key    = "pumpkin"
    region = "ap-southeast-2"
  }
}

provider "aws" {
  region = var.region
}