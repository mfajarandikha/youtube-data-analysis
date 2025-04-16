variable "bucket_name_source" {
  description = "The name of the GCS bucket."
  type        = string
}

variable "storage_class" {
  description = "Storage class of the bucket."
  type        = string
}

variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "region" {
  description = "GCP region."
  type        = string
}

variable "zone" {
  description = "GCP zone."
  type        = string
}


variable "dataset_id" {
  description = "BigQuery dataset ID."
  type        = string
}

variable "table_id" {
  description = "BigQuery table ID."
  type        = string
}

