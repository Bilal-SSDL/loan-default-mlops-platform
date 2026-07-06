output "cluster_name" {
  value       = google_container_cluster.gke.name
  description = "GKE Cluster Name"
}

output "cluster_endpoint" {
  value       = google_container_cluster.gke.endpoint
  description = "GKE Cluster Endpoint"
}

output "cluster_ca_certificate" {
  value       = google_container_cluster.gke.master_auth[0].cluster_ca_certificate
  description = "GKE Cluster CA Certificate"
}

output "node_pool_name" {
  description = "Name of the node pool"
  value = google_container_node_pool.gke_node_pool.name
}
