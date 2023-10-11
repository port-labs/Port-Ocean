from typing import Any, Optional
import httpx
from loguru import logger


class OpenCostClient:
    def __init__(self, app_host: str, window: str):
        self.app_host = app_host
        self.window = window
        self.http_client = httpx.AsyncClient(headers=self.api_auth_header)

    @property
    def api_auth_header(self) -> dict[str, Any]:
        return {"Content-Type": "application/json"}

    async def send_api_request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        try:
            response = await self.http_client.request(
                method=method,
                url=f"{self.app_host}/{endpoint}",
                params=query_params,
                json=json_data,
                headers=self.api_auth_header,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error with status code: {e.response.status_code} and response text: {e.response.text}"
            )
            raise

    async def get_cost_allocation(self) -> list[dict[str, Any]]:
        """Calls the OpenCost allocation endpoint to return data for cost and usage
        https://www.opencost.io/docs/integrations/api
        """
        endpoint = "allocation/compute"
        parameters: dict[str, Any] = {"window": self.window}
        return (
            await self.send_api_request(endpoint=endpoint, query_params=parameters)
        )["data"]
