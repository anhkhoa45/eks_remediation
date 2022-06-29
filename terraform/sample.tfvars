app = "app"
env = "dev"
profile = "aws-profile"

vpc_cidr_prefix = "10.0"

eks_public_access = true
eks_public_access_whitelist = ["1.2.3.4/32"]
eks_use_spot_instance = true
eks_node_types = ["t3.medium"]
