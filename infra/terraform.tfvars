# Terraform Variables for Fraud Detection API

aws_region           = "eu-west-3"
project_name         = "fraud-detection"
environment          = "prod"
app_name             = "fraud-detection-api"
container_port       = 8000
instance_cpu         = "1024"
instance_memory      = "2048"
auto_deployments_enabled = true
github_repo          = "faresboukasba/fraud-detection-mlops"
enable_monitoring    = true
