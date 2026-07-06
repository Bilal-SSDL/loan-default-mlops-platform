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

