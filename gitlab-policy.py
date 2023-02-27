import gitlab
import os
from dotenv import load_dotenv

load_dotenv()

gitlab_token = os.environ['GITLAB_TOKEN']
gitlab_uri = os.environ['GITLAB_URI']
gl = gitlab.Gitlab(gitlab_uri, gitlab_token)
gl.auth()

projects = gl.projects.list(all=True)

report = []
disabled = []
changed = []

for project_in_list in projects:

    if project_in_list.archived:
        continue

    state = project_in_list.container_expiration_policy['enabled']
    report.append(f"{project_in_list.path_with_namespace} : {state}")
    if True:
        disabled.append(f"{project_in_list.path_with_namespace} : {state}")
        response = gl.projects.update(project_in_list.id, {'container_expiration_policy_attributes': {
            "enabled": True,
            "cadence": "1d",
            "keep_n": 5,
            "older_than": "7d",
            "name_regex": ".*",
            "name_regex_keep": "^([0-9]+)\\.([0-9]+)\\.([0-9]+)(-[0-9]+)?$",
        }})
        changed.append(f"{response['id']} : {response['path_with_namespace']}")

reportCnt = len(report)
disabledCnt = len(disabled)
changedCnt = len(changed)

result = [
    f"There are {reportCnt} projects",
    f"Tried update {disabledCnt} projects",
    f"Updated {changedCnt} projects"
]

print(result)

