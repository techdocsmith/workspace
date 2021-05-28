# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client(project="plucky-agency-315021")

for bucket in storage_client.list_buckets():
    print(bucket)

mybucket = storage_client.get_bucket("my-wikipedia-tutorial")
print(mybucket.path)
myblobs = mybucket.list_blobs()
for blob in myblobs:
    print(blob.path)

