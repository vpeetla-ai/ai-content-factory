terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "environment" { default = "demo" }

provider "aws" { region = var.aws_region }

resource "aws_db_instance" "finops" {
  identifier        = "agent-finops-${var.environment}"
  engine            = "postgres"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  username          = "finops"
  password          = "CHANGE_ME"
  skip_final_snapshot = true
}

resource "aws_sns_topic" "budget_alerts" {
  name = "agent-finops-budget-${var.environment}"
}

output "finops_db_endpoint" { value = aws_db_instance.finops.endpoint }
output "budget_alert_topic" { value = aws_sns_topic.budget_alerts.arn }
