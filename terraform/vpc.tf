locals {
  vpc_name = "${var.app}-${var.env}-vpc"
  vpc_cidr_prefix = var.vpc_cidr_prefix
}

data "aws_availability_zones" "azs" {
  state = "available"
}

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = ">= 3.14.2"

  name = local.vpc_name
  cidr = "${local.vpc_cidr_prefix}.0.0/16"

  azs             = slice(data.aws_availability_zones.azs.names, 0, 3)
  private_subnets = ["${local.vpc_cidr_prefix}.0.0/19", "${local.vpc_cidr_prefix}.32.0/19", "${local.vpc_cidr_prefix}.64.0/19"]
  public_subnets  = ["${local.vpc_cidr_prefix}.96.0/19", "${local.vpc_cidr_prefix}.128.0/19", "${local.vpc_cidr_prefix}.160.0/19"]

  enable_nat_gateway  = true
  single_nat_gateway  = true

  tags = {
    Terraform   = "true"
    Application = var.app
    Environment = var.env
  }
}