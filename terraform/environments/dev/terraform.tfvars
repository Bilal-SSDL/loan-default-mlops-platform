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
bucket_name         = "lendo-mlops-terraform-state"
bucket_versioning   = true
bucket_location     = "US"

