# Uses environmental variable for JIRA_TOKEN

import os, requests, json
from bs4 import BeautifulSoup
from jira import JIRA


# CONFIG





## Get page children 
root_page = '1970864252'
headers = {
   "Accept": "application/json"
}
expand = {
    "expand" : "descendants.page"
}
base_url = "https://implydata.atlassian.net"
children_url = "https://implydata.atlassian.net/wiki/rest/api/content/%s/child/page"%(root_page)
info_url = "https://implydata.atlassian.net/wiki/pages/viewinfo.action"
#print(children_url)
children =requests.get(children_url, auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN')),headers=headers, params=expand)
#for a confluence page, get the incoming pages
def print_incoming(page_id):
    payload = {'pageId' : page_id}
    resp = requests.get(info_url, auth=(os.getenv('JIRA_USER'), os.getenv('JIRA_TOKEN')), params=payload )
    mypage = BeautifulSoup(resp.text, 'lxml')
    try:
        for div in mypage.find_all('div'):
            if "class" in div.attrs.keys():
                if div.attrs["class"][0] == "basicPanelContainer":
                    if "Incoming Links" in div.text:
                        print("Incoming Links")
                        for descendant in div.descendants:
                            #print(descendant)
                            if descendant.name == "a":
                                #print("found an anchor")
                                if "data-linked-resource-id" in descendant.attrs.keys():
                                    print(base_url+descendant.attrs["href"])
    except:
        print("Broke looking for anchors")
    print("\n\n")



#print(children.status_code)
#print(json.dumps(json.loads(children.text), sort_keys=True, indent=4, separators=(",", ": ")))
def print_pages(result):
    print("Title: %s\n"%(result["title"]))
    #print("ID: %s"%(result["id"])
    print("URL: %s/wiki%s\n"%(base_url,result["_links"]["webui"]))
    print_incoming(result["id"])
    print('\n\n')
    if "descendants" in result.keys():
        for descendant in result["descendants"]["page"]["results"]:
            print_pages(descendant)



children_json = json.loads(children.text)
for result in children_json["results"]:
    print_pages(result)
  

## Grab a page in confluence and get info by page id

