package com.example.gametrackermod;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.item.ItemStack;
import net.minecraftforge.event.TickEvent;
import org.slf4j.Logger;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.*;

import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.client.Minecraft;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.core.Direction;

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
            //check if final element
            if(entry == map.entrySet().stream().toList().get(map.entrySet().size() - 1) ){
                out.append("\"") .append(entry.getKey()) .append("\"")
                        .append(" : ")
                        .append("\"") .append(entry.getValue()) .append("\"");
                break;
            }
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
    @SubscribeEvent
    public void sendData(PlayerEvent.PlayerLoggedInEvent event) throws IOException {
        if(channel == null){
            LOGGER.info("channel is null");
            throw new IOException("RabbitMQ Channel null");
        } else if(!channel.isOpen()){
            LOGGER.info("channel isn't open");
            throw new IOException("RabbitMQ Channel not open");
        }
        HashMap<String, String> dataToken = new HashMap<String, String>();
        ServerPlayer player = (ServerPlayer) event.getEntity();
        Minecraft minecraft = Minecraft.getInstance();
        int fps = minecraft.getFps();
        // 1. Main Inventory
        String mainInv = "";
        for(int i = 0; i < player.getInventory().items.size(); i++){
            ItemStack stack = player.getInventory().items.get(i);
            if (!stack.isEmpty()) {
                mainInv += ("Main Inventory " + i + ": " +
                        stack.getHoverName().getString() +
                        ", Count: " + stack.getCount()) + "; ";
            } else{
                mainInv += ("Main Inventory " + i + ": " +
                        "None, Count: 0" ) + "; ";
            }
        }
        // 2. Armor Inventory (0-3 slots)
        String armr = "";
        for (int i = 0; i < player.getInventory().armor.size(); i++) {
            ItemStack stack = player.getInventory().armor.get(i);

            if (!stack.isEmpty()) {
                armr += "Armor Slot " + i + ": " +
                        stack.getHoverName().getString() +
                        ", Count: " + stack.getCount() + "; ";
            } else{
                armr += ("Armor Slot " + i + ": " +
                        "None, Count: 0" ) + "; ";
            }
        }
        // 3. Offhand Inventory (usually 1 slot)
        String offHand = "";
        ItemStack offhandStack = player.getInventory().offhand.getFirst();
        if (!offhandStack.isEmpty()) {
            offHand += "Offhand: " +
                    offhandStack.getHoverName().getString() +
                    ", Count: " + offhandStack.getCount() + "; ";
            
        } else{
            offHand += ("Offhand: " +
                    "None, Count: 0" ) + "; ";
        }
        dataToken.put("fps", fps + "");
        dataToken.put("time", LocalTime.now().toString());
        dataToken.put("date", LocalDate.now().toString());
        dataToken.put("plyrName", player.getName().toString());
        dataToken.put("plyrLocation", String.valueOf(player.position()));
        dataToken.put("plyrHealth", String.valueOf(player.getHealth()));
        dataToken.put("plyrInventory", mainInv);
        dataToken.put("plyrArmor", armr);
        dataToken.put("plyrOffhand", offHand);
        // 4. Player Statistics Information
        Collection<MobEffectInstance> activeEffects = player.getActiveEffects();
        if (activeEffects.isEmpty()){
            dataToken.put("plyrStatus","None");
        } else{
            StringBuilder stat = new StringBuilder();
            for(MobEffectInstance  effectInstance: activeEffects){
                MobEffect effect = effectInstance.getEffect().value();
                String effectName = effect.getDisplayName().getString();
                String effectType = effect.getCategory().toString();
                int duration = effectInstance.getDuration();
                int amplifier = effectInstance.getAmplifier();
                //String effectStrength =  "Level: "+ (amplifier + 1);
                String effectDetails = " Type: " + effectType +
                        ", Duration: " + (duration / 20.0) + " seconds" +
                        ", Amplifier Level: " + amplifier; // IS strength

                stat.append(effectName).append(" --> ").append(effectDetails).append('; ');

            }

            dataToken.put("plyrStatus", stat.toString());
        }
        dataToken.put("plyrHunger", String.valueOf(player.getFoodData().getFoodLevel()));
        dataToken.put("plyrSat", String.valueOf(player.getFoodData().getSaturationLevel()));
        // 5. Player Viewing Direction Info
        float pitch = player.getXRot();
        float yaw = player.getYRot();
        double x = -Math.cos(Math.toRadians(yaw)) * Math.cos(Math.toRadians(pitch));
        double y = -Math.sin(Math.toRadians(pitch));
        double z = -Math.sin(Math.toRadians(yaw)) * Math.cos(Math.toRadians(pitch));
        double[] viewDirection = {x,y,z};
        dataToken.put("plyrView", Arrays.toString(viewDirection));
        // 6. Player Facing Direction Info (North, South, East, West)
        Direction direction = player.getDirection();
        dataToken.put("plyrFacing",String.valueOf(direction));


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
