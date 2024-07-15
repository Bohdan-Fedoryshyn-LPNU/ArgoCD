# Провайдер
provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("${path.module}/credentials.json")
}

# Ввімкнення Kubernetes Engine API
# resource "google_project_service" "enable_kubernetes_api" {
#   project = var.project_id
#   service = "container.googleapis.com"
# }

# Створення кластерів GKE
resource "google_container_cluster" "primary" {
  for_each = { for cluster in var.clusters : cluster.name => cluster }

#   depends_on = [google_project_service.enable_kubernetes_api]

  name               = each.value.name
  location           = var.region
  initial_node_count = each.value.initial_node_count

  node_config {
    machine_type = each.value.node_config.machine_type
    disk_size_gb = each.value.node_config.disk_size_gb
  }
}

# Виведення імен кластерів
output "cluster_names" {
  value = [for cluster in google_container_cluster.primary : cluster.name]
}
