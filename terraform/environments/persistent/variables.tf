variable "project_id" {
  description = "GCP project ID"
  type        = string
  default     = "loan-default-mlops-platform-007"

}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  type        = string
  default     = "us-central1-a"
}

variable "bucket_name" {
  description = "name of the GCS bucket"
  type        = string
}

variable "artifact_registry_repository_id" {
  description = "name of the artifact registry repository"
  type        = string
}

variable "artifact_registry_description" {
  description = "description of the artifact registry repository"
  type        = string
}


variable "bucket_versioning" {
  description = "whether to enable versioning for the GCS bucket"
  type        = bool
  default     = true
}

variable "cluster_name" {
  description = "name of the GKE cluster"
  type        = string
}

variable "service_account_name" {
  description = "name of the service account"
  type        = string
}

variable "service_account_id" {
  description = "id of the service account"
  type        = string
}

variable "bucket_location" {
  description = "location of the GCS bucket"
  type        = string
  default     = "us"
}

variable "vpc_name" {
  description = "name of vpc"
  type        = string
}

variable "auto_create_subnetworks" {
  description = "whether to auto create subnetworks"
  type        = bool
  default     = false
}

variable "public_subnet_name" {
  description = "name of public subnet"
  type        = string
}

variable "private_subnet_name" {
  description = "name of private subnet"
  type        = string
}

variable "public_cidr_range" {
  description = "cidr range of public subnet"
  type        = string
}

variable "private_cidr_range" {
  description = "cidr range of private subnet"
  type        = string
}

variable "router_name" {
  description = "name of cloud router"
  type        = string
}

variable "nat_name" {
  description = "name of cloud nat"
  type        = string
}

variable "node_pool_name" {
  description = "name of the node pool"
  type        = string
}

variable "machine_type" {
  description = "machine type for the node pool"
  type        = string
}

variable "min_node_count" {
  description = "minimum number of nodes in the node pool"
  type        = number
}

variable "max_node_count" {
  description = "maximum number of nodes in the node pool"
  type        = number
}

variable "spot" {
  description = "whether to use spot instances for the node pool"
  type        = bool
  default     = true
}

