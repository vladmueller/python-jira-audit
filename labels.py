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


def search():
    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    headers = {"Accept": "application/json"}

    all_issues = []
    next_page_token = None

    while True:
        query = {
            'jql': "project IN ('AI', 'BWM', 'BROOK', 'CPMCT', 'CMDEV', 'CSCP', 'CSCPDESK', 'GTMS', 'IBC', 'IS', 'IQR', 'IQROMS', 'JB', 'JIR', 'JT', 'LEAD', 'MK', 'MDP', 'MW', 'MW2', 'MOR', 'MWR2', 'REPMC', 'RCIM', 'SAL', 'TESTSE', 'SS', 'SA', 'SUP', 'SWSCRUM', 'VDR', 'VAC', 'AB', 'WM2', 'ZOR') AND labels IS NOT EMPTY",
            'maxResults': '800',
            'fields': 'labels',
        }

        if next_page_token:
            query['nextPageToken'] = next_page_token

        response = requests.get(url, headers=headers, params=query, auth=auth)
        data = response.json()

        all_issues.extend(data.get("issues", []))

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return json.dumps({"issues": all_issues}, sort_keys=True, indent=4, separators=(",", ": "))


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


def fetch_all_labels():
    url = f"{JIRA_BASE_URL}/rest/api/3/label"
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code == 200:
        return json.loads(response.text).get("values", [])
    else:
        return []
