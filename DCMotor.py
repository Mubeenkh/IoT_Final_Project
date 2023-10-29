import RPi.GPIO as GPIO


class DCMotor:

    EN1 = 0
    IN1 = 0
    IN2 = 0
    state = False
    
    def __init__(self,EN1,IN1,IN2,state):
        self.EN1 = EN1
        self.IN1 = IN1
        self.IN2 = IN2
        
        self.state = state

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(EN1,GPIO.OUT,initial=False)
        GPIO.setup(IN1,GPIO.OUT,initial=False)
        GPIO.setup(IN2,GPIO.OUT,initial=False)

    def control_fan(self,state):
        print(EN1)
        print(IN1)
        print(IN2)
        if(state == True):
            GPIO.output(EN1,GPIO.HIGH)
            GPIO.output(IN1,GPIO.LOW)
            GPIO.output(IN2,GPIO.HIGH)
        
        if(state == False):
            GPIO.output(EN1,GPIO.LOW)
            GPIO.output(IN1,GPIO.LOW)
            GPIO.output(IN2,GPIO.LOW)
        
        
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

