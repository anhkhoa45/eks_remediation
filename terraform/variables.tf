variable "region" {
	type = string
  default = "us-east-1"
}

variable "profile" {
	type = string
  default = "default"
}

variable "app" {
  type = string
  default = "app"
}

variable "env" {
  type = string
  description = "Environment"
  default = "dev"
}

# VPC variables
variable "vpc_cidr_prefix" {
  type = string
  default = "10.0"
}

# EKS variables
variable "eks_public_access" {
  type = bool
  default = false
}

variable "eks_public_access_whitelist" {
  type = list(string)
  default = [ "0.0.0.0" ]
}

variable "eks_use_spot_instance" {
  type = bool
  default = false
}

variable "eks_node_types" {
  type = list(string)
  default = ["t3.medium", "t3a.medium", "t2.medium"]
}
