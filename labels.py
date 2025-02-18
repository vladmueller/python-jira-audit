import os
from dotenv import load_dotenv
from jira import JIRA

load_dotenv()
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

jira = JIRA(JIRA_BASE_URL, basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN")))


def fetch_project_keys(p_jira):
    return [project.key for project in p_jira.projects()]


project_keys = fetch_project_keys(jira)
print(project_keys)
