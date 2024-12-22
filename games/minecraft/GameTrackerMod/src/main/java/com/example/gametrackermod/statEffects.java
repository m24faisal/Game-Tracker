package com.example.gametrackermod;

public class statEffects {
    public String effectName;
    public String effectType;
    public int strengthLevel;
    public int durationInSeconds;
    public int amplifierLevel;

    public statEffects(String effectName, String effectType, int strengthLevel, int amplifierLevel, int durationInSeconds){
        this.effectName = effectName;
        this.effectType = effectType;
        this.strengthLevel = strengthLevel;
        this.amplifierLevel = amplifierLevel;
        this.durationInSeconds = durationInSeconds;
    }

}
