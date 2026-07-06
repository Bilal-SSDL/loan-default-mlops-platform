output "service_account_name" {
  description = "Name of the service account"
  value = google_service_account.service_account.name
}

output "service_account_email" {
  description = "Email of the service account"
  value = google_service_account.service_account.email
}
