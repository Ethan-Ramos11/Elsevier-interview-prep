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
resource "aws_dynamodb_table" "terraform_locks" {
  name = "terraform-state-lock"
}
