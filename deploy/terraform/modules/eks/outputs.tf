output "security_group" {
  description = "Security group created for the cluster, manages inbound/outbound access."
  value       = aws_security_group.this
}
