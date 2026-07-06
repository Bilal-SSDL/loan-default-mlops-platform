output "repositry_id" {
  description = "Name of the newly created repository"
  value = google_artifact_registry_repository.image_repo.repository_id
}

output "repository_location" {
  description = "Location of the newly created repository"
  value = google_artifact_registry_repository.image_repo.location
}

output "repository_url" {
  description = "URL of the newly created repository"
  value = google_artifact_registry_repository.image_repo.id
}

output "repository_name" {
  description = "Name of the newly created repository"
  value = google_artifact_registry_repository.image_repo.name
}



