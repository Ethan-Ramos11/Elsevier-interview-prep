# Core Configuration
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "elsevier-prep"
}

# Resource Naming
variable "bucket_prefix" {
  description = "Prefix for S3 bucket names to ensure uniqueness"
  type = string
  default = "er"
}





# Security and Features
variable "enable_versioning" {
  description = "Enable S3 bucket versioning"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable server-side encryption"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable S3 access logging"
  type        = bool
  default     = true
}



# Resource Tags
variable "tags" {
  description = "Resource tags"
  type = map(string)
  default = {
    Environment = "dev"           
    Project     = "elsevier-prep"
    ManagedBy   = "terraform"
    Purpose     = "document-storage"
    Owner       = "ethan"
  }
}
