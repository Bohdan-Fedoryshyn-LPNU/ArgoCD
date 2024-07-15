project_id = "southern-branch-429220-j9"
region     = "us-central1"

clusters = [
  {
    name              = "cluster-1"
    initial_node_count = 3
    node_config = {
      machine_type = "e2-medium"
      disk_size_gb = 10
    }
  },
  {
    name              = "cluster-2"
    initial_node_count = 3
    node_config = {
      machine_type = "e2-medium"
      disk_size_gb = 10
    }
  },
  {
    name              = "cluster-3"
    initial_node_count = 3
    node_config = {
      machine_type = "e2-medium"
      disk_size_gb = 10
    }
  }
]
