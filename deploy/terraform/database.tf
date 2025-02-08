resource "random_password" "database_passwords" {
  count   = 1
  length  = 25
  special = false
}

locals {
  cluster_db_password = random_password.database_passwords[0].result
}


module "core_database" {
  source        = "./modules/rds"
  prefix        = local.prefix
  common_tags   = local.common_tags
  resource_name = "cluster-db"

  db_name                  = var.cluster_db_name
  db_username              = var.cluster_db_username
  db_password              = local.cluster_db_password
  engine_version           = "12.19"
  enable_blue_green_update = true
  enable_final_snapshot    = true
  create_from_snapshot     = ""

  vpc_id                  = module.vpc.vpc_id
  subnet_ids              = [for subnet in module.vpc.private_subnets : subnet.id]
  ingress_cidr_blocks     = [for subnet in module.vpc.private_subnets : subnet.cidr_block]
  ingress_security_groups = []
  # ingress_security_groups = [aws_security_group.eks.id]
}
