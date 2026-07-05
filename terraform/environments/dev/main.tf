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
}