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
