variable "bucket_name" {
  description = "name of the GCS bucket"
  type        = string
}

variable "location" {
  description = "location of the GCS bucket"
  type        = string
}

variable "bucket_versioning" {
  description = "whether to enable versioning for the GCS bucket"
  type        = bool
  default     = true
}

