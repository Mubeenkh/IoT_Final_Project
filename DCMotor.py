# import RPi.GPIO as GPIO


# class DCMotor:
	
#     LED_PIN = 0
#     state = False
    
#     def __init__(self,LED_PIN,state):
#         self.LED_PIN = LED_PIN
#         self.state = state

#         GPIO.setwarnings(False)
#         GPIO.setmode(GPIO.BOARD)
#         GPIO.setup(LED_PIN,GPIO.OUT,initial=state)

#     def control_fan(self,):
#         enable = 22 
#         input1 = 27
#         input2 = 18
        
#         GPIO.setup(enable,GPIO.OUT)
#         GPIO.setup(input1,GPIO.OUT)
#         GPIO.setup(input2,GPIO.OUT)
#         # print("dfd");
#         bool_disabled = n_clicks % 2
        
#         if bool_disabled:
#             reply = receiveRecentEmail()
#             if reply == True:
#                 n_clicks == 0
#                 GPIO.setmode(GPIO.BCM)
#                 GPIO.setwarnings(False)

#                 GPIO.output(enable,GPIO.HIGH)
#                 GPIO.output(input1,GPIO.LOW)
#                 GPIO.output(input2,GPIO.HIGH)
#                 return 'Fan is On', fan_on
#             else:
#                 n_clicks == 0
#                 return 'Fan is off', fan_off
#         else:
#             n_clicks == 0
#             return 'Fan is off', fan_off

