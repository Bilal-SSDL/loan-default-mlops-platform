variable "repository_id" {
  description = "Repo Name"
  type = string
}

variable "repository_location" {
  description = "Repo location"
  type = string
}

variable "description" {
  description = "Repository description"
  type        = string
  default     = "Docker repository for MLOps platform"
}