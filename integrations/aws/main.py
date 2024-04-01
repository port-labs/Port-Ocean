from typing import Any

import boto3
import json
from port_ocean.context.ocean import ocean
from loguru import logger


SUPPORTED_AWS_CLOUD_CONTROL_RESOURCES = [
    "AWS::Lambda::Function",
    "AWS::RDS::DBInstance",
    "AWS::S3::Bucket",
    "AWS::IAM::User",
    "AWS::ECS::Cluster",
    "AWS::ECS::Service",
    "AWS::Logs::LogGroup",
    "AWS::DynamoDB::Table",
    "AWS::SQS::Queue",
    "AWS::SNS::Topic",
    "AWS::Cognito::IdentityPool",
]
# Handles unserializable date properties in the JSON by turning them into a string
def _fix_unserializable_date_properties(obj: Any) -> Any:
    return json.loads(json.dumps(obj, default=str))

def _get_sessions() -> list[boto3.Session]:
    aws_access_key_id = ocean.integration_config.get("aws_access_key_id")
    aws_secret_access_key = ocean.integration_config.get("aws_secret_access_key")
    aws_regions = ocean.integration_config.get("aws_regions")

    aws_sessions = []
    for aws_region in aws_regions:
        aws_sessions.append(boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region))
    
    return aws_sessions

@ocean.on_resync()
async def resync_all(kind: str) -> list[dict[Any, Any]]:
    await resync_loadbalancer(kind)
    return []

@ocean.on_resync('loadBalancer')
async def resync_loadbalancer(kind: str) -> list[dict[Any, Any]]:
    sessions = _get_sessions()
    all_stacks = []
    next_token = None
    for session in sessions:
        region = session.region_name
        while True:
            try:
                elbv2 = session.client('elbv2')
                if next_token:
                    response = elbv2.describe_load_balancers(Marker=next_token)
                else:
                    response = elbv2.describe_load_balancers()
                next_token = response.get('NextMarker')
                for stack in response.get('LoadBalancers', []):
                    all_stacks.append(_fix_unserializable_date_properties(stack))
            except Exception as e:
                logger.error(f"Failed to list CloudFormation Stack in region: {region}; error {e}")
                break
            if not next_token:
                break

    return all_stacks

@ocean.on_resync('cloudFormation')
async def resync_cloudformation(kind: str) -> list[dict[Any, Any]]:
    sessions = _get_sessions()
    all_stacks = []
    next_token = None
    for session in sessions:
        region = session.region_name
        while True:
            try:
                cloudformation = session.client('cloudformation')
                if next_token:
                    response = cloudformation.list_stacks(NextToken=next_token)
                else:
                    response = cloudformation.list_stacks()
                next_token = response.get('NextToken')
                for stack in response.get('StackSummaries', []):
                    all_stacks.append(stack)
            except Exception as e:
                logger.error(f"Failed to list CloudFormation Stack in region: {region}; error {e}")
                break
            if not next_token:
                break

    return all_stacks

@ocean.on_resync('cloudResource')
async def resync_cloudcontrol(kind: str) -> list[dict[Any, Any]]:
    sessions = _get_sessions()
    all_instances = []
    next_token = None
    for session in sessions:
        region = session.region_name
        for resource_type in SUPPORTED_AWS_CLOUD_CONTROL_RESOURCES:
            while True:
                try:
                    cloudcontrol = session.client('cloudcontrol')
                    params = {
                        'TypeName': resource_type,
                    }
                    if next_token:
                        params['NextToken'] = next_token
                    
                    response = cloudcontrol.list_resources(**params)
                    next_token = response.get('NextToken')
                    for instance in response.get('ResourceDescriptions', []):
                        all_instances.append({
                            'Identifier': instance.get('Identifier', ''),
                            'Kind': resource_type,
                            **json.loads(instance.get('Properties', {}))
                        })
                except Exception as e:
                    logger.error(f"Failed to list CloudControl Instance in region: {region}; error {e}")
                    break
                if not next_token:
                    break
                
    return all_instances

@ocean.on_resync('ec2')
async def resync_ec2(kind: str) -> list[dict[Any, Any]]:
    sessions = _get_sessions()
    all_instances = []
    for session in sessions:
        region = session.region_name
        try:
            ec2 = session.resource('ec2')
            response = ec2.instances.all()
        except Exception as e:
            logger.error(f"Failed to list EC2 Instance in region: {region}; error {e}")
            break

        ec2_client = session.client('ec2')
        for instance in response:
            described_instance = ec2_client.describe_instances(InstanceIds=[instance.id])
            instance_definition = described_instance["Reservations"][0]["Instances"][0]
            seriliazable_instance = _fix_unserializable_date_properties(instance_definition)
            all_instances.append(seriliazable_instance)
        
    return all_instances

# Optional
# Listen to the start event of the integration. Called once when the integration starts.
@ocean.on_start()
async def on_start() -> None:
    # Something to do when the integration starts
    # For example create a client to query 3rd party services - GitHub, Jira, etc...
    print("Starting integration")
