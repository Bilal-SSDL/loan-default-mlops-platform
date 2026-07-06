resource "google_container_node_pool" "gke_node_pool" {
    name       = var.node_pool_name
    location   = var.region
    cluster    = google_container_cluster.gke.name
    #node_count = var.node_count
    autoscaling {
        min_node_count = var.min_node_count
        max_node_count = var.max_node_count
    }
    node_config {
        machine_type = var.machine_type
        service_account = var.service_account_email
        spot = var.spot

        shielded_instance_config {
            enable_secure_boot          = true
            enable_integrity_monitoring = true
        }

    

    oauth_scopes = [
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring"
     ]

    labels = {
        "env" = "dev"
        }
    }

    management {
        auto_upgrade = true
        auto_repair  = true
    }



  
}