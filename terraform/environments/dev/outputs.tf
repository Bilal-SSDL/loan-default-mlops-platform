output "vpc_id" {
  description = "vpc id"
  value       = module.networking.vpc_id
}

output "vpc_name" {
  description = "vpc name"
  value       = module.networking.vpc_name
}

output "vpc_self_link" {
  description = "vpc self link"
  value       = module.networking.vpc_self_link
}

output "private_subnet_name" {
  description = "private subnet name"
  value       = module.networking.private_subnet_name
}

output "public_subnet_name" {
  description = "public subnet name"
  value       = module.networking.public_subnet_name
}



