import boto3

region = 'region'

autoscaling_client = boto3.client('autoscaling', region_name=region)

launch_config_name = 'launch_config_name'
instance_type = 't2.micro'
ami_id = 'ami_id'

autoscaling_client.create_launch_configuration(
    LaunchConfigurationName=launch_config_name,
    ImageId=ami_id,
    InstanceType=instance_type,
)

autoscaling_group_name = 'autoscaling_group_name'
min_size = 2
max_size = 5
desired_capacity = 2

autoscaling_client.create_auto_scaling_group(
    AutoScalingGroupName=autoscaling_group_name,
    LaunchConfigurationName=launch_config_name,
    MinSize=min_size,
    MaxSize=max_size,
    DesiredCapacity=desired_capacity,
)

cpu_utilization_target = 70
scale_out_adjustment = 1
scale_in_adjustment = -1

autoscaling_client.put_scaling_policy(
    AutoScalingGroupName=autoscaling_group_name,
    PolicyName='scale-out-policy',
    PolicyType='TargetTrackingScaling',
    TargetTrackingConfiguration={
        'PredefinedMetricSpecification': {
            'PredefinedMetricType': 'ASGAverageCPUUtilization',
        },
        'TargetValue': cpu_utilization_target,
    },
    AdjustmentType='ChangeInCapacity',
    MinAdjustmentMagnitude=scale_out_adjustment,
)

scaling_policy_name = 'scale-out-policy'

autoscaling_client.attach_scaling_policy(
    AutoScalingGroupName=autoscaling_group_name,
    PolicyName=scaling_policy_name,
)