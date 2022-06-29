module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "18.24.1"

  cluster_name                    = "${var.app}-${var.env}-cluster"
  cluster_version                 = "1.22"
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = var.eks_public_access
  cluster_endpoint_public_access_cidrs = concat(
    var.eks_public_access_whitelist,
    [for nat_ip in module.vpc.nat_public_ips : "${nat_ip}/32"]
  )

  cluster_addons = {
    coredns = {
      resolve_conflicts = "OVERWRITE"
    }

    kube-proxy = {
      resolve_conflicts = "OVERWRITE"
    }

    vpc-cni = {
      resolve_conflicts = "OVERWRITE"
    }
  }

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # Extend cluster security group rules
  cluster_security_group_additional_rules = {
    api_access_from_vpc = {
      description                = "API server access from within VPC"
      protocol                   = "tcp"
      from_port                  = 443
      to_port                    = 443
      type                       = "ingress"
      cidr_blocks                = [module.vpc.vpc_cidr_block]
    }
    egress_nodes_ephemeral_ports_tcp = {
      description                = "To node 1025-65535"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "egress"
      source_node_security_group = true
    }
  }

  # Extend node-to-node security group rules
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all ports/protocols"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
    egress_all = {
      description      = "Node all egress"
      protocol         = "-1"
      from_port        = 0
      to_port          = 0
      type             = "egress"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
  }

  eks_managed_node_group_defaults = {
    ami_type               = "AL2_x86_64"
    disk_size              = 30
    instance_types         = var.eks_node_types
    iam_role_attach_cni_policy = true
  }

  # Default node group
  eks_managed_node_groups = {
    # "${var.app}-${var.env}-bl" = {}
    "${var.app}-${var.env}-gr" = {
      min_size     = 1
      max_size     = 10

      instance_types = var.eks_node_types
      capacity_type  = var.eks_use_spot_instance ? "SPOT" : "ON_DEMAND"

      iam_role_additional_policies = [
        "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
      ]

      labels = {
        Environment = var.env
        NodeGroup = "default"
      }
    }
  }

  tags = {
    Terraform   = "true"
    Application = var.app
    Environment = var.env
  }
}