terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.curr_region
}

resource "aws_s3_bucket" "test-buckets"{
  bucket_prefix = "${var.bucket_prefix}-${var.project_name}-${var.environment}"
  
  force_destroy = true
  tags = var.tags
}
