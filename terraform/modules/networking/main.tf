resource "google_compute_network" "vpc" {
  name = var.vpc_name
  auto_create_subnetworks = var.auto_create_subnetworks

}

resource "google_compute_subnetwork" "public_subnet" {
  name          = var.public_subnet_name
  ip_cidr_range = var.public_cidr_range
  region        = var.region
  network       = google_compute_network.vpc.id

 # depends_on = [google_compute_network.vpc]

}

resource "google_compute_subnetwork" "private_subnet" {
  name          = var.private_subnet_name
  ip_cidr_range = var.private_cidr_range
  region        = var.region
  network       = google_compute_network.vpc.id

  private_ip_google_access = true

 # depends_on = [google_compute_network.vpc]

}

resource "google_compute_router" "router" {
  name    = var.router_name
  network = google_compute_network.vpc.id
  region  = var.region

}

resource "google_compute_router_nat" "nat" {
  name                               = var.nat_name
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY" // GCP automatically allocate external IP addresses for NAT
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES" //NAT covers all current and future subnets in the VPC network in this vpc

  depends_on = [google_compute_router.router]
}

