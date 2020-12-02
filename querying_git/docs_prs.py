import requests, json, os
from pprint import pprint
# Need to update this for GraphQL

query_url = "https://api.github.com/repos/apache/druid/pulls"
params = {
    "state": "open",
    "labels": "Area+-+Documentation"
}
token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}
r = requests.get(query_url, headers=headers, params=params).json()
resultlist = []
for result in r:
    resultlist.append(result["number"])
    
print (resultlist)
print()
print()
opendocs = ["10528", "10396", "10339"]
print (len(resultlist))
check = all(item in opendocs for item in resultlist)
if check == True:
    print("All there")
else: print ("Not all there")




#test with known docs prs
r = [{"number": "10528", "state":"open"}, {"number": "10396", "state":"open"},
    {"number": "10339", "state":"open"}]
for result in r:
    label_url = "https://api.github.com/repos/apache/druid/issues/%s/labels"%(result["number"])
    l = requests.get(label_url, headers=headers).json()
    
    for label in l:
        if label["name"]=="Area - Documentation":
            print("pr: %s, state: %s"%(result["number"], result["state"]))
            print()
            print("docs")

