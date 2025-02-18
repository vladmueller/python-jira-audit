import json
import os
import requests
from dotenv import load_dotenv
from jira import JIRA
from requests.auth import HTTPBasicAuth

load_dotenv()
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

jira = JIRA(JIRA_BASE_URL, basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))


def fetch_project_keys(p_jira):
    return [project.key for project in p_jira.projects()]


project_keys = fetch_project_keys(jira)
print(project_keys)


def search():
    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))

    headers = {
        "Accept": "application/json"
    }

    query = {
        'jql': "project IN ('AI', 'BWM', 'BROOK', 'CPMCT', 'CMDEV', 'CSCP', 'CSCPDESK', 'GTMS', 'IBC', 'IS', 'IQR', 'IQROMS', 'JB', 'JIR', 'JT', 'LEAD', 'MK', 'MDP', 'MW', 'MW2', 'MOR', 'MWR2', 'REPMC', 'RCIM', 'SAL', 'TESTSE', 'SS', 'SA', 'SUP', 'SWSCRUM', 'VDR', 'VAC', 'AB', 'WM2', 'ZOR') AND labels IS NOT EMPTY",
        'maxResults': '800',
        'fields': 'labels',
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))



def extract_labels(response_json):
    labels_set = set()

    response_dict = json.loads(response_json)
    issues = response_dict.get("issues", [])

    for issue in issues:
        labels = issue.get("fields", {}).get("labels", [])
        labels_set.update(labels)

    return list(labels_set)


def extract_project_labels(response_json):
    project_labels = {}

    response_dict = json.loads(response_json)
    issues = response_dict.get("issues", [])

    for issue in issues:
        project_key = issue.get("key", "").split("-")[0]
        labels = issue.get("fields", {}).get("labels", [])

        if project_key:
            if project_labels.get(project_key) is None:
                project_labels[project_key] = set()
            project_labels[project_key].update(labels)

    return {key: list(value) for key, value in project_labels.items()}


labels_json = search()
labels_list = extract_labels(labels_json)
print(labels_list)

project_labels_dict = extract_project_labels(labels_json)
print(project_labels_dict)

