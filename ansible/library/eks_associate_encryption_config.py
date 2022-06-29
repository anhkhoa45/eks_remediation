#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: eks_associate_encrytion_config
version_added: 1.0.0
short_description: Associate encryption configuration to an existing cluster.
description:
  - Associate encryption configuration to an existing cluster.
author:
  - Khoa Nguyen Dao Anh (@anhkhoa45)
options:
  cluster_name:
    description: EKS cluster name.
    required: true
    type: str
  key_arn:
    description: KMS key arn.
    required: true
    type: str
extends_documentation_fragment:
- amazon.aws.aws
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.
- name: Associate encryption configuration.
  eks_associate_encrytion_config:
    cluster_name: kri-dev-cluster
    key_arn: “arn:aws:kms:aws-region:123456789012:key/abcd1234-abcd-1234-5678-ef1234567890
'''

RETURN = '''
arn:
  description: ARN of the EKS cluster
  returned: when state is present
  type: str
  sample: arn:aws:eks:us-west-2:111111111111:cluster/my-eks-cluster
certificate_authority:
  description: Dictionary containing Certificate Authority Data for cluster
  returned: after creation
  type: complex
  contains:
    data:
      description: Base-64 encoded Certificate Authority Data for cluster
      returned: when the cluster has been created and is active
      type: str
endpoint:
  description: Kubernetes API server endpoint
  returned: when the cluster has been created and is active
  type: str
  sample: https://API_SERVER_ENDPOINT.yl4.us-west-2.eks.amazonaws.com
created_at:
  description: Cluster creation date and time
  returned: when state is present
  type: str
  sample: '2018-06-06T11:56:56.242000+00:00'
name:
  description: EKS cluster name
  returned: when state is present
  type: str
  sample: my-eks-cluster
resources_vpc_config:
  description: VPC configuration of the cluster
  returned: when state is present
  type: complex
  contains:
    security_group_ids:
      description: List of security group IDs
      returned: always
      type: list
      sample:
      - sg-abcd1234
      - sg-aaaa1111
    subnet_ids:
      description: List of subnet IDs
      returned: always
      type: list
      sample:
      - subnet-abcdef12
      - subnet-345678ab
      - subnet-cdef1234
    vpc_id:
      description: VPC id
      returned: always
      type: str
      sample: vpc-a1b2c3d4
role_arn:
  description: ARN of the IAM role used by the cluster
  returned: when state is present
  type: str
  sample: arn:aws:iam::111111111111:role/eks_cluster_role
status:
  description: status of the EKS cluster
  returned: when state is present
  type: str
  sample:
  - CREATING
  - ACTIVE
version:
  description: Kubernetes version of the cluster
  returned: when state is present
  type: str
  sample: '1.10'
'''

try:
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def eks_associate_encryption_config(eks_client, module):

    cluster_name = module.params.get("cluster_name")
    key_arn = module.params.get("key_arn")

    try:
        eks_client.associate_encryption_config(
            aws_retry=True,
            clusterName=cluster_name,
            encryptionConfig=[
                {
                    'resources': [
                        'secrets',
                    ],
                    'provider': {
                        'keyArn': key_arn
                    }
                },
            ],
        )
        cluster = eks_client.describe_cluster(aws_retry=True, name=cluster_name)['cluster']
        cluster = camel_dict_to_snake_dict(cluster)
    except (ClientError, BotoCoreError) as err:
        module.fail_json_aws(err, msg="error describing cluster")
    module.exit_json(**cluster)


def main():
    argument_spec = dict(
      cluster_name=dict(required=True),
      key_arn=dict(required=True)
    )

    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    eks_client = module.client('eks', retry_decorator=AWSRetry.jittered_backoff())

    eks_associate_encryption_config(eks_client, module)


if __name__ == '__main__':
    main()