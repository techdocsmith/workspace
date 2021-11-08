import json, random
from confluent_kafka import Producer

from sseclient import SSEClient as EventSource


# Kafka running on 29092 in docker compose scenario
#producer = KafkaProducer(bootstrap_servers='localhost:29092')
p = Producer({'bootstrap.servers': 'localhost:29092'})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


url = 'https://stream.wikimedia.org/v2/stream/recentchange'

#environments for header example
environments = ['dev', 'prod', 'stage']

# Makes all the headers the same
# headers = {'myheader':'myvalue'}
for event in EventSource(url):
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
             # Trigger any available delivery report callbacks from previous produce() calls
            p.poll(0)
    
            # Randomly set the environment header
            headers = {'environment': random.choice(environments)}
            #String key example takes a CSV inputFormat
            #key = 'edit-stream'
            key = '{"key":"edit-stream"}'


             # Asynchronously produce a message, the delivery report callback
            # will be triggered from poll() above, or flush() below, when the message has
            # been successfully delivered or failed permanently.
            p.produce('wikistream-i', event.data.encode('utf-8'), callback=delivery_report,key=key, headers=headers)