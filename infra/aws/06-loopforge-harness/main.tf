terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "environment" { default = "demo" }

provider "aws" { region = var.aws_region }

resource "aws_ecs_cluster" "loopforge" {
  name = "loopforge-${var.environment}"
}

resource "aws_s3_bucket" "eval_artifacts" {
  bucket = "loopforge-evals-${var.environment}"
}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
}

output "ecs_cluster" { value = aws_ecs_cluster.loopforge.name }
output "eval_bucket" { value = aws_s3_bucket.eval_artifacts.bucket }
