terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file("creds.json")
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}
