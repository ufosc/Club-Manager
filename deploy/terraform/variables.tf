#############################
## General
#############################
variable "prefix" {
  default = "clubs"
}

variable "project" {
  default = "Club Manager"
}

variable "contact" {
  default = "web@ikehunter.dev"
}

#############################
## Database 
#############################
variable "cluster_db_name" {
  description = "Postgres database name."
  type        = string
  default     = "clusterdb"
}
variable "cluster_db_username" {
  description = "Postgres database auth username."
  type        = string
  sensitive   = true
}
