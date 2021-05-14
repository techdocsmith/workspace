# Take a list of PR urls and check Jira for corresponding issue.
# config.json has a JSON object with a list of PRs
# Uses environmental variable for JIRA_TOKEN

import os, json, requests
from jira import JIRA
from github import Github

# CONFIG
# This should be your user id.
# TODO: Move to environment or config
USER = "charles.smith@imply.io"
JIRA_URL = "https://implydata.atlassian.net"

def init_jira():
    global j
    j = JIRA(JIRA_URL, basic_auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN')))

def main():
    with open ('config.json') as config_file:
        config_data = json.loads(config_file.read())
    prs = config_data['prs']
    release = config_data['release']
    init_jira()
    for pr in prs:
        results = j.search_issues(f'project=IMPLY and "pr"="{pr}"')
        if len(results):
            for jira_issue in results:
                print("%s : %s FV: %s LABELS: %s"%(jira_issue.key, pr, jira_issue.fields.fixVersions, jira_issue.fields.labels))
                fix_versions: List[Version] = jira_issue.fields.fixVersions
            else: print("No ticket found for %s"%(pr))


if __name__ == "__main__":
    main()
   