import json
from typing import Any, Literal
import typing

import aioboto3
from loguru import logger
from port_ocean.context.event import event
from utils.misc import (
    CustomProperties,
    ResourceKindsWithSpecialHandling,
)
from utils.aws import get_sessions

from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from utils.aws import _session_manager
from utils.overrides import AWSResourceConfig


def is_global_resource(kind: str) -> bool:
    global_services = [
        "cloudfront",
        "route53",
        "waf",
        "waf-regional",
        "iam",
        "organizations",
    ]
    try:
        service = kind.split("::")[1].lower()
        return service in global_services
    except IndexError:
        return False


def fix_unserializable_date_properties(obj: Any) -> Any:
    return json.loads(json.dumps(obj, default=str))


async def describe_single_resource(
    kind: str, identifier: str, account_id: str | None = None, region: str | None = None
) -> dict[str, str]:
    async for session in get_sessions(account_id, region):
        region = session.region_name
        match kind:
            case ResourceKindsWithSpecialHandling.ACM_CERTIFICATE:
                async with session.client("acm") as acm:
                    response = await acm.describe_certificate(CertificateArn=identifier)
                    resource = response.get("ResourceDescription")
                    return fix_unserializable_date_properties(resource)
            case ResourceKindsWithSpecialHandling.AMI_IMAGE:
                logger.warning(
                    f"Skipping AMI image {identifier} because it's not supported yet"
                )
                return {}
            case ResourceKindsWithSpecialHandling.CLOUDFORMATION_STACK:
                async with session.client("cloudformation") as cloudformation:
                    response = await cloudformation.describe_stacks(
                        StackName=identifier
                    )
                    stack = response.get("Stacks")[0]
                    return fix_unserializable_date_properties(stack)
            case _:
                async with session.client("cloudcontrol") as cloudcontrol:
                    response = await cloudcontrol.get_resource(
                        TypeName=kind, Identifier=identifier
                    )
                    resource_description = response.get("ResourceDescription")
                    serialized = resource_description.copy()
                    serialized.update(
                        {
                            "Properties": json.loads(
                                resource_description.get("Properties")
                            ),
                        }
                    )
                    return serialized
    return {}


async def batch_resources(
    kind: str,
    session: aioboto3.Session,
    service_name: Literal["acm", "elbv2", "cloudformation", "ec2"],
    describe_method: str,
    list_param: str,
    marker_param: str = "NextToken",
    describe_method_params: dict[str, Any] = {},
) -> ASYNC_GENERATOR_RESYNC_TYPE:
    """
    Batch resources from a service that supports pagination

    kind - the kind of resource
    session - the boto3 session to use
    service_name - the name of the service
    describe_method - the name of the method to describe the resource
    list_param - the name of the parameter that contains the list of resources
    marker_param - the name of the parameter that contains the next token
    describe_method_params - additional parameters for the describe method
    """
    region = session.region_name
    account_id = await _session_manager.find_account_id_by_session(session)
    next_token = None
    while True:
        async with session.client(service_name) as client:
            params: dict[str, Any] = describe_method_params
            if next_token:
                pointer_param = (
                    marker_param if marker_param == "NextToken" else "Marker"
                )
                params[pointer_param] = next_token
            response = await getattr(client, describe_method)(**params)
            next_token = response.get(marker_param)
            if results := response.get(list_param, []):
                yield [
                    {
                        CustomProperties.KIND: kind,
                        CustomProperties.ACCOUNT_ID: account_id,
                        CustomProperties.REGION: region,
                        **fix_unserializable_date_properties(resource),
                    }
                    for resource in results
                ]

        if not next_token:
            break


async def resync_cloudcontrol(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    is_global = is_global_resource(kind)
    use_get_resource_api = typing.cast(
        AWSResourceConfig, event.resource_config
    ).selector.use_get_resource_api
    async for session in get_sessions(None, None, is_global):
        region = session.region_name
        logger.info(f"Resyncing {kind} in region {region}")
        account_id = await _session_manager.find_account_id_by_session(session)
        next_token = None
        while True:
            async with session.client("cloudcontrol") as cloudcontrol:
                params = {
                    "TypeName": kind,
                }
                if next_token:
                    params["NextToken"] = next_token

                response = await cloudcontrol.list_resources(**params)
                next_token = response.get("NextToken")
                resources = response.get("ResourceDescriptions", [])
                if not resources:
                    break
                page_resources = []
                for instance in resources:
                    serialized = instance.copy()
                    if use_get_resource_api:
                        serialized = await describe_single_resource(
                            kind,
                            instance.get("Identifier"),
                            account_id=account_id,
                            region=region,
                        )
                    else:
                        serialized.update(
                            {
                                "Properties": json.loads(instance.get("Properties")),
                            }
                        )
                    serialized.update(
                        {
                            CustomProperties.KIND: kind,
                            CustomProperties.ACCOUNT_ID: account_id,
                            CustomProperties.REGION: region,
                        }
                    )
                    page_resources.append(
                        fix_unserializable_date_properties(serialized)
                    )
                yield page_resources

                if not next_token:
                    break
