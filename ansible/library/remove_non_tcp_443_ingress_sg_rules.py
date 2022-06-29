#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: remove_non_tcp_443_sg_rules
version_added: 1.0.0
short_description: Remove all inbound rules are configured to allow access on ports different than TCP port 443 (HTTPS)
description:
  - Remove all inbound rules are configured to allow access on ports different than TCP port 443 (HTTPS)
author:
  - Khoa Nguyen Dao Anh (@anhkhoa45)
options:
  security_group_id:
    description: Security group ID.
    required: true
    type: str
extends_documentation_fragment:
- amazon.aws.aws
'''

EXAMPLES = '''
# Note: These examples do not set authentication details, see the AWS Guide for details.
- name: Remove all inbound rules are configured to allow access on ports different than TCP port 443 (HTTPS)
  remove_non_tcp_443_sg_rules:
    security_group_id: sg-abcde12345
'''

RETURN = '''
security_group_rules:
    description: List of removed security group rule IDs
    returned: always
    type: list
    sample:
    - sgr-abcdef12
    - sgr-345678ab
    - sgr-cdef1234
'''

try:
    from botocore.exceptions import ClientError, BotoCoreError
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry

def filter_non_tcp_443_sg_rules(ec2_client, module):

    security_group_id = module.params.get("security_group_id")

    rules = ec2_client.describe_security_group_rules(
        Filters = [
            {
                "Name": "group-id",
                "Values": [security_group_id]
            }
        ]
    )['SecurityGroupRules']
    filtered = []
    for rule in rules:
        if not rule["IsEgress"]:
            is_ingress_tcp_443 = rule["IpProtocol"] == "tcp" and rule["FromPort"] == 443 and rule["ToPort"] == 443
            if not is_ingress_tcp_443:
                filtered.append(rule["SecurityGroupRuleId"])
    return filtered

def remove_non_tcp_443_ingress_sg_rules(module):
    ec2_client = module.client('ec2', retry_decorator=AWSRetry.jittered_backoff())
    ec2_resource = module.resource('ec2')

    security_group_id = module.params.get("security_group_id")

    try:
        non_tcp_443_rules = filter_non_tcp_443_sg_rules(ec2_client, module)
        if len(non_tcp_443_rules) > 0:
            module.warn(f"Revoking security group rules: {non_tcp_443_rules}")
            security_group = ec2_resource.SecurityGroup(security_group_id)
            security_group.revoke_ingress(
                SecurityGroupRuleIds = non_tcp_443_rules
            )
    except (ClientError, BotoCoreError) as err:
        module.fail_json_aws(err, msg="error revoking rules")
    module.exit_json(security_group_rules=non_tcp_443_rules)


def main():
    argument_spec = dict(
      security_group_id=dict(required=True)
    )

    module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True)

    remove_non_tcp_443_ingress_sg_rules(module)


if __name__ == '__main__':
    main()