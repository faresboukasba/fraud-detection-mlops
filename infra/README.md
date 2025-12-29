# Infrastructure as Code (Terraform)

This directory contains the Infrastructure as Code (IaC) for the Fraud Detection API using Terraform.

## Architecture

```
GitHub (CI/CD)
    ↓
ECR (Docker Image Registry)
    ↓
App Runner (Managed Container Service)
    ↓
CloudWatch (Logs & Monitoring)
```

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured with appropriate credentials
- AWS Account with permissions for ECR, App Runner, IAM, and CloudWatch

## Files

- `terraform.tf` - Terraform provider and backend configuration
- `variables.tf` - Input variables
- `main.tf` - Main infrastructure resources (ECR, App Runner, IAM)
- `outputs.tf` - Output values
- `terraform.tfvars` - Variable values (example)

## Resources Created

### 1. ECR Repository
- Private Docker image registry
- Image scanning enabled
- Lifecycle policy (keeps last 10 images)

### 2. App Runner Service
- Managed container service
- Auto-deployments from ECR enabled
- Health check configured (/health endpoint)
- CPU: 1024 (1 vCPU)
- Memory: 2048 MB (2 GB)

### 3. IAM Roles & Policies
- **App Runner ECR Access Role**: Allows App Runner to pull images from ECR
- **GitHub Actions Role**: Allows GitHub Actions to push to ECR and deploy to App Runner

### 4. CloudWatch
- Log group for App Runner service logs
- 7-day retention policy

## Setup Instructions

### 1. Initialize Terraform

```bash
cd infra
terraform init
```

### 2. Plan Deployment

```bash
terraform plan -var-file="terraform.tfvars"
```

### 3. Apply Configuration

```bash
terraform apply -var-file="terraform.tfvars"
```

### 4. Get Outputs

```bash
terraform output
```

Example output:
```
apprunner_service_url = "https://2sdeaedszk.eu-west-3.awsapprunner.com"
ecr_repository_url = "073184925698.dkr.ecr.eu-west-3.amazonaws.com/fraud-detection-api"
github_actions_role_arn = "arn:aws:iam::073184925698:role/GitHubActionsRole"
```

## Variable Customization

Edit `terraform.tfvars` to customize:

- `aws_region` - AWS region for deployment
- `environment` - Environment name (dev, staging, prod)
- `instance_cpu` - CPU allocation (256, 512, 1024, 2048)
- `instance_memory` - Memory allocation (512, 1024, 2048, 3072, 4096)
- `github_repo` - GitHub repository for OIDC trust relationship

## Destroying Infrastructure

To remove all resources:

```bash
terraform destroy -var-file="terraform.tfvars"
```

## Remote State Management (Optional)

For team collaboration, use S3 backend:

1. Create S3 bucket and DynamoDB table (one-time setup)
2. Uncomment backend configuration in `terraform.tf`
3. Run `terraform init` to migrate state

```bash
# One-time setup
aws s3 mb s3://fraud-detection-tf-state --region eu-west-3
aws dynamodb create-table \
  --table-name terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-west-3
```

## Monitoring & Logs

Access logs from App Runner:

```bash
aws logs tail /aws/apprunner/fraud-detection-api --follow
```

## Troubleshooting

### App Runner service fails to start
- Check ECR image exists: `aws ecr describe-images --repository-name fraud-detection-api`
- Check health endpoint: `curl https://<service-url>/health`
- Review logs: `aws logs tail /aws/apprunner/fraud-detection-api`

### GitHub Actions deployment fails
- Verify IAM role has correct trust relationship
- Check OIDC provider is configured in AWS account
- Review GitHub Actions secrets and environment variables

## Cost Estimation

- **ECR**: ~$0.10/month (first 1GB free per month)
- **App Runner**: ~$5.40/month (1024 CPU, 2048 MB memory, always active)
- **CloudWatch Logs**: ~$0.50/month (7-day retention)

**Total estimated cost: ~$6/month** (development usage)

## Next Steps

1. Push code to GitHub main/master branch
2. GitHub Actions will automatically:
   - Run tests
   - Build Docker image
   - Push to ECR
   - Deploy to App Runner
3. Monitor service health in CloudWatch
4. Scale as needed by modifying CPU/Memory variables
