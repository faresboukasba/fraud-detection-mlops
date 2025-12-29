output "ecr_repository_url" {
  description = "ECR repository URL for API"
  value       = aws_ecr_repository.fraud_detection.repository_url
}

output "ecr_repository_arn" {
  description = "ECR repository ARN for API"
  value       = aws_ecr_repository.fraud_detection.arn
}

output "apprunner_service_arn" {
  description = "App Runner service ARN for API"
  value       = aws_apprunner_service.fraud_detection.arn
}

output "apprunner_service_url" {
  description = "App Runner service URL for API"
  value       = "https://${aws_apprunner_service.fraud_detection.service_url}"
}

output "apprunner_service_status" {
  description = "App Runner service status"
  value       = aws_apprunner_service.fraud_detection.status
}

# Streamlit UI Outputs
output "streamlit_ecr_repository_url" {
  description = "ECR repository URL for Streamlit UI"
  value       = aws_ecr_repository.streamlit_ui.repository_url
}

output "streamlit_apprunner_service_url" {
  description = "App Runner service URL for Streamlit UI"
  value       = "https://${aws_apprunner_service.streamlit_ui.service_url}"
}

output "streamlit_apprunner_service_status" {
  description = "Streamlit App Runner service status"
  value       = aws_apprunner_service.streamlit_ui.status
}

output "github_actions_role_arn" {
  description = "GitHub Actions IAM role ARN"
  value       = aws_iam_role.github_actions.arn
}

output "github_actions_role_name" {
  description = "GitHub Actions IAM role name"
  value       = aws_iam_role.github_actions.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name"
  value       = var.enable_monitoring ? aws_cloudwatch_log_group.apprunner[0].name : null
}
