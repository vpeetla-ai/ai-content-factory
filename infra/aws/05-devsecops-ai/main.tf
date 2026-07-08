terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "environment" { default = "demo" }

provider "aws" { region = var.aws_region }

resource "aws_dynamodb_table" "security_posture" {
  name         = "devsecops-posture-${var.environment}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "repo"
  range_key    = "scanned_at"

  attribute {
    name = "repo"
    type = "S"
  }
  attribute {
    name = "scanned_at"
    type = "S"
  }
}

output "posture_table" {
  value = aws_dynamodb_table.security_posture.name
}
