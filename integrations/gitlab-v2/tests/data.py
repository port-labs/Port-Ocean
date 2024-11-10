from choices import Entity


__GROUPS = [
  {
    "id": 1,
    "name": "Group 1",
    "path": "group-1",
    "description": "An interesting group",
    "visibility": "public",
    "share_with_group_lock": False,
    "require_two_factor_authentication": False,
    "two_factor_grace_period": 48,
    "project_creation_level": "developer",
    "auto_devops_enabled": None,
    "subgroup_creation_level": "owner",
    "emails_disabled": None,
    "emails_enabled": None,
    "mentions_disabled": None,
    "lfs_enabled": True,
    "default_branch": None,
    "default_branch_protection": 2,
    "default_branch_protection_defaults": {
      "allowed_to_push": [
          {
              "access_level": 40
          }
      ],
      "allow_force_push": False,
      "allowed_to_merge": [
          {
              "access_level": 40
          }
      ]
    },
    "avatar_url": "http://localhost:3000/uploads/group/avatar/1/foo.jpg",
    "web_url": "http://localhost:3000/groups/group-1",
    "request_access_enabled": False,
    "repository_storage": "default",
    "full_name": "Group 1",
    "full_path": "group-1",
    "file_template_project_id": 1,
    "parent_id": None,
    "created_at": "2020-01-15T12:36:29.590Z",
    "ip_restriction_ranges": None
  },
  {
    "id": 2,
    "name": "Group 2",
    "path": "group-2",
    "description": "An interesting group",
    "visibility": "public",
    "share_with_group_lock": False,
    "require_two_factor_authentication": False,
    "two_factor_grace_period": 48,
    "project_creation_level": "developer",
    "auto_devops_enabled": None,
    "subgroup_creation_level": "owner",
    "emails_disabled": None,
    "emails_enabled": None,
    "mentions_disabled": None,
    "lfs_enabled": True,
    "default_branch": None,
    "default_branch_protection": 2,
    "default_branch_protection_defaults": {
      "allowed_to_push": [
          {
              "access_level": 40
          }
      ],
      "allow_force_push": False,
      "allowed_to_merge": [
          {
              "access_level": 40
          }
      ]
    },
    "avatar_url": "http://localhost:3000/uploads/group/avatar/1/goo.jpg",
    "web_url": "http://localhost:3000/groups/group-2",
    "request_access_enabled": False,
    "repository_storage": "default",
    "full_name": "Group 2",
    "full_path": "group-2",
    "file_template_project_id": 1,
    "parent_id": None,
    "created_at": "2020-01-15T12:36:29.590Z",
    "ip_restriction_ranges": None
  },
]


