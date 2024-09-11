import pika
import pickle
import dataFormat as df

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same queue (in case it doesn’t exist)
channel.queue_declare(queue='test_queue')

# Callback function to handle received messages
def callback(ch, method, properties, body):
    # Deserialize the data
    data = pickle.loads(body)
    print(f" [x] Received deserialized data: {data}")

# Set up the consumer to listen to the queue
channel.basic_consume(queue='test_queue',
                      on_message_callback=callback,
                      auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
