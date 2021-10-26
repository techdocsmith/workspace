from flask import Flask, request
import json
import snappy
from kafka import KafkaProducer
from google.protobuf.json_format import MessageToJson
from prometheus_client.parser import text_string_to_metric_families

producer = KafkaProducer(bootstrap_servers='localhost:9092')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/receive', methods=['POST'])
def processData():
    #data = MessageToJson(request.get_data())
    data = request.get_data()
    #uncompressed = snappy.decompress(data).decode('utf-8')
    #print(snappy.decompress(data))
    #print(data.decode('unicode_escape'))
    #for family in text_string_to_metric_families(uncompressed):
    #    for sample in family.samples:
    #       print("Name: {0} Labels: {1} Value: {2}".format(*sample))
            #msg = "Name: {0} Labels: {1} Value: {2}".format(*sample)
            #producer.send('prometheus', msg)
    protoData = request.get_data()
    #data = json.loads(protoData)
    
    #data = MessageToDict(protoData)
    producer.send('prometheus', protoData)
    return "OK"