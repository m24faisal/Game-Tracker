package com.example.gametrackermod;

//import com.rabbitmq.client.Channel;
//import com.rabbitmq.client.Connection;
//import com.rabbitmq.client.ConnectionFactory;

import java.io.IOException;


public class ExternalAPI {
    //rabbitmq connection variables
    private final String QUEUE_NAME = "examplequeue";
    //public Channel channel = null;

    public ExternalAPI(){
        /*
        //register rabbitmq connection
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        try (Connection connection = factory.newConnection()) {
            this.channel = connection.createChannel();
            channel.queueDeclare(QUEUE_NAME, false, false, false, null);
            String message = "Hello World!";
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            System.out.println(" [x] Sent '" + message + "'");
        } catch (Exception e) {
            System.err.println("RabbitMQ setup failure");
        }
         */
    }

    public void sendMessage(String message) throws IOException {
        /*
        //send RabbitMQ message
        channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
        System.out.println(" [x] Sent '" + message + "'");
         */
    }
}
