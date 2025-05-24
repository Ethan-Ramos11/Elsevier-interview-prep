terraform {
  backend "s3" {
    bucket = "er-terraform-state-20250523"  
    key    = "resources/terraform.tfstate"   
    region = "us-east-2"
    dynamodb_table = "er-terraform-locks"
  }
}
