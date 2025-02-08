module "clubmanager_static" {
  source      = "./modules/public-bucket"
  resource_name        = "clubmanager-public"
  prefix      = local.prefix
  common_tags = local.common_tags
}
