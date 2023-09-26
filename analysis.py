import boto3
import pandas as pd
import matplotlib.pyplot as plt

# AWS credentials and region
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_KEY'
aws_region = 'us-east-1'

# EC2 instance ID
instance_id = 'YOUR_INSTANCE_ID'

# Initialize the CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Define the time range for data retrieval
end_time = pd.Timestamp.now()
start_time = end_time - pd.Timedelta(days=7)  # Adjust the time window as needed

# Function to retrieve CloudWatch metrics
def get_cloudwatch_metrics(metric_name):
    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': metric_name,
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 3600,  # 1 hour interval
                    'Stat': 'Average',  # You can change this to 'Sum', 'SampleCount', etc.
                },
                'ReturnData': True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    timestamps = response['MetricDataResults'][0]['Timestamps']
    values = response['MetricDataResults'][0]['Values']
    df = pd.DataFrame({'Timestamp': timestamps, metric_name: values})
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

# Get CPU, Memory, Disk I/O, and Network Traffic metrics
cpu_df = get_cloudwatch_metrics('CPUUtilization')
memory_df = get_cloudwatch_metrics('MemoryUtilization')
disk_io_df = get_cloudwatch_metrics('DiskReadBytes')
network_traffic_df = get_cloudwatch_metrics('NetworkIn')

# Perform statistical analysis (you can customize this as needed)
cpu_stats = cpu_df.describe()
memory_stats = memory_df.describe()
disk_io_stats = disk_io_df.describe()
network_traffic_stats = network_traffic_df.describe()

# Plot the metrics (you can customize the plots)
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.plot(cpu_df['Timestamp'], cpu_df['CPUUtilization'], label='CPU Utilization')
plt.xlabel('Timestamp')
plt.ylabel('Percentage')
plt.legend()

plt.subplot(2, 2, 2)
plt.plot(memory_df['Timestamp'], memory_df['MemoryUtilization'], label='Memory Utilization')
plt.xlabel('Timestamp')
plt.ylabel('Percentage')
plt.legend()

plt.subplot(2, 2, 3)
plt.plot(disk_io_df['Timestamp'], disk_io_df['DiskReadBytes'], label='Disk Read Bytes')
plt.xlabel('Timestamp')
plt.ylabel('Bytes')
plt.legend()

plt.subplot(2, 2, 4)
plt.plot(network_traffic_df['Timestamp'], network_traffic_df['NetworkIn'], label='Network In')
plt.xlabel('Timestamp')
plt.ylabel('Bytes')
plt.legend()

plt.tight_layout()
plt.show()

# Print the statistical analysis results
print("CPU Statistics:")
print(cpu_stats)
print("\nMemory Statistics:")
print(memory_stats)
print("\nDisk I/O Statistics:")
print(disk_io_stats)
print("\nNetwork Traffic Statistics:")
print(network_traffic_stats)