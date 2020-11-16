import requests, json, os
from pprint import pprint

query_url = "https://api.github.com/repos/apache/druid/pulls"
params = {
    "state": "open",
    "labels": "Area - Documentation"
}
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params).json()
for result in r:
    label_url = "https://api.github.com/repos/apache/druid/issues/%s/labels"%(result["number"])
    l = requests.get(label_url).json()
    print("pr: %s, state: %s"%(result["number"], result["state"]))
    print(l)
