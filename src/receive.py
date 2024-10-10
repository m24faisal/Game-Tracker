import pika
import pickle
import dataFormat as df
import json
import re


# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue (in case it doesn’t exist)
channel.queue_declare(queue='data_gametracker')

# Callback function to handle received messages
def callback(ch, method, properties, body):
    # Read data from the received message queue
    p = re.compile('(?<!\\\\)\'')
    try:
        print(f"Received data: {body}")
        data = p.sub('\"', data)
        data = json.loads(body)
        print(data)
    except Exception as e:
        print("Could not decipher properly")

# Set up the consumer to listen to the queue
channel.basic_consume(queue='data_gametracker',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
