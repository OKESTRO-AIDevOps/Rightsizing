import boto3
import subprocess
import yaml

# Define your AWS and EKS cluster details
aws_region = 'region'
eks_cluster_name = 'eks-cluster-name'
nodegroup_name = 'nodegroup-name'

subprocess.run(["kubectl", "apply", "-f", "https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml"])

hpa_yaml = """
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      targetAverageUtilization: 50
  - type: Resource
    resource:
      name: memory
      targetAverageUtilization: 50
"""

# Apply the HPA definition
with open("hpa.yaml", "w") as hpa_file:
    hpa_file.write(hpa_yaml)

subprocess.run(["kubectl", "apply", "-f", "hpa.yaml"])

eks = boto3.client('eks', region_name=aws_region)

# Define the labels for allowed instance types
node_labels = {
    "eks.amazonaws.com/capacityType": "m5.large,m5.xlarge",
}

# Update the nodegroup with labels
eks.update_nodegroup_config(
    clusterName=eks_cluster_name,
    nodegroupName=nodegroup_name,
    labels=node_labels
)