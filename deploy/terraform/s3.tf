module "clubmanager_static" {
  source      = "./modules/public-bucket"
  name        = "clubmanager-public"
  prefix      = local.prefix
  common_tags = local.common_tags
}
