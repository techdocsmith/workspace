# write demo data to kinsis stream
# based on https://aws.amazon.com/blogs/big-data/snakes-in-the-stream-feeding-and-eating-amazon-kinesis-streams-with-python/
import boto3, json
import os, time

# See if the destination stream exists.
# If not, create it.
def get_stream():
    if stream not in kinesis.list_streams()["StreamNames"]:
        print("Stream not found, creating stream %s." %(stream))
        kinesis.create_stream(StreamName=stream, ShardCount=1)
        # Give it a minute
        time.sleep(60)
    
#def load_record(myrecord): 
    #kinesis.put_record(StreamName=stream, Data=myrecord, PartitionKey=partitionkey)

# Load the data from the sample file.
# Treat each line of the file as a record.

def load_records(samplefile):
    print("Starting to load data.")
    with open(samplefile, "r") as sampledata:
        for line in sampledata.readlines():
            print("Loading %s" %(line))
            samplerow = bytearray(line, "utf-8")
            kinesis.put_record(StreamName=stream, Data=samplerow, PartitionKey=partitionkey)
        # All done
        print("done")    

def main():
    # AWS profile configuration
    # Set this using command line for `docker run`.
    # os.environ['AWS_PROFILE'] = 'sfsmithcha'
    # os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'

    # Destination stream in Kenisis
    global stream
    stream = "wiki_tutorial-DOCKER"
    # Arbitrary partition key (this may need work)
    global partitionkey
    partitionkey = "partition_key"
    
    # Single sample record
    myrecord = """
    {"isRobot":true,"channel":"#sv.wikipedia","timestamp":"2016-06-27T00:00:11.080Z","flags":"NB","isUnpatrolled":false,"page":"Salo Toraut","diffUrl":"https://sv.wikipedia.org/w/index.php?oldid=36099284&rcid=89369918","added":31,"comment":"Botskapande Indonesien omdirigering","commentLength":35,"isNew":true,"isMinor":false,"delta":31,"isAnonymous":false,"user":"Lsjbot","deltaBucket":0.0,"deleted":0,"namespace":"Main"}
    """

    # Multi-record sample data set
    samplefile = ("./wikipedia-2016-06-27-sampled.json")
    
    # Open a Kinesis client
    global kinesis
    try:
        kinesis = boto3.client('kinesis')
    except:
        print("Unable to initialize Kenisis client. Quitting.")
        quit()
    
    # Get the Kinesis stream
    get_stream()
    print("Got a stream.")
    
    # Load records
    load_records(samplefile)
    
    

if __name__ == '__main__':
    main()
    