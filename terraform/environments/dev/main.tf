# Root module
# Child modules will be added here as we build the infrastructure.

module "networking" {
  source   = "../../modules/networking"
  vpc_name = var.vpc_name

  auto_create_subnetworks = var.auto_create_subnetworks
  region                  = var.region
  public_subnet_name      = var.public_subnet_name
  private_subnet_name     = var.private_subnet_name
  public_cidr_range       = var.public_cidr_range
  private_cidr_range      = var.private_cidr_range

  router_name = var.router_name
  nat_name    = var.nat_name
}

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

module "gke" {
  source       = "../../modules/gke"
  cluster_name = var.cluster_name
  region       = var.region
  network      = module.networking.vpc_name
  subnetwork   = module.networking.private_subnet_name
  project_id   = var.project_id

  node_pool_name = var.node_pool_name
  machine_type   = var.machine_type
  #node_count            = var.node_count
  min_node_count        = var.min_node_count
  max_node_count        = var.max_node_count
  spot                  = var.spot
  service_account_email = module.service_account.service_account_email


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




