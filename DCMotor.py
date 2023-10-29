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
        GPIO.setup(EN1,GPIO.OUT)
        GPIO.setup(IN1,GPIO.OUT)
        GPIO.setup(IN2,GPIO.OUT)

    def control_fan(self,state):
        
        
        if(state == True):
            print('-------------------Motor On-------------------')
            GPIO.output(self.EN1,GPIO.HIGH)
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
        else:
            print('-------------------Motor Off-------------------')
            GPIO.output(self.EN1,GPIO.LOW)
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.LOW)
        
        # print(f' Pin EN1: {self.EN1}')
        # print(f' Pin IN1: {self.IN1}')
        # print(f' Pin IN2: {self.IN2}')
        # print(f' Fan State: {state}')
