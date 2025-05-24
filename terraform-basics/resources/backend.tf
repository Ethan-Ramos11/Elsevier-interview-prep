terraform {
  backend "s3" {
    bucket = "er20250523214535876500000001"
    key    = "resources/terraform.tfstate"   
    region = "us-east-2"
    dynamodb_table = "terraform-state-lock"
  }
}
