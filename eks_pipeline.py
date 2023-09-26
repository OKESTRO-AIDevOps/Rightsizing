import boto3

# AWS region and your account ID
region = 'your_region'
account_id = 'your_account_id'  # You can retrieve this from AWS Management Console

# EKS cluster details
cluster_name = 'cluster_name'
eks_role_name = 'eks_role_name'  # IAM role for EKS service

# Auto Scaling Group details
asg_name = 'your_asg_name'
launch_config_name = 'your_launch_config_name'
min_size = 1  # Minimum number of instances in the group
max_size = 3  # Maximum number of instances in the group
desired_capacity = 2  # Desired number of instances in the group

# IAM client for role creation and policy attachment
iam_client = boto3.client('iam', region_name=region)

# Create IAM role for Auto Scaling Group
try:
    iam_client.create_role(
        RoleName=asg_role_name,
        AssumeRolePolicyDocument='AssumeRolePolicyDocument'  # Replace with your policy document
    )
except iam_client.exceptions.EntityAlreadyExistsException:
    pass

# Attach policies to the Auto Scaling Group IAM role
asg_policies = ['asg_policies']  # Replace with the IAM policies you need

for policy in asg_policies:
    iam_client.attach_role_policy(
        RoleName=asg_role_name,
        PolicyArn=f'arn:aws:iam::aws:policy/{policy}'
    )

# EKS client for cluster creation
eks_client = boto3.client('eks', region_name=region)

# Create EKS cluster
eks_client.create_cluster(
    name=cluster_name,
    roleArn=f'arn:aws:iam::{account_id}:role/{eks_role_name}',
    version='1.28',
    resourcesVpcConfig={
        'subnetIds': ['subnetIds'],
        'securityGroupIds': ['securityGroupIds'],
    },
)

# Wait for EKS cluster to become active
eks_client.get_waiter('cluster_active').wait(
    name=cluster_name
)

# Autoscaling group client
asg_client = boto3.client('autoscaling', region_name=region)

# Create a launch configuration for Auto Scaling Group
asg_client.create_launch_configuration(
    LaunchConfigurationName=launch_config_name,
    ImageId='your_ami_id',
    InstanceType='t2.micro',  # Replace with your desired instance type
    KeyName='your_key_name',
    SecurityGroups=['your_security_group_id'],
    IamInstanceProfile='your_iam_instance_profile',  # IAM role for instances
    UserData='your_user_data_script'  # Optional user data script
)

# Create the Auto Scaling Group
asg_client.create_auto_scaling_group(
    AutoScalingGroupName=asg_name,
    LaunchConfigurationName=launch_config_name,
    MinSize=min_size,
    MaxSize=max_size,
    DesiredCapacity=desired_capacity,
    VPCZoneIdentifier='your_subnet_ids',  # Comma-separated subnet IDs
    Tags=[
        {
            'Key': 'Name',
            'Value': 'YourASGNameTag'
        },
        # Add more tags as needed
    ]
)

# Wait for Auto Scaling Group instances to launch and stabilize
asg_waiter = asg_client.get_waiter('group_in_service')
asg_waiter.wait(
    AutoScalingGroupName=asg_name,
    WaiterConfig={
        'Delay': 30,  # Adjust as needed
        'MaxAttempts': 60  # Adjust as needed
    }
)
