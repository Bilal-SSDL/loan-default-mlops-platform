terraform {
  backend "gcs" {
    bucket = "lendo-mlops-terraform-state"
    prefix = "environment/dev"
    #key    = "terraform.tfstate"
  }
}