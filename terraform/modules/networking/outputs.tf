output "vpc_id" {
  description = "ID of VPC"
  value = google_compute_network.vpc.id
}

output "vpc_name" {
  description = "Name of VPC"
  value = google_compute_network.vpc.name
}

output "vpc_self_link" {
    description = "Self link of VPC"
    value = google_compute_network.vpc.self_link
}

output "private_subnet_name" {
    description = "Name of Private Subnet"
    value = google_compute_subnetwork.private_subnet.name
}

output "public_subnet_name" {
    description = "Name of Public Subnet"
    value = google_compute_subnetwork.public_subnet.name
}

output "router_name" {
    description = "Name of Router"
    value = google_compute_router.router.name
}

output "nat_name" {
    description = "Name of NAT"
    value = google_compute_router_nat.nat.name
}
