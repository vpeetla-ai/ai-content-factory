# Governed Multi-Agent API — Terraform skeleton
# Usage: terraform init && terraform plan (requires AWS credentials)

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "environment" {
  type    = string
  default = "demo"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  tags       = { Name = "vap-aegis-${var.environment}" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, 1)
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"
}

resource "aws_lb" "api" {
  name               = "governed-agents-${var.environment}"
  load_balancer_type = "application"
  subnets            = [aws_subnet.public.id]
}

resource "aws_db_instance" "postgres" {
  identifier     = "governed-agents-${var.environment}"
  engine         = "postgres"
  instance_class = "db.t4g.micro"
  allocated_storage = 20
  username       = "vapadmin"
  password       = "CHANGE_ME"
  skip_final_snapshot = true
}

output "alb_dns" {
  value = aws_lb.api.dns_name
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}
