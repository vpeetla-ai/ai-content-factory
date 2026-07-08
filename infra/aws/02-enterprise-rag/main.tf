terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "environment" { default = "demo" }

provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "documents" {
  bucket = "enterprise-rag-docs-${var.environment}"
}

resource "aws_opensearch_domain" "rag" {
  domain_name    = "enterprise-rag-${var.environment}"
  engine_version = "OpenSearch_2.11"
  cluster_config {
    instance_type  = "t3.small.search"
    instance_count = 1
  }
  ebs_options {
    ebs_enabled = true
    volume_size = 20
  }
}

output "opensearch_endpoint" {
  value = aws_opensearch_domain.rag.endpoint
}

output "documents_bucket" {
  value = aws_s3_bucket.documents.bucket
}
