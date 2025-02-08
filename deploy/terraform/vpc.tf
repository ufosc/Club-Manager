# Virtual Private Cloud
module "vpc" {
  source      = "./modules/vpc"
  prefix      = local.prefix
  common_tags = local.common_tags

  cidr_block_prefix = "10.0"
}
