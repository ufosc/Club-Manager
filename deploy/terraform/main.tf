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

locals {
  prefix = "${var.prefix}-${terraform.workspace}"
  common_tags = {
    Environment = terraform.workspace
    Project     = var.project
    Owner       = var.contact
    ManagedBy   = "Terraform"
  }
  cluster_name = "${local.prefix}-cluster"
}

data "aws_region" "current" {}