import boto3
import logging
import os

region = os.environ['region']
instance_id=os.environ['instance_id']

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def get_instance_state(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        return instance_state
    except Exception as e:
        print(f"Error getting instance state: {str(e)}")
        raise

def start_instance(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        ec2.start_instances(InstanceIds=[instance_id], DryRun=False)
        return "Instance started"
    except Exception as e:
        logger.error(f"Error starting instance: {str(e)}")
        raise

def stop_instance(instance_id, region):
    try:
        ec2 = boto3.client('ec2', region_name=region)
        ec2.stop_instances(InstanceIds=[instance_id], DryRun=False)
        return "Instance stopped"
    except Exception as e:
        logger.error(f"Error stopping instance: {str(e)}")
        raise

def lambda_handler(event, context):
    path = event['requestContext']['http']['path']
    if path == "/statue":
        try:
            instance_state = get_instance_state(instance_id, region)
            return instance_state
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }
        
    elif path == "/start":
        try:
            response = start_instance(instance_id, region)
            return response
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }

    elif path == "/stop":
        try:
            response = stop_instance(instance_id, region)
            return response
        except Exception as e:
            return {
                'statusCode': 500,
                'body': str(e)
            }
    else:
        return {
            'statusCode': 404,
            'body': "404 Not Found - Invalid URL"
        }
