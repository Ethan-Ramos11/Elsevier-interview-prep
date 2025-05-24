terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}


resource "aws_s3_bucket" "module-buckets"{
  bucket_prefix = "${var.bucket_prefix}-${var.project_name}-${var.environment}"
  
  force_destroy = true
  tags = var.tags
}
