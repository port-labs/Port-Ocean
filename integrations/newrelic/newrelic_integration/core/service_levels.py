from typing import Any, AsyncIterable, Tuple, Optional
import httpx
from port_ocean.context.ocean import ocean
from newrelic_integration.core.query_templates.service_levels import (
    LIST_SLOS_QUERY,
    GET_SLI_BY_NRQL_QUERY,
)
from newrelic_integration.core.utils import send_graph_api_request
from newrelic_integration.utils import (
    render_query,
)
from newrelic_integration.core.paging import send_paginated_graph_api_request

SLI_OBJECT = "__SLI"


class ServiceLevelsHandler:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http_client = http_client

    async def get_service_level_indicator_value(
        self, http_client: httpx.AsyncClient, nrql: str
    ) -> dict[Any, Any]:
        query = await render_query(
            GET_SLI_BY_NRQL_QUERY,
            nrql_query=nrql,
            account_id=ocean.integration_config.get("new_relic_account_id"),
        )
        response = await send_graph_api_request(
            http_client, query, request_type="get_service_level_indicator_value"
        )
        service_levels = (
            response.get("data", {})
            .get("actor", {})
            .get("account", {})
            .get("nrql", {})
            .get("results", [])
        )
        if service_levels:
            return service_levels[0]
        return {}

    async def process_service_level(
        self, service_level: dict[str, Any]
    ) -> dict[str, Any]:
        nrql = (
            service_level.get("serviceLevel", {})
            .get("indicators", [])[0]
            .get("resultQueries", {})
            .get("indicator", {})
            .get("nrql")
        )
        service_level[SLI_OBJECT] = await self.get_service_level_indicator_value(
            self.http_client, nrql
        )
        self._format_tags(service_level)
        return service_level

    async def list_service_levels(self) -> AsyncIterable[dict[str, Any]]:
        async for service_level in send_paginated_graph_api_request(
            self.http_client,
            LIST_SLOS_QUERY,
            request_type="list_service_levels",
            extract_data=self._extract_service_levels,
        ):
            yield service_level

    @staticmethod
    async def _extract_service_levels(
        response: dict[Any, Any]
    ) -> Tuple[Optional[str], list[dict[Any, Any]]]:
        """Extract service levels from the response. used by send_paginated_graph_api_request"""
        results = (
            response.get("data", {})
            .get("actor", {})
            .get("entitySearch", {})
            .get("results", {})
        )
        return results.get("nextCursor"), results.get("entities", [])

    @staticmethod
    def _format_tags(entity: dict[Any, Any]) -> dict[Any, Any]:
        entity["tags"] = {tag["key"]: tag["values"] for tag in entity.get("tags", [])}
        return entity
