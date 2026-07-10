project_id          = "lendo-dr-417012"
region              = "us-central1"
zone                = "us-central1-a"
vpc_name            = "lendo-app-vpc"
public_subnet_name  = "lendo-app-public-subnet"
private_subnet_name = "lendo-app-private-subnet"
public_cidr_range   = "10.0.1.0/24"
private_cidr_range  = "10.0.2.0/24"
router_name         = "lendo-app-router"
nat_name            = "lendo-app-nat"

bucket_name       = "lendo-mlops-terraform-state"
bucket_versioning = true
bucket_location   = "US"

artifact_registry_repository_id = "lendo-app-artifact-repo"
artifact_registry_description   = "lendo-app artifact registry repository"

cluster_name = "lendo-app-gke-cluster"

service_account_name = "lendo-app-service-account"
service_account_id   = "lendo-app-service-account"

node_pool_name = "lendo-app-primary-node-pool"
machine_type   = "e2-standard-2"
min_node_count = 1
max_node_count = 3
spot           = false
