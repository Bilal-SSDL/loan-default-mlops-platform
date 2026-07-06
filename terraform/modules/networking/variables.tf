variable "vpc_name" {
  description = "name of vpc"
  type        = string
}


variable "auto_create_subnetworks" {
  description = "whether to auto create subnetworks"
  type        = bool
  default     = false
}

variable "private_subnet_name" {
  description = "name of private subnet"
  type        = string
}

variable "public_subnet_name" {
  description = "name of public subnet"
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

variable "region" {
  description = "GCP region"
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

