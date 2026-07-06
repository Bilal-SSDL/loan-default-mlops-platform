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

variable "bucket_versioning" {
  description = "whether to enable versioning for the GCS bucket"
  type        = bool
  default     = true
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

