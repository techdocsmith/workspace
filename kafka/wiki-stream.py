import json
from kafka import KafkaProducer
from sseclient import SSEClient as EventSource

# Kafka running on 29092 in docker compose scenario
producer = KafkaProducer(bootstrap_servers='localhost:29092')

url = 'https://stream.wikimedia.org/v2/stream/recentchange'
for event in EventSource(url):
    if event.event == 'message':
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            print('{user} edited {title}'.format(**change))
            #print(change)
            #producer.send('wikitopic', change)
            producer.send('wikistream', event.data.encode('utf-8'))
    