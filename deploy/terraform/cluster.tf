locals {
  cluster_name      = module.cluster.cluster_name
  oidc_provider_url = module.cluster.oidc_provider_url
}

##############################################
## MARK: Main Cluster Config
##############################################
module "cluster" {
  source        = "./modules/eks"
  prefix        = local.prefix
  resource_name = "cluster"
  common_tags   = local.common_tags

  scaling_config = {
    desired_size = 2
    max_size     = 2
    min_size     = 1
  }

  vpc_id = module.network.vpc_id
  ingress_access = [
    {
      description = "Allow traffic to proxy",
      port        = 8080,
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
  egress_access = [
    {
      description = "Allow responses to http (port 80)",
      port        = 80,
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "Allow responses to https (port 443)",
      port        = 443,
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "Allow requests from the cluster to the database"
      port        = 5432
      cidr_blocks = local.private_subnet_cidr_blocks
    }
  ]
  private_subnet_ids = local.private_subnet_ids
}

##############################################
## MARK: Service Accounts
##############################################

module "ebs_csi_sa" {
  source        = "./modules/eks-service-account"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "ebs-csi"

  cluster_name              = local.cluster_name
  service_account_namespace = "kube-system"
  service_account_name      = "ebs-csi-controller-sa"

  oidc_provider_url  = local.oidc_provider_url
  policy_description = "Allow EKS cluster to access EBS resources."
  policy_file        = file("./templates/eks/eks-ebs-service-role-policy.json")

  depends_on = [module.cluster]
}

module "secrets_manager_sa" {
  source        = "./modules/eks-service-account"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "secrets-manager"

  cluster_name              = local.cluster_name
  service_account_namespace = "cluster"
  service_account_name      = "secretsmanager-sa"

  oidc_provider_url  = local.oidc_provider_url
  policy_description = "Allow EKS cluster to access secrets manager."
  policy_file        = file("./templates/eks/eks-access-secrets-manager-policy.json")

  depends_on = [module.cluster]
}

module "vpc_cni_sa" {
  source        = "./modules/eks-service-account"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "vpc-cni"

  cluster_name              = local.cluster_name
  service_account_namespace = "kube-system"
  service_account_name      = "aws-node"

  oidc_provider_url  = local.oidc_provider_url
  policy_description = "Allow EKS cluster to access VPC CNI addon resources."
  policy_file        = file("./templates/eks/eks-vpccni-service-role-policy.json")

  depends_on = [module.cluster]
}

module "external_dns_sa" {
  source        = "./modules/eks-service-account"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "external-dns"

  cluster_name              = local.cluster_name
  service_account_namespace = "kube-system"
  service_account_name      = "external-dns"

  oidc_provider_url  = local.oidc_provider_url
  policy_description = "Allow EKS cluster to manage DNS resources with Route53."
  policy_file        = file("./templates/eks/eks-manage-dns-policy.json")

  depends_on = [module.cluster]
}

module "alb_controller_sa" {
  source        = "./modules/eks-service-account"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "alb-controller"

  cluster_name              = local.cluster_name
  service_account_namespace = "kube-system"
  service_account_name      = "aws-load-balancer-controller"

  oidc_provider_url  = local.oidc_provider_url
  policy_description = "Allow EKS cluster to manage application load balancer resources."
  policy_file        = file("./templates/eks/eks-manage-alb-policy.json")

  depends_on = [module.cluster]
}


##############################################
## MARK: EKS Addons
##############################################

resource "aws_eks_addon" "eks_ebs_addon" {
  addon_name               = "aws-ebs-csi-driver"
  cluster_name             = local.cluster_name
  service_account_role_arn = module.ebs_csi_sa.iam_role.arn
}

resource "aws_eks_addon" "eks_identity_agent_addon" {
  addon_name               = "eks-pod-identity-agent"
  cluster_name             = local.cluster_name
  service_account_role_arn = module.secrets_manager_sa.iam_role.arn
}

resource "aws_eks_addon" "eks_cni_addon" {
  addon_name               = "vpc-cni"
  cluster_name             = local.cluster_name
  service_account_role_arn = module.vpc_cni_sa.iam_role.arn
}
