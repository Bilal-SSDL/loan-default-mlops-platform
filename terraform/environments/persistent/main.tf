# Root module
# Child modules will be added here as we build the infrastructure.

module "storage" {
  source            = "../../modules/storage"
  bucket_name       = var.bucket_name
  location          = var.region
  bucket_versioning = var.bucket_versioning

}

module "artifact_registry" {
  source              = "../../modules/artifact-registry"
  repository_id       = var.artifact_registry_repository_id
  repository_location = var.region
  description         = var.artifact_registry_description

}

module "service_account" {
  source = "../../modules/service-account"

  project_id   = var.project_id
  display_name = var.service_account_name
  account_id   = var.service_account_id


}

# Allow the GKE node pool service account to pull images from Artifact Registry.
# Without this the node cannot authorize against the repo and image pulls fail
# with "403 Forbidden" when fetching the pull token. Scoped to the single repo
# to keep with the least-privilege IAM decision.
resource "google_artifact_registry_repository_iam_member" "node_pool_reader" {
  project    = var.project_id
  location   = module.artifact_registry.repository_location
  repository = module.artifact_registry.repositry_id
  role       = "roles/artifactregistry.reader"
  member     = "serviceAccount:${module.service_account.service_account_email}"
}




