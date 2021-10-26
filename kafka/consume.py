from kafka import KafkaConsumer
#from prometheus_api_client import PrometheusConnect

#prom = PrometheusConnect(url ="http://localhost:9090", disable_ssl=True)

#for metric in prom.all_metrics():
#    print(metric)
#consumer = KafkaConsumer('prometheus')

#topic = 'wikipedia'
topic = 'wikistream'
#sasl_mechanism = "PLAIN"
#username = "admin"
#password = "12345"
#security_protocol = "SASL_PLAINTEXT"


consumer = KafkaConsumer (topic, bootstrap_servers=['localhost:29092'])#,
#                              api_version=(0, 10),
#                              security_protocol=security_protocol,
#                              sasl_mechanism = sasl_mechanism,
#                              sasl_plain_username = username,
#                              sasl_plain_password = password)
for msg in consumer:
    print (msg)