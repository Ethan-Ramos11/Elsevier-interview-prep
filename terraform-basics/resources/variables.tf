# Core Configuration
variable "curr_region" {
  description = "Region in which the resource will be used"
  type = string
  default = "us-east-2"
}

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

# File Handling
variable "file_types" {
  description = "File types allowed to be uploaded to the S3 bucket"
  type = list(string)
  default = [
    "txt",
    "doc",
    "docx",
    "pdf"
  ]
}

variable "file_structure" {
  description = "Map of file types to their corresponding S3 folders"
  type = map(string)
  default = {
    "doc": "docs" 
    "docx": "docs"
    "txt": "texts"
    "pdf": "pdfs"
  }
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

variable "retention_hrs" {
  description = "Number of hours to retain objects"
  type        = number
  default     = 1
}

# Resource Tags
variable "tags" {
  description = "Resource tags"
  type = map(string)
  default = {
    Environment = "development"
    Project     = "elsevier-prep"
    ManagedBy   = "terraform"
    Purpose     = "document-storage"
    Owner       = "ethan"
  }
}
