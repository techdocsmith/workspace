from kafka import KafkaConsumer
import sys

# TODO make configs/args:
# bootstrap server (default 'localhost:9092')
# topic
# no. of messages to consume
# consume in 1 by 1 mode

#topic = 'wikipedia'
#topic = 'docs-demo'
topic = 'mini-demo'

print("initialize consumer")
consumer = KafkaConsumer (topic, bootstrap_servers=['localhost:29092'], auto_offset_reset='earliest',
     enable_auto_commit=True )
print("loop through messages")
for msg in consumer:
    print("got a message")
    print(msg.value)
    print()
    proceed = input("Type 'X' + Enter to exit. Enter to continue.").lower()
    if proceed == 'x':
        print("TTFN")
        sys.exit()

# SASL config
#sasl_mechanism = "PLAIN"
#username = "admin"
#password = "12345"
#security_protocol = "SASL_PLAINTEXT"
# #,
#                              api_version=(0, 10),
#                              security_protocol=security_protocol,
#                              sasl_mechanism = sasl_mechanism,
#                              sasl_plain_username = username,
#                              sasl_plain_password = password)