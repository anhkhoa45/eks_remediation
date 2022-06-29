-   [AWS EKS security groups allow incoming traffic only on TCP port 443.](#aws-eks-security-groups-allow-incoming-traffic-only-on-tcp-port-443.)
    -   [Remediation resource:](#remediation-resource)
    -   [Resource metadata](#resource-metadata)
    -   [Why remediation?](#why-remediation)
    -   [Remediation or solution steps](#remediation-or-solution-steps)
        -   [Roles and Permissions required for the IAM user to execute the remediation.](#roles-and-permissions-required-for-the-iam-user-to-execute-the-remediation.)
    -   [How to setup the infrastructure for testing?](#how-to-setup-the-infrastructure-for-testing)
    -   [How to run the remediation script?](#how-to-run-the-remediation-script)
    -   [Details about the variables/parameters used](#details-about-the-variablesparameters-used)
-   [Envelope encryption for EKS Kubernetes Secrets is enabled using Amazon KMS.](#envelope-encryption-for-eks-kubernetes-secrets-is-enabled-using-amazon-kms.)
    -   [Remediation resource:](#remediation-resource-1)
    -   [Resource metadata](#resource-metadata-1)
    -   [Why remediation?](#why-remediation-1)
    -   [Remediation or solution steps](#remediation-or-solution-steps-1)
        -   [Roles and Permissions required for the IAM user to execute the remediation.](#roles-and-permissions-required-for-the-iam-user-to-execute-the-remediation.-1)
    -   [How to setup the infrastructure for testing?](#how-to-setup-the-infrastructure-for-testing-1)
    -   [How to run the remediation script?](#how-to-run-the-remediation-script-1)
    -   [Details about the variables/parameters used](#details-about-the-variablesparameters-used-1)
-   [File/folder details - names and purpose.](#filefolder-details---names-and-purpose.)



# AWS EKS security groups allow incoming traffic only on TCP port 443.

Automatically remove all ingress rules that doesn't have protocol = TCP and port = 443

## Remediation resource:

EKS cluster's security groups

## Resource metadata

Ingress security group rules must match following condition:

-   `IpProtocol == "tcp"`

-   `FromPort == 443`

-   `ToPort == 443`

## Why remediation?

```
The minimum rules for the control plane security group allows port 443 inbound from the worker node SG. This rule is what allows the kubelets to communicate with the Kubernetes API server.

Source: https://aws.github.io/aws-eks-best-practices/security/docs/network/#security-groups
```

## Remediation or solution steps

-   Describe cluster

-   Get cluster's security groups

-   Descibe security groups rules

-   Revoke non-compliance rules

### Roles and Permissions required for the IAM user to execute the remediation.

```
eks:ListClusters
eks:DescribeCluster
ec2:DescribeSecurityGroups
ec2:DescribeSecurityGroupRules
ec2:RevokeSecurityGroupIngress
```

## How to setup the infrastructure for testing?

```shell
cd terraform
```

Modify variables

```shell
cp sample.tfvars dev.tfvars
vi dev.tfvars # Using appropriate values
```

Provision the infrastructure

```shell
terraform init
terraform plan
terraform apply -var-file dev.tfvars -state dev.tfstate
```

## How to run the remediation script?

```shell
cd ansible
```

Create virtual environment & install dependencies

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Modify variables

```shell
cp variables.sample.yml variables.yml
vi variables.yml # Using appropriate values
```

Run remediation playbook

```shell
ansible-playbook eks_security_group.yml
```

## Details about the variables/parameters used

-   cluster_name: the EKS cluster name to remediate issue

# Envelope encryption for EKS Kubernetes Secrets is enabled using Amazon KMS.

Automatically enable envelope encryption (if haven't been enabled) for an EKS cluster

## Remediation resource:

EKS cluster

## Resource metadata

-   eks_cluster.encryption_config

## Why remediation?

Reference: https://aws.amazon.com/about-aws/whats-new/2020/03/amazon-eks-adds-envelope-encryption-for-secrets-with-aws-kms/

## Remediation or solution steps

-   Describe cluster

-   Check encryption_config metadata

-   If encryption_config isn't enabled, create new KMS key and associate
    with cluster

### Roles and Permissions required for the IAM user to execute the remediation.

```
eks:ListClusters
eks:DescribeCluster
eks:AssociateEncryptionConfig
kms:List*
kms:Get*
kms:Describe*
kms:CreateKey
kms:PutKeyPolicy
kms:TagResource
kms:CreateAlias
kms:EnableKey
```

## How to setup the infrastructure for testing?

```shell
cd terraform
```

Modify variables

```shell
cp sample.tfvars dev.tfvars
vi dev.tfvars # Using appropriate values
```

Provision the infrastructure

```shell
terraform init
terraform plan
terraform apply -var-file dev.tfvars -state dev.tfstate
```

## How to run the remediation script?

```shell
cd ansible
```

Create virtual environment & install dependencies

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Modify variables

```shell
cp variables.sample.yml variables.yml
vi variables.yml # Using appropriate values
```

Run remediation playbook

```shell
ansible-playbook secret_encryption.yml
```

## Details about the variables/parameters used

-   cluster_name: the EKS cluster name to remediate issue

# File/folder details - names and purpose.

```
ansible/
  library/                                    - custom ansible modules
    eks_cluster_facts.py                      - module to get infos of an eks cluster
    remove_non_tcp_443_ingress_sg_rules.py    - module to remove all non tcp 443 ingress rule from a security group
    eks_associate_encryption_config.py        - module to associate secret encryption config to an existing eks cluster
  policy/
    kms_policy.json                           - policy document for secret encryption kms
  eks_security_group.yml                      - playbook for EKS cluster security group remediation
  secret_encryption.yml                       - playbook for EKS cluster secret encryption remediation
terraform/
  
```
