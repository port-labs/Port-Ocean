from gitlab import Gitlab

from gitlab_integration.events.event_handler import EventHandler
from gitlab_integration.events.hooks.issues import Issues
from gitlab_integration.events.hooks.jobs import Job
from gitlab_integration.events.hooks.merge_request import MergeRequest
from gitlab_integration.events.hooks.pipelines import Pipelines
from gitlab_integration.events.hooks.push import PushHook
from gitlab_integration.gitlab_service import GitlabService

event_handler = EventHandler()


def setup_listeners(gitlab_service: GitlabService, webhook_id: str | int) -> None:
    handlers = [
        PushHook(gitlab_service),
        MergeRequest(gitlab_service),
        Job(gitlab_service),
        Issues(gitlab_service),
        Pipelines(gitlab_service),
    ]
    for handler in handlers:
        event_ids = [f"{event_name}:{webhook_id}" for event_name in handler.events]
        event_handler.on(event_ids, handler.on_hook)


def setup_application(
    token_mapping: dict[str, list[str]], gitlab_host: str, app_host: str
) -> None:
    for token, group_mapping in token_mapping.items():
        gitlab_client = Gitlab(gitlab_host, token)
        gitlab_service = GitlabService(gitlab_client, app_host, group_mapping)
        webhook_ids = gitlab_service.create_webhooks()
        for webhook_id in webhook_ids:
            setup_listeners(gitlab_service, webhook_id)
