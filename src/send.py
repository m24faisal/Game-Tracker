import pika
import pickle
import dataFormat as df 

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='test_queue')

example = df.DataSnap(fps=3, time=1230, date="Sept 11, 2024", plyrName="PLACEHOLDER", plyrLocation=[12,20,13], plyrHealth=20, plyrInventory=[], 
                      plyrStatus=[], plyrHunger=4.3, plyrSat=0 )

print(example)

while True:
# Define the Python object to be sent
    
    inp = input("Enter data: ")
    if inp == "exit":
        break
    data = example
    data.plyrName = inp
# Serialize the object with pickle
    serialized_data = pickle.dumps(data)

# Publish the serialized data to the queue
    channel.basic_publish(exchange='',
                      routing_key='test_queue',
                      body=serialized_data)

    print(" [x] Sent serialized data")

# Close the connection
connection.close()
