package com.example.gametrackermod;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.slf4j.Logger;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.Arrays;


public class ExternalAPI {
    //rabbitmq connection variables
    private final String QUEUE_NAME = "examplequeue";
    private Channel channel = null;
    private Connection connection = null;

    private final Logger LOGGER;

    public ExternalAPI(Logger LOGGER){
        this.LOGGER = LOGGER;

        LOGGER.info("Register RabbitMQ connection");
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        try {
            this.connection = factory.newConnection();
            LOGGER.info("Connection started: {}", connection.toString());
            this.channel = connection.createChannel();
            channel.queueDeclare(QUEUE_NAME, false, false, false, null);

            // for debug purposes, can comment-out in release
            //    String message = "Minecraft GameTracker Startup...";
            //    channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
            //    System.out.println(" [x] Sent '" + message + "'");
            //    LOGGER.info(" [x] Sent '{}' ", message);
            // ^^ Can comment-out above in release
            sendMessage("Minecraft GameTracker Startup...");
            LOGGER.info(" [x] Sent startup message ");
        } catch (Exception e) {
            StringWriter sw = new StringWriter();
            PrintWriter pw = new PrintWriter(sw);
            e.printStackTrace(pw);
            System.err.println("RabbitMQ setup failure");
            LOGGER.info(" RabbitMQ setup failure {}", sw.toString());
        }
    }

    public void sendMessage(String message) throws IOException {
        if(channel == null){
            LOGGER.info("channel is null");
            throw new IOException("RabbitMQ Channel null");
        } else if(!channel.isOpen()){
            LOGGER.info("channel isn't open");
            throw new IOException("RabbitMQ Channel not open");
        }
        //send RabbitMQ message
        channel.basicPublish("", QUEUE_NAME, null, message.getBytes());
        System.out.println(" [x] Sent '" + message + "'");
        LOGGER.info("Sent: {}, Queue: {}", message, QUEUE_NAME);

    }

    public void shutdownAPI(){
        try{
            channel.close();
            connection.close();
        } catch(Exception e){
            System.err.println("Could not close rabbitmq connection");
            e.printStackTrace();
            LOGGER.info("Could not close RabbitMQ connection successfully, there may be memory leaks");
        }

    }
}
