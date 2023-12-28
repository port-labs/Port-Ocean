from typing import Any, AsyncGenerator, Optional
from urllib.parse import urlparse
import httpx

from loguru import logger

from port_ocean.context.event import event
from port_ocean.utils import http_async_client


class JenkinsClient:
    def __init__(
        self, jenkins_base_url: str, jenkins_user: str, jenkins_token: str
    ) -> None:
        self.jenkins_base_url = jenkins_base_url
        self.client = http_async_client
        self.client.auth = httpx.BasicAuth(jenkins_user, jenkins_token)

    async def get_all_jobs_and_builds(
        self,
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        cache_key = "jenkins_jobs_and_builds"

        if cache := event.attributes.get(cache_key):
            logger.info("picking from cache")
            yield cache
            return

        all_jobs = []

        try:
            async for jobs in self.fetch_jobs_and_builds_from_api():
                all_jobs.extend(jobs)

            yield all_jobs
            event.attributes[cache_key] = all_jobs
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            raise

    async def fetch_jobs_and_builds_from_api(
        self, parent_job: Optional[dict[str, Any]] = None
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        page_size = 5
        page = 0
        job_batch = []

        while True:
            start_idx = page_size * page
            end_idx = start_idx + page_size

            params = {
                "tree": f"jobs[name,url,displayName,fullName,color,jobs[name,color,fullName,displayName,url],"
                f"builds[id,number,url,result,duration,timestamp,displayName,fullDisplayName]"
                f"{{0,50}}]{{{start_idx},{end_idx}}}"
            }

            if parent_job:
                job_path = urlparse(parent_job["url"]).path
                base_url = f"{self.jenkins_base_url}{urlparse(job_path).path}"
            else:
                base_url = self.jenkins_base_url

            job_response = await self.client.get(f"{base_url}/api/json", params=params)
            job_response.raise_for_status()
            jobs = job_response.json()["jobs"]

            if not jobs:
                break

            for job in jobs:
                if parent_job:
                    parent_job["__jobsCount"] = len(parent_job["jobs"])
                    job["__parentJob"] = {
                        key: value
                        for key, value in parent_job.items()
                        if parent_job and key != "jobs"
                    }

                if "builds" not in job:
                    # Recursively fetch child jobs only if no builds key
                    async for child_jobs in self.fetch_jobs_and_builds_from_api(job):
                        job_batch.extend(child_jobs)
                else:
                    job_batch.append(job)

            yield job_batch
            page += 1
            if len(jobs) < page_size:
                break

    async def get_single_resource(self, resource_url: str) -> dict[str, Any]:
        """
        Get either a job or build using the url from the event e.g.

        Job: job/JobName/
        Build: job/JobName/34/
        """
        response = await self.client.get(
            f"{self.jenkins_base_url}/{resource_url}api/json"
        )
        response.raise_for_status()
        return response.json()
