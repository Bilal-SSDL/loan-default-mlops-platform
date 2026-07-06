project_id          = "lendo-dr-417012"
region              = "us-central1"
zone                = "us-central1-a"
vpc_name            = "mlops-vpc"
public_subnet_name  = "mlops-public-subnet"
private_subnet_name = "mlops-private-subnet"
public_cidr_range   = "10.0.1.0/24"
private_cidr_range  = "10.0.2.0/24"
router_name         = "mlops-router"
nat_name            = "mlops-nat"

bucket_name       = "lendo-mlops-terraform-state"
bucket_versioning = true
bucket_location   = "US"

artifact_registry_repository_id = "mlops-artifact-repo"
artifact_registry_description   = "MLOps artifact registry repository"

cluster_name = "mlops-gke-cluster"

service_account_name = "mlops-service-account"
service_account_id   = "mlops-service-account"

node_pool_name = "mlops-primary-node-pool"
machine_type   = "e2-standard-2"
min_node_count = 1
max_node_count = 2
spot           = true
