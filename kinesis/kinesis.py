# write demo data to kinsis stream
# based on https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
import boto3, json
import os
os.environ['AWS_PROFILE'] ='sfsmithcha'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
stream = "wiki"
partitionkey = "123"
myrecord = """
{"isRobot":true,"channel":"#sv.wikipedia","timestamp":"2016-06-27T00:00:11.080Z","flags":"NB","isUnpatrolled":false,"page":"Salo Toraut","diffUrl":"https://sv.wikipedia.org/w/index.php?oldid=36099284&rcid=89369918","added":31,"comment":"Botskapande Indonesien omdirigering","commentLength":35,"isNew":true,"isMinor":false,"delta":31,"isAnonymous":false,"user":"Lsjbot","deltaBucket":0.0,"deleted":0,"namespace":"Main"}
"""
samplefile = ("./wikipedia-2016-06-27-sampled.json")
kinesis = boto3.client('kinesis')
if stream not in kinesis.list_streams()["StreamNames"]:
    print("Stream not found, creating stream %s." %(stream))
    kinesis.create_stream(StreamName=stream, ShardCount=10)
print(kinesis.list_streams()["StreamNames"])
#kinesis.put_record(StreamName=stream, Data=myrecord, PartitionKey=partitionkey)
with open(samplefile, "r") as sampledata:
    for line in sampledata.readlines():
        sampledata = bytearray(line, "utf-8")
        kinesis.put_record(StreamName=stream, Data=sampledata, PartitionKey=partitionkey)
    