# Variables
variable "project_id" {
  description = "The ID of the project in which to create the clusters."
  type        = string
}

variable "region" {
  description = "The region in which to create the clusters."
  type        = string
  default     = "us-central1"
}

variable "clusters" {
  description = "A list of cluster configurations."
  type = list(object({
    name           = string
    initial_node_count = number
    node_config = object({
      machine_type = string
      disk_size_gb = number
    })
  }))
}
