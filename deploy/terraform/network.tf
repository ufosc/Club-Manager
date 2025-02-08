locals {
  private_subnet_ids         = [for subnet in module.network.private_subnets : subnet.id]
  private_subnet_cidr_blocks = [for subnet in module.network.private_subnets : subnet.cidr_block]
}

# Virtual Private Cloud
module "network" {
  source      = "./modules/vpc"
  prefix      = local.prefix
  common_tags = local.common_tags

  cidr_block_prefix = "10.0"
}
