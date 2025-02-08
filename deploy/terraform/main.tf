terraform {
    backend "s3" {
        bucket = "clubmanager-terraform-state"
        key = "clubmanager-terraform-state.tfstate"
        region = "us-east-1"
        encrypt = true
        dynamodb_table = "clubmanager-tf-state-lock"
    }
}

provider "aws" {
  region = "us-east-2"
}

provider "helm" {
  kubernetes {
    host                   = aws_eks_cluster.main.endpoint
    cluster_ca_certificate = base64decode(aws_eks_cluster.main.certificate_authority.0.data)
    exec {
      api_version = "client.authentication.k8s.io/v1"
      args        = ["eks", "get-token", "--cluster-name", aws_eks_cluster.main.id]
      command     = "aws"
    }
  }
}

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
}

data "aws_region" "current" {}