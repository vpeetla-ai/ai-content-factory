terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

variable "aws_region" { default = "us-east-1" }
variable "environment" { default = "demo" }

provider "aws" { region = var.aws_region }

resource "aws_ecs_cluster" "acf" {
  name = "content-factory-${var.environment}"
}

resource "aws_db_instance" "postgres" {
  identifier        = "acf-${var.environment}"
  engine            = "postgres"
  instance_class    = "db.t4g.micro"
  allocated_storage = 20
  username          = "acfadmin"
  password          = "CHANGE_ME"
  skip_final_snapshot = true
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "acf-redis-${var.environment}"
  engine               = "redis"
  node_type            = "cache.t4g.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
}

output "ecs_cluster" { value = aws_ecs_cluster.acf.name }
output "rds_endpoint" { value = aws_db_instance.postgres.endpoint }
output "redis_endpoint" { value = aws_elasticache_cluster.redis.cache_nodes[0].address }
