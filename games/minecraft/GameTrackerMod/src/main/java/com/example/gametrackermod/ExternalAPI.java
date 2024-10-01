package com.example.gametrackermod;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import org.slf4j.Logger;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.HashMap;


public class ExternalAPI {
    private final Logger LOGGER;
    private final GameTrackerMod currentInstance;

    //rabbitmq connection variables
    private Channel channel = null;
    private Connection connection = null;
    private final String DEBUG_QUEUE_NAME = "debug_gametracker";
    private final String DATA_QUEUE_NAME = "data_gametracker";

    public ExternalAPI(GameTrackerMod currentInstance){
        this.LOGGER = currentInstance.LOGGER;
        this.currentInstance = currentInstance;

        LOGGER.info("Register RabbitMQ connection");
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        try {
            this.connection = factory.newConnection();
            LOGGER.info("Connection started: {}", connection.toString());
            this.channel = connection.createChannel();

            channel.queueDeclare(DEBUG_QUEUE_NAME, false, false, false, null);
            channel.queueDeclare(DATA_QUEUE_NAME, false, false, false, null);

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

    public String StringMapToJSON(HashMap<String, String> map){
        StringBuilder out = new StringBuilder("{");
        for(var entry : map.entrySet()){
            o
            out.append("\"") .append(entry.getKey()) .append("\"")
                    .append(" : ")
                    .append("\"") .append(entry.getValue()) .append("\"")
                    .append(",");
        }
        out.append("}");
        return out.toString();
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
        channel.basicPublish("", DEBUG_QUEUE_NAME, null, message.getBytes());
        System.out.println(" [x] Sent '" + message + "'");
        LOGGER.info("Sent: {}, Queue: {}", message, DEBUG_QUEUE_NAME);
    }

    public void sendData() throws IOException {
        if(channel == null){
            LOGGER.info("channel is null");
            throw new IOException("RabbitMQ Channel null");
        } else if(!channel.isOpen()){
            LOGGER.info("channel isn't open");
            throw new IOException("RabbitMQ Channel not open");
        }

        HashMap<String, String> dataToken = new HashMap<String, String>();
        dataToken.put("fps", "100");
        dataToken.put("time", LocalTime.now().toString());
        dataToken.put("date", LocalDate.now().toString());
        dataToken.put("plyrName", "playerName");
        dataToken.put("plyrLocation", "100");
        dataToken.put("plyrHealth", "100");
        dataToken.put("plyrInventory", "100");
        dataToken.put("plyrStatus", "100");
        dataToken.put("plyrHunger", "100");
        dataToken.put("plyrSat", "100");


        String out = StringMapToJSON(dataToken);


        //send RabbitMQ message
        channel.basicPublish("", DATA_QUEUE_NAME, null, out.getBytes());
        System.out.println(" [x] Sent '" + out + "'");
        LOGGER.info("Sent: {}, Queue: {}", out, DATA_QUEUE_NAME);
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
