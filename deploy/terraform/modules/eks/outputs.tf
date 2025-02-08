output "security_group" {
  description = "Security group created for the cluster, manages inbound/outbound access."
  value       = aws_security_group.this
}

output "oidc_provider_url" {
  description = "Url used to look up aws_iam_openid_connect_provider resource."
  value       = aws_iam_openid_connect_provider.this.url
}

output "cluster_name" {
  description = "Identifier for the created EKS cluster."
  value       = aws_eks_cluster.this.name
}
