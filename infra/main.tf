# ECR Repository
resource "aws_ecr_repository" "fraud_detection" {
  name                 = var.app_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}-ecr"
  }
}

# ECR Repository Lifecycle Policy
resource "aws_ecr_lifecycle_policy" "fraud_detection" {
  repository = aws_ecr_repository.fraud_detection.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "any"
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# IAM Role for App Runner to access ECR
resource "aws_iam_role" "apprunner_ecr_access" {
  name = "${var.app_name}-apprunner-ecr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = [
            "build.apprunner.amazonaws.com",
            "tasks.apprunner.amazonaws.com"
          ]
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name = "${var.app_name}-apprunner-ecr-role"
  }
}

# ECR Access Policy for App Runner
resource "aws_iam_role_policy_attachment" "apprunner_ecr_access" {
  role       = aws_iam_role.apprunner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

# App Runner Service
resource "aws_apprunner_service" "fraud_detection" {
  service_name = var.app_name

  source_configuration {
    image_repository {
      image_identifier      = var.docker_image_uri
      image_repository_type = "ECR"
      image_configuration {
        port = tostring(var.container_port)
      }
    }
    auto_deployments_enabled = var.auto_deployments_enabled
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }
  }

  instance_configuration {
    cpu    = var.instance_cpu
    memory = var.instance_memory
  }

  # Health check configuration
  health_check_configuration {
    protocol            = "HTTP"
    path                = "/health"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  tags = {
    Name = "${var.app_name}-service"
  }

  depends_on = [aws_iam_role_policy_attachment.apprunner_ecr_access]
}

# CloudWatch Log Group for App Runner
resource "aws_cloudwatch_log_group" "apprunner" {
  count             = var.enable_monitoring ? 1 : 0
  name              = "/aws/apprunner/${var.app_name}"
  retention_in_days = 7

  tags = {
    Name = "${var.app_name}-logs"
  }
}

# IAM Role for GitHub Actions
resource "aws_iam_role" "github_actions" {
  name = "GitHubActionsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Federated = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/token.actions.githubusercontent.com"
        }
        Action = "sts:AssumeRoleWithWebIdentity"
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_repo}:*"
          }
        }
      }
    ]
  })

  tags = {
    Name = "github-actions-role"
  }
}

# GitHub Actions Policy - ECR Push
resource "aws_iam_role_policy" "github_ecr" {
  name = "${var.app_name}-github-ecr-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:GetAuthorizationToken"
        ]
        Resource = aws_ecr_repository.fraud_detection.arn
      },
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken"
        ]
        Resource = "*"
      }
    ]
  })
}

# GitHub Actions Policy - App Runner Deploy
resource "aws_iam_role_policy" "github_apprunner" {
  name = "${var.app_name}-github-apprunner-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "apprunner:StartDeployment",
          "apprunner:DescribeService",
          "apprunner:ListServices"
        ]
        Resource = "*"
      }
    ]
  })
}

# Get AWS account ID
data "aws_caller_identity" "current" {}
# ========================================
# Streamlit UI Service
# ========================================

# ECR Repository for Streamlit UI
resource "aws_ecr_repository" "streamlit_ui" {
  name                 = "${var.app_name}-ui"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "${var.app_name}-ui-ecr"
  }
}

# ECR Lifecycle Policy for Streamlit
resource "aws_ecr_lifecycle_policy" "streamlit_ui" {
  repository = aws_ecr_repository.streamlit_ui.name

  policy = jsonencode({
    rules = [
      {
        rulePriority = 1
        description  = "Keep last 10 images"
        selection = {
          tagStatus     = "any"
          countType     = "imageCountMoreThan"
          countNumber   = 10
        }
        action = {
          type = "expire"
        }
      }
    ]
  })
}

# App Runner Service for Streamlit UI
resource "aws_apprunner_service" "streamlit_ui" {
  service_name = "${var.app_name}-ui"

  source_configuration {
    image_repository {
      image_identifier      = "${aws_ecr_repository.streamlit_ui.repository_url}:latest"
      image_repository_type = "ECR"

      image_configuration {
        port = "8501"
        runtime_environment_variables = {
          API_URL = "https://${aws_apprunner_service.fraud_detection.service_url}"
        }
      }
    }

    auto_deployments_enabled = true

    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }
  }

  instance_configuration {
    cpu    = var.instance_cpu
    memory = var.instance_memory
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/_stcore/health"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 3
  }

  depends_on = [aws_iam_role_policy_attachment.apprunner_ecr]

  tags = {
    Name = "${var.app_name}-ui"
  }
}

# GitHub Actions Policy - ECR Push for UI
resource "aws_iam_role_policy" "github_ecr_ui" {
  name = "${var.app_name}-github-ecr-ui-policy"
  role = aws_iam_role.github_actions.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart",
          "ecr:CompleteLayerUpload",
          "ecr:GetAuthorizationToken"
        ]
        Resource = aws_ecr_repository.streamlit_ui.arn
      }
    ]
  })
}