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

