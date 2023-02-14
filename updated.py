import boto3
import time

# set your AWS credentials
session = boto3.Session(
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    region_name='REGION_NAME'
)

# specify the SageMaker instance and duration to run (in minutes)
instance_name = 'INSTANCE_NAME'
duration_minutes = 60

# start the instance
sagemaker = session.client('sagemaker')
response = sagemaker.start_notebook_instance(
    NotebookInstanceName=instance_name
)

# wait for the specified duration
time.sleep(duration_minutes * 60)

# stop the instance
response = sagemaker.stop_notebook_instance(
    NotebookInstanceName=instance_name
)
