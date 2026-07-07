resource "google_artifact_registry_repository" "image_repo" {
  description = var.description
  location = var.repository_location
  repository_id = var.repository_id

  format = "DOCKER"

}