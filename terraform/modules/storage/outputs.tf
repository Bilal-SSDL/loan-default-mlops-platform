output "bucket_name" {
  description = "name of gcs bucket created"
  value       = google_storage_bucket.terraform_state.name

}

output "bucket_url" {
  description = "url of gcs bucket created"
  value       = google_storage_bucket.terraform_state.url

}
