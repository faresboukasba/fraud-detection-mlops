variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-west-3"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "fraud-detection"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "fraud-detection-api"
}

variable "docker_image_uri" {
  description = "Docker image URI in ECR"
  type        = string
  default     = "073184925698.dkr.ecr.eu-west-3.amazonaws.com/fraud-detection-api:latest"
}

variable "container_port" {
  description = "Container port for the application"
  type        = number
  default     = 8000
}

variable "instance_cpu" {
  description = "CPU for App Runner instance"
  type        = string
  default     = "1024"
}

variable "instance_memory" {
  description = "Memory for App Runner instance"
  type        = string
  default     = "2048"
}

variable "auto_deployments_enabled" {
  description = "Enable automatic deployments on image push"
  type        = bool
  default     = true
}

variable "github_repo" {
  description = "GitHub repository for CI/CD"
  type        = string
  default     = "faresboukasba/fraud-detection-mlops"
}

variable "enable_monitoring" {
  description = "Enable CloudWatch monitoring"
  type        = bool
  default     = true
}
