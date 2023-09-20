import boto3

region = 'region'

eks_client = boto3.client('eks', region_name=region)

cluster_name = 'cluster_name'
eks_role_name = 'eks_role_name'  # IAM role for EKS service

iam_client = boto3.client('iam', region_name=region)

try:
    iam_client.create_role(
        RoleName=eks_role_name,
        AssumeRolePolicyDocument='AssumeRolePolicyDocument'
    )
except iam_client.exceptions.EntityAlreadyExistsException:
    pass

eks_policies = ['eks_policies']

for policy in eks_policies:
    iam_client.attach_role_policy(
        RoleName=eks_role_name,
        PolicyArn=f'arn:aws:iam::aws:policy/{policy}'
    )

eks_client.create_cluster(
    name=cluster_name,
    roleArn=f'arn:aws:iam::{YOUR_ACCOUNT_ID}:role/{eks_role_name}',
    version='1.28',
    resourcesVpcConfig={
        'subnetIds': ['subnetIds'],
        'securityGroupIds': ['securityGroupIds'],
    },
)

eks_client.get_waiter('cluster_active').wait(
    name=cluster_name
)

print(f'EKS cluster {cluster_name} created successfully!')