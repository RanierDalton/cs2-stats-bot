output "instance_id" {
  description = "ID da instância EC2"
  value       = aws_instance.bot_server.id
}

output "instance_public_ip" {
  description = "IP público da instância EC2 (Elastic IP)"
  value       = aws_eip.bot_eip.public_ip
}

output "instance_public_dns" {
  description = "DNS público da instância EC2"
  value       = aws_instance.bot_server.public_dns
}

output "security_group_id" {
  description = "ID do Security Group"
  value       = aws_security_group.bot_sg.id
}

output "ssh_command" {
  description = "Comando SSH para conectar à instância"
  value       = "ssh -i ~/.ssh/${var.key_name}.pem ubuntu@${aws_eip.bot_eip.public_ip}"
}

output "https_url" {
  description = "URL HTTPS do bot (se domínio configurado)"
  value       = var.domain_name != "" ? "https://${var.domain_name}" : "https://${aws_eip.bot_eip.public_ip}"
}
