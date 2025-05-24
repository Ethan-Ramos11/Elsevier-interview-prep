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
  region = "us-east-2"
}


module "dev-buckets" {
  source = "./modules/s3-operations"

  environment = "dev"
  tags = {
    Environment = "development"        
    Project     = "elsevier-prep"
    ManagedBy   = "terraform"
    Purpose     = "document-storage"
    Owner       = "ethan"
  }
}

module "prod-buckets" {
  source = "./modules/s3-operations"
  environment = "prod"
  tags = {
    Environment = "production"        
    Project     = "elsevier-prep"
    ManagedBy   = "terraform"
    Purpose     = "document-storage"
    Owner       = "ethan"
  }
}
