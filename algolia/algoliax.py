# Explain the difference in the number of docs with different facet filters

from algoliasearch.search_client import SearchClient

myApp=''
myAPIkey=''
myIndex=''

client = SearchClient.create(myApp, myAPIkey)
index = client.init_index(myIndex)

query = ''
res = index.browse_objects({'query': query, 'attributesToRetrieve': [ 'url' ], 'facetFilters': ['version:4.0']})
total = 0
myHits = []
for hit in res:
    total = total + 1
    #print(hit)
    myHits.append(hit['url'][25:])
print(total)
#print(myHits)

resnew = index.browse_objects({'query': query, 'attributesToRetrieve': [ 'url' ], 'facetFilters': ['version:latest']})
for hit in resnew:
    try:
        myHits.remove(hit['url'][28:])
    except:
        print('not in 4.0 docs: %s' %(hit['url'][28:]))
        
for hit in myHits:
        print('not in latest %s' %(hit))