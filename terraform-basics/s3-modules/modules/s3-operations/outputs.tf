output "bucket_name" {
  value = aws_s3_bucket.module-buckets.id
}

output "bucket_arn" {
  value = aws_s3_bucket.module-buckets.arn
}

output "bucket_domain_name" {
  value = aws_s3_bucket.module-buckets.bucket_domain_name
}

output "bucket_region" {
  value = aws_s3_bucket.module-buckets.region
}
