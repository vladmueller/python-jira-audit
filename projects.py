import os

from dotenv import load_dotenv
from jira import JIRA

load_dotenv()
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
jira = JIRA(JIRA_BASE_URL, basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))


def fetch_project_keys():
    return [project.key for project in jira.projects()]


def build_projects_jql():
    project_keys = fetch_project_keys()
    jql_string = f"project IN ({', '.join(f'\'{key}\'' for key in project_keys)})"
    return jql_string
