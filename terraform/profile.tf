terraform {
  required_version = ">= 1.1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.5"
    }
  }
}

provider "aws" {
  profile = var.profile
  region  = var.region
}