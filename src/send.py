import pika
import pickle

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='test_queue')

while True:
# Define the Python object to be sent
    
    inp = input("Enter data: ")
    if inp == "exit":
        break
    data = {'data' : inp}
# Serialize the object with pickle
    serialized_data = pickle.dumps(data)

# Publish the serialized data to the queue
    channel.basic_publish(exchange='',
                      routing_key='test_queue',
                      body=serialized_data)

    print(" [x] Sent serialized data")

# Close the connection
connection.close()