__PROJECTS = [
  {
    "id": 1,
    "description": "Project 1",
    "description_html": "<p data-sourcepos=\"1:1-1:56\" dir=\"auto\">Project 1</p>",
    "name": "Project 1",
    "name_with_namespace": "Diaspora / Project 1",
    "path": "diaspora-client",
    "path_with_namespace": "diaspora/diaspora-client",
    "created_at": "2013-08-30T13:46:02Z",
    "updated_at": "2013-08-30T13:46:02Z",
    "default_branch": "main",
    "tag_list": [
      "example",
      "disapora client_1"
    ],
    "topics": [
      "example",
      "disapora client_1"
    ],
    "ssh_url_to_repo": "git@gitlab.example.com:diaspora/diaspora-client.git",
    "http_url_to_repo": "https://gitlab.example.com/diaspora/diaspora-client.git",
    "web_url": "https://gitlab.example.com/diaspora/diaspora-client",
    "readme_url": "https://gitlab.example.com/diaspora/diaspora-client/blob/main/README.md",
    "avatar_url": "https://gitlab.example.com/uploads/project/avatar/4/uploads/avatar.png",
    "forks_count": 0,
    "star_count": 0,
    "last_activity_at": "2022-06-24T17:11:26.841Z",
    "namespace": {
      "id": 1,
      "name": "Geoup 1",
      "path": "group-1",
      "kind": "group",
      "full_path": "diaspora",
      "parent_id": None,
      "avatar_url": "https://gitlab.example.com/uploads/project/avatar/6/uploads/avatar.png",
      "web_url": "https://gitlab.example.com/diaspora"
    },
    "container_registry_image_prefix": "registry.gitlab.example.com/diaspora/diaspora-client",
    "_links": {
      "self": "https://gitlab.example.com/api/v4/projects/4",
      "issues": "https://gitlab.example.com/api/v4/projects/4/issues",
      "merge_requests": "https://gitlab.example.com/api/v4/projects/4/merge_requests",
      "repo_branches": "https://gitlab.example.com/api/v4/projects/4/repository/branches",
      "labels": "https://gitlab.example.com/api/v4/projects/4/labels",
      "events": "https://gitlab.example.com/api/v4/projects/4/events",
      "members": "https://gitlab.example.com/api/v4/projects/4/members",
      "cluster_agents": "https://gitlab.example.com/api/v4/projects/4/cluster_agents"
    },
    "packages_enabled": True,
    "empty_repo": False,
    "archived": False,
    "visibility": "public",
    "resolve_outdated_diff_discussions": False,
    "container_expiration_policy": {
      "cadence": "1month",
      "enabled": True,
      "keep_n": 1,
      "older_than": "14d",
      "name_regex": "",
      "name_regex_keep": ".*-main",
      "next_run_at": "2022-06-25T17:11:26.865Z"
    },
    "issues_enabled": True,
    "merge_requests_enabled": True,
    "wiki_enabled": True,
    "jobs_enabled": True,
    "snippets_enabled": True,
    "container_registry_enabled": True,
    "service_desk_enabled": True,
    "can_create_merge_request_in": True,
    "issues_access_level": "enabled",
    "repository_access_level": "enabled",
    "merge_requests_access_level": "enabled",
    "forking_access_level": "enabled",
    "wiki_access_level": "enabled",
    "builds_access_level": "enabled",
    "snippets_access_level": "enabled",
    "pages_access_level": "enabled",
    "analytics_access_level": "enabled",
    "container_registry_access_level": "enabled",
    "security_and_compliance_access_level": "private",
    "emails_disabled": None,
    "emails_enabled": None,
    "shared_runners_enabled": True,
    "group_runners_enabled": True,
    "lfs_enabled": True,
    "creator_id": 1,
    "import_url": None,
    "import_type": None,
    "import_status": "none",
    "import_error": None,
    "open_issues_count": 0,
    "ci_default_git_depth": 20,
    "ci_forward_deployment_enabled": True,
    "ci_forward_deployment_rollback_allowed": True,
    "ci_allow_fork_pipelines_to_run_in_parent_project": True,
    "ci_job_token_scope_enabled": False,
    "ci_separated_caches": True,
    "ci_restrict_pipeline_cancellation_role": "developer",
    "ci_pipeline_variables_minimum_override_role": "maintainer",
    "ci_push_repository_for_job_token_allowed": False,
    "public_jobs": True,
    "build_timeout": 3600,
    "auto_cancel_pending_pipelines": "enabled",
    "ci_config_path": "",
    "shared_with_groups": [],
    "only_allow_merge_if_pipeline_succeeds": False,
    "allow_merge_on_skipped_pipeline": None,
    "allow_pipeline_trigger_approve_deployment": False,
    "restrict_user_defined_variables": False,
    "request_access_enabled": True,
    "only_allow_merge_if_all_discussions_are_resolved": False,
    "remove_source_branch_after_merge": True,
    "printing_merge_request_link_enabled": True,
    "merge_method": "merge",
    "squash_option": "default_off",
    "enforce_auth_checks_on_uploads": True,
    "suggestion_commit_message": None,
    "merge_commit_template": None,
    "squash_commit_template": None,
    "issue_branch_template": "gitlab/%{id}-%{title}",
    "auto_devops_enabled": False,
    "auto_devops_deploy_strategy": "continuous",
    "autoclose_referenced_issues": True,
    "keep_latest_artifact": True,
    "runner_token_expiration_interval": None,
    "external_authorization_classification_label": "",
    "requirements_enabled": False,
    "requirements_access_level": "enabled",
    "security_and_compliance_enabled": False,
    "compliance_frameworks": [],
    "warn_about_potentially_unwanted_characters": True,
    "permissions": {
      "project_access": None,
      "group_access": None
    }
  },
  {
    "id": 2,
    "description": "Project 2",
    "description_html": "<p data-sourcepos=\"1:1-1:56\" dir=\"auto\">Project 2</p>",
    "name": "Project 2",
    "name_with_namespace": "Diaspora / Project 2",
    "path": "diaspora-client",
    "path_with_namespace": "diaspora/diaspora-client",
    "created_at": "2013-09-30T13:46:02Z",
    "updated_at": "2013-09-30T13:46:02Z",
    "default_branch": "main",
    "tag_list": [
      "example",
      "disapora client"
    ],
    "topics": [
      "example",
      "disapora client"
    ],
    "ssh_url_to_repo": "git@gitlab.example.com:diaspora/diaspora-client.git",
    "http_url_to_repo": "https://gitlab.example.com/diaspora/diaspora-client.git",
    "web_url": "https://gitlab.example.com/diaspora/diaspora-client",
    "readme_url": "https://gitlab.example.com/diaspora/diaspora-client/blob/main/README.md",
    "avatar_url": "https://gitlab.example.com/uploads/project/avatar/4/uploads/avatar.png",
    "forks_count": 0,
    "star_count": 0,
    "last_activity_at": "2022-06-24T17:11:26.841Z",
    "namespace": {
      "id": 2,
      "name": "Group 2",
      "path": "group-2",
      "kind": "group",
      "full_path": "diaspora",
      "parent_id": None,
      "avatar_url": "https://gitlab.example.com/uploads/project/avatar/6/uploads/avatar.png",
      "web_url": "https://gitlab.example.com/diaspora"
    },
    "container_registry_image_prefix": "registry.gitlab.example.com/diaspora/diaspora-client",
    "_links": {
      "self": "https://gitlab.example.com/api/v4/projects/4",
      "issues": "https://gitlab.example.com/api/v4/projects/4/issues",
      "merge_requests": "https://gitlab.example.com/api/v4/projects/4/merge_requests",
      "repo_branches": "https://gitlab.example.com/api/v4/projects/4/repository/branches",
      "labels": "https://gitlab.example.com/api/v4/projects/4/labels",
      "events": "https://gitlab.example.com/api/v4/projects/4/events",
      "members": "https://gitlab.example.com/api/v4/projects/4/members",
      "cluster_agents": "https://gitlab.example.com/api/v4/projects/4/cluster_agents"
    },
    "packages_enabled": True,
    "empty_repo": False,
    "archived": False,
    "visibility": "public",
    "resolve_outdated_diff_discussions": False,
    "container_expiration_policy": {
      "cadence": "1month",
      "enabled": True,
      "keep_n": 1,
      "older_than": "14d",
      "name_regex": "",
      "name_regex_keep": ".*-main",
      "next_run_at": "2022-06-25T17:11:26.865Z"
    },
    "issues_enabled": True,
    "merge_requests_enabled": True,
    "wiki_enabled": True,
    "jobs_enabled": True,
    "snippets_enabled": True,
    "container_registry_enabled": True,
    "service_desk_enabled": True,
    "can_create_merge_request_in": True,
    "issues_access_level": "enabled",
    "repository_access_level": "enabled",
    "merge_requests_access_level": "enabled",
    "forking_access_level": "enabled",
    "wiki_access_level": "enabled",
    "builds_access_level": "enabled",
    "snippets_access_level": "enabled",
    "pages_access_level": "enabled",
    "analytics_access_level": "enabled",
    "container_registry_access_level": "enabled",
    "security_and_compliance_access_level": "private",
    "emails_disabled": None,
    "emails_enabled": None,
    "shared_runners_enabled": True,
    "group_runners_enabled": True,
    "lfs_enabled": True,
    "creator_id": 1,
    "import_url": None,
    "import_type": None,
    "import_status": "none",
    "import_error": None,
    "open_issues_count": 0,
    "ci_default_git_depth": 20,
    "ci_forward_deployment_enabled": True,
    "ci_forward_deployment_rollback_allowed": True,
    "ci_allow_fork_pipelines_to_run_in_parent_project": True,
    "ci_job_token_scope_enabled": False,
    "ci_separated_caches": True,
    "ci_restrict_pipeline_cancellation_role": "developer",
    "ci_pipeline_variables_minimum_override_role": "maintainer",
    "ci_push_repository_for_job_token_allowed": False,
    "public_jobs": True,
    "build_timeout": 3600,
    "auto_cancel_pending_pipelines": "enabled",
    "ci_config_path": "",
    "shared_with_groups": [],
    "only_allow_merge_if_pipeline_succeeds": False,
    "allow_merge_on_skipped_pipeline": None,
    "allow_pipeline_trigger_approve_deployment": False,
    "restrict_user_defined_variables": False,
    "request_access_enabled": True,
    "only_allow_merge_if_all_discussions_are_resolved": False,
    "remove_source_branch_after_merge": True,
    "printing_merge_request_link_enabled": True,
    "merge_method": "merge",
    "squash_option": "default_off",
    "enforce_auth_checks_on_uploads": True,
    "suggestion_commit_message": None,
    "merge_commit_template": None,
    "squash_commit_template": None,
    "issue_branch_template": "gitlab/%{id}-%{title}",
    "auto_devops_enabled": False,
    "auto_devops_deploy_strategy": "continuous",
    "autoclose_referenced_issues": True,
    "keep_latest_artifact": True,
    "runner_token_expiration_interval": None,
    "external_authorization_classification_label": "",
    "requirements_enabled": False,
    "requirements_access_level": "enabled",
    "security_and_compliance_enabled": False,
    "compliance_frameworks": [],
    "warn_about_potentially_unwanted_characters": True,
    "permissions": {
      "project_access": None,
      "group_access": None
    }
  },
]


