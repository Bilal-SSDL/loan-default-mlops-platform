output "vpc_id" {
  description = "vpc id"
  value       = module.networking.vpc_id
}

output "vpc_name" {
  description = "vpc name"
  value       = module.networking.vpc_name
}

output "vpc_self_link" {
  description = "vpc self link"
  value       = module.networking.vpc_self_link
}

output "private_subnet_name" {
  description = "private subnet name"
  value       = module.networking.private_subnet_name
}

output "public_subnet_name" {
  description = "public subnet name"
  value       = module.networking.public_subnet_name
}

output "bucket_name" {
  description = "name of gcs bucket created"
  value       = module.storage.bucket_name
}

output "bucket_url" {
  description = "url of the bucket"
  value       = module.storage.bucket_url
}

output "artifact_repositroy_name" {
  description = "Docker images repo name"
  value       = module.artifact_registry.repository_name
}

output "gke_cluster_name" {
  value       = module.gke.cluster_name
  description = "GKE Cluster Name"
}

output "gke_cluster_endpoint" {
  value       = module.gke.cluster_endpoint
  description = "GKE Cluster Endpoint"
}

output "service_account_name" {
  value       = module.service_account.service_account_name
  description = "Service Account Name"
}

output "node_pool_name" {
  value       = module.gke.node_pool_name
  description = "GKE Node Pool Name"
}




