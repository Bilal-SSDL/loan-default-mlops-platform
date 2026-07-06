resource "google_storage_bucket" "terraform_state" {
  name     = var.bucket_name
  location = var.location

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  versioning {
    enabled = var.bucket_versioning
  }

  lifecycle {
    prevent_destroy = true
  }
  

}