__MERGE_REQUESTS = [
  {
    "id": 1,
    "iid": 1,
    "project_id": 1,
    "title": "test1",
    "description": "fixed login page css paddings",
    "state": "merged",
    "imported": False,
    "imported_from": "none",
    "merged_by": {
      "id": 87854,
      "name": "Douwe Maan",
      "username": "DouweM",
      "state": "active",
      "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
      "web_url": "https://gitlab.com/DouweM"
    },
    "merge_user": {
      "id": 87854,
      "name": "Douwe Maan",
      "username": "DouweM",
      "state": "active",
      "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
      "web_url": "https://gitlab.com/DouweM"
    },
    "merged_at": "2018-09-07T11:16:17.520Z",
    "merge_after": "2018-09-07T11:16:00.000Z",
    "prepared_at": "2018-09-04T11:16:17.520Z",
    "closed_by": None,
    "closed_at": None,
    "created_at": "2017-03-29T08:46:00Z",
    "updated_at": "2017-03-29T08:46:00Z",
    "target_branch": "main",
    "source_branch": "test1",
    "upvotes": 0,
    "downvotes": 0,
    "author": {
      "id": 1,
      "name": "Administrator",
      "username": "admin",
      "state": "active",
      "avatar_url": None,
      "web_url" : "https://gitlab.example.com/admin1"
    },
    "assignee": {
      "id": 1,
      "name": "Administrator",
      "username": "admin",
      "state": "active",
      "avatar_url": None,
      "web_url" : "https://gitlab.example.com/admin1"
    },
    "assignees": [{
      "name": "Miss Monserrate Beier",
      "username": "axel.block",
      "id": 12,
      "state": "active",
      "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
      "web_url": "https://gitlab.example.com/axel.block"
    }],
    "reviewers": [{
      "id": 2,
      "name": "Sam Bauch",
      "username": "kenyatta_oconnell",
      "state": "active",
      "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
      "web_url": "http://gitlab.example.com//kenyatta_oconnell"
    }],
    "source_project_id": 2,
    "target_project_id": 3,
    "labels": [
      "Community contribution",
      "Manage"
    ],
    "draft": False,
    "work_in_progress": False,
    "milestone": {
      "id": 1,
      "iid": 1,
      "project_id": 1,
      "title": "v2.0",
      "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
      "state": "closed",
      "created_at": "2015-02-02T19:49:26.013Z",
      "updated_at": "2015-02-02T19:49:26.013Z",
      "due_date": "2018-09-22",
      "start_date": "2018-08-08",
      "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1"
    },
    "merge_when_pipeline_succeeds": True,
    "merge_status": "can_be_merged",
    "detailed_merge_status": "not_open",
    "sha": "8888888888888888888888888888888888888888",
    "merge_commit_sha": None,
    "squash_commit_sha": None,
    "user_notes_count": 1,
    "discussion_locked": None,
    "should_remove_source_branch": True,
    "force_remove_source_branch": False,
    "allow_collaboration": False,
    "allow_maintainer_to_push": False,
    "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
    "references": {
      "short": "!1",
      "relative": "my-group/my-project!1",
      "full": "my-group/my-project!1"
    },
    "time_stats": {
      "time_estimate": 0,
      "total_time_spent": 0,
      "human_time_estimate": None,
      "human_total_time_spent": None
    },
    "squash": False,
    "task_completion_status":{
      "count":0,
      "completed_count":0
    }
  },
  {
    "id": 2,
    "iid": 2,
    "project_id": 2,
    "title": "test1",
    "description": "fixed login page css paddings",
    "state": "merged",
    "imported": False,
    "imported_from": "none",
    "merged_by": {
      "id": 87854,
      "name": "Douwe Maan",
      "username": "DouweM",
      "state": "active",
      "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
      "web_url": "https://gitlab.com/DouweM"
    },
    "merge_user": {
      "id": 87854,
      "name": "Douwe Maan",
      "username": "DouweM",
      "state": "active",
      "avatar_url": "https://gitlab.example.com/uploads/-/system/user/avatar/87854/avatar.png",
      "web_url": "https://gitlab.com/DouweM"
    },
    "merged_at": "2018-09-07T11:16:17.520Z",
    "merge_after": "2018-09-07T11:16:00.000Z",
    "prepared_at": "2018-09-04T11:16:17.520Z",
    "closed_by": None,
    "closed_at": None,
    "created_at": "2017-04-29T08:46:00Z",
    "updated_at": "2017-04-29T08:46:00Z",
    "target_branch": "main",
    "source_branch": "test1",
    "upvotes": 0,
    "downvotes": 0,
    "author": {
      "id": 1,
      "name": "Administrator",
      "username": "admin",
      "state": "active",
      "avatar_url": None,
      "web_url" : "https://gitlab.example.com/admin"
    },
    "assignee": {
      "id": 1,
      "name": "Administrator",
      "username": "admin",
      "state": "active",
      "avatar_url": None,
      "web_url" : "https://gitlab.example.com/admin"
    },
    "assignees": [{
      "name": "Miss Monserrate Beier",
      "username": "axel.block",
      "id": 12,
      "state": "active",
      "avatar_url": "http://www.gravatar.com/avatar/46f6f7dc858ada7be1853f7fb96e81da?s=80&d=identicon",
      "web_url": "https://gitlab.example.com/axel.block"
    }],
    "reviewers": [{
      "id": 2,
      "name": "Sam Bauch",
      "username": "kenyatta_oconnell",
      "state": "active",
      "avatar_url": "https://www.gravatar.com/avatar/956c92487c6f6f7616b536927e22c9a0?s=80&d=identicon",
      "web_url": "http://gitlab.example.com//kenyatta_oconnell"
    }],
    "source_project_id": 2,
    "target_project_id": 3,
    "labels": [
      "Community contribution",
      "Manage"
    ],
    "draft": False,
    "work_in_progress": False,
    "milestone": {
      "id": 2,
      "iid": 2,
      "project_id": 2,
      "title": "v2.0",
      "description": "Assumenda aut placeat expedita exercitationem labore sunt enim earum.",
      "state": "closed",
      "created_at": "2015-02-02T19:49:26.013Z",
      "updated_at": "2015-02-02T19:49:26.013Z",
      "due_date": "2018-09-22",
      "start_date": "2018-08-08",
      "web_url": "https://gitlab.example.com/my-group/my-project/milestones/1"
    },
    "merge_when_pipeline_succeeds": True,
    "merge_status": "can_be_merged",
    "detailed_merge_status": "not_open",
    "sha": "8888888888888888888888888888888888888888",
    "merge_commit_sha": None,
    "squash_commit_sha": None,
    "user_notes_count": 1,
    "discussion_locked": None,
    "should_remove_source_branch": True,
    "force_remove_source_branch": False,
    "allow_collaboration": False,
    "allow_maintainer_to_push": False,
    "web_url": "http://gitlab.example.com/my-group/my-project/merge_requests/1",
    "references": {
      "short": "!1",
      "relative": "my-group/my-project!1",
      "full": "my-group/my-project!1"
    },
    "time_stats": {
      "time_estimate": 0,
      "total_time_spent": 0,
      "human_time_estimate": None,
      "human_total_time_spent": None
    },
    "squash": False,
    "task_completion_status":{
      "count":0,
      "completed_count":0
    }
  }
]


