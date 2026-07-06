resource "google_container_cluster" "gke" {
  name               = var.cluster_name
  location           = var.region
  initial_node_count = 1
  network            = var.network
  subnetwork         = var.subnetwork
  remove_default_node_pool = true
  deletion_protection = false

}