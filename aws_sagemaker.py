import boto3
import time

# Replace the values with your own
instance_type = 'ml.t2.medium'
instance_name = 'my-sagemaker-instance'
instance_lifetime_minutes = 60

# Create the SageMaker client
sagemaker = boto3.client('sagemaker')

# Start the instance
response = sagemaker.create_notebook_instance(
    InstanceType=instance_type,
    NotebookInstanceName=instance_name,
    LifecycleConfigName='my-lifecycle-config'
)

# Wait for the instance to start
status = None
while status != 'InService':
    instance_info = sagemaker.describe_notebook_instance(NotebookInstanceName=instance_name)
    status = instance_info['NotebookInstanceStatus']
    time.sleep(5)

print(f"Instance '{instance_name}' is up and running!")

# Wait for the defined lifetime period
time.sleep(instance_lifetime_minutes * 60)

# Stop the instance
sagemaker.stop_notebook_instance(NotebookInstanceName=instance_name)

print(f"Instance '{instance_name}' has been stopped.")