__ISSUES = [
   {
      "state" : "opened",
      "description" : "Ratione dolores corrupti mollitia soluta quia.",
      "author" : {
         "state" : "active",
         "id" : 18,
         "web_url" : "https://gitlab.example.com/eileen.lowe",
         "name" : "Alexandra Bashirian",
         "avatar_url" : None,
         "username" : "eileen.lowe"
      },
      "milestone" : {
         "project_id" : 1,
         "description" : "Ducimus nam enim ex consequatur cumque ratione.",
         "state" : "closed",
         "due_date" : None,
         "iid" : 2,
         "created_at" : "2016-01-04T15:31:39.996Z",
         "title" : "v4.0",
         "id" : 17,
         "updated_at" : "2016-01-04T15:31:39.996Z"
      },
      "project_id" : 1,
      "assignees" : [{
         "state" : "active",
         "id" : 1,
         "name" : "Administrator",
         "web_url" : "https://gitlab.example.com/root",
         "avatar_url" : None,
         "username" : "root"
      }],
      "assignee" : {
         "state" : "active",
         "id" : 1,
         "name" : "Administrator",
         "web_url" : "https://gitlab.example.com/root",
         "avatar_url" : None,
         "username" : "root"
      },
      "type" : "ISSUE",
      "updated_at" : "2016-01-04T15:31:51.081Z",
      "closed_at" : None,
      "closed_by" : None,
      "id" : 1,
      "title" : "Consequatur vero maxime deserunt laboriosam est voluptas dolorem.",
      "created_at" : "2016-01-04T15:31:51.081Z",
      "moved_to_id" : None,
      "iid" : 6,
      "labels" : ["foo", "bar"],
      "upvotes": 4,
      "downvotes": 0,
      "merge_requests_count": 0,
      "user_notes_count": 1,
      "due_date": "2016-07-22",
      "imported":False,
      "imported_from": "none",
      "web_url": "http://gitlab.example.com/my-group/my-project/issues/6",
      "references": {
        "short": "#6",
        "relative": "my-group/my-project#6",
        "full": "my-group/my-project#6"
      },
      "time_stats": {
         "time_estimate": 0,
         "total_time_spent": 0,
         "human_time_estimate": None,
         "human_total_time_spent": None
      },
      "has_tasks": True,
      "task_status": "10 of 15 tasks completed",
      "confidential": False,
      "discussion_locked": False,
      "issue_type": "issue",
      "severity": "UNKNOWN",
      "_links":{
         "self":"http://gitlab.example.com/api/v4/projects/1/issues/76",
         "notes":"http://gitlab.example.com/api/v4/projects/1/issues/76/notes",
         "award_emoji":"http://gitlab.example.com/api/v4/projects/1/issues/76/award_emoji",
         "project":"http://gitlab.example.com/api/v4/projects/1",
         "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
      },
      "task_completion_status":{
         "count":0,
         "completed_count":0
      }
   },
   {
      "state" : "opened",
      "description" : "Ratione dolores corrupti mollitia soluta quia.",
      "author" : {
         "state" : "active",
         "id" : 18,
         "web_url" : "https://gitlab.example.com/eileen.lowe",
         "name" : "Alexandra Bashirian",
         "avatar_url" : None,
         "username" : "eileen.lowe"
      },
      "milestone" : {
         "project_id" : 1,
         "description" : "Ducimus nam enim ex consequatur cumque ratione.",
         "state" : "closed",
         "due_date" : None,
         "iid" : 2,
         "created_at" : "2016-01-04T15:31:39.996Z",
         "title" : "v4.0",
         "id" : 17,
         "updated_at" : "2016-01-04T15:31:39.996Z"
      },
      "project_id" : 2,
      "assignees" : [{
         "state" : "active",
         "id" : 1,
         "name" : "Administrator",
         "web_url" : "https://gitlab.example.com/root",
         "avatar_url" : None,
         "username" : "root"
      }],
      "assignee" : {
         "state" : "active",
         "id" : 1,
         "name" : "Administrator",
         "web_url" : "https://gitlab.example.com/root",
         "avatar_url" : None,
         "username" : "root"
      },
      "type" : "ISSUE",
      "updated_at" : "2016-01-04T15:31:51.081Z",
      "closed_at" : None,
      "closed_by" : None,
      "id" : 2,
      "title" : "Issue 2.",
      "created_at" : "2016-01-04T15:31:51.081Z",
      "moved_to_id" : None,
      "iid" : 2,
      "labels" : ["foo", "bar"],
      "upvotes": 4,
      "downvotes": 0,
      "merge_requests_count": 0,
      "user_notes_count": 1,
      "due_date": "2016-07-22",
      "imported":False,
      "imported_from": "none",
      "web_url": "http://gitlab.example.com/my-group/my-project/issues/6",
      "references": {
        "short": "#6",
        "relative": "my-group/my-project#6",
        "full": "my-group/my-project#6"
      },
      "time_stats": {
         "time_estimate": 0,
         "total_time_spent": 0,
         "human_time_estimate": None,
         "human_total_time_spent": None
      },
      "has_tasks": True,
      "task_status": "10 of 15 tasks completed",
      "confidential": False,
      "discussion_locked": False,
      "issue_type": "issue",
      "severity": "UNKNOWN",
      "_links":{
         "self":"http://gitlab.example.com/api/v4/projects/1/issues/76",
         "notes":"http://gitlab.example.com/api/v4/projects/1/issues/76/notes",
         "award_emoji":"http://gitlab.example.com/api/v4/projects/1/issues/76/award_emoji",
         "project":"http://gitlab.example.com/api/v4/projects/1",
         "closed_as_duplicate_of": "http://gitlab.example.com/api/v4/projects/1/issues/75"
      },
      "task_completion_status":{
         "count":0,
         "completed_count":0
      }
   }
]


DATA = {
    Entity.GROUP.value: __GROUPS,
    Entity.PROJECT.value: __PROJECTS,
    Entity.MERGE_REQUEST.value: __MERGE_REQUESTS,
    Entity.ISSUE.value: __ISSUES,
}
