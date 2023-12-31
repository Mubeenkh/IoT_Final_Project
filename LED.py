#!/usr/bin/env python3
#############################################################################
# Filename    : LED.py
# Description :	LED for Raspberry
# Author      : Mubeen Khan
# modification: 2023/10/29
########################################################################
import RPi.GPIO as GPIO

class LED:
	
    LED_PIN = 0
    state = False
    
    def __init__(self,LED_PIN,state):
        self.LED_PIN = LED_PIN
        self.state = state

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN,GPIO.OUT,initial=state)

    def setupLEDState(self,state):
        
        if(state == True):
            print('-------------------light on-------------------')
            GPIO.output(self.LED_PIN,1)
        else:
            print('-------------------light off-------------------')
            GPIO.output(self.LED_PIN,0)

        # print(f' Fin LED: {self.LED_PIN}')
        # print(f' LED state: {state}')

