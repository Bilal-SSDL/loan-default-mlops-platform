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