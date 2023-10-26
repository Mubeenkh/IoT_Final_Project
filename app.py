# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc
import dash_daq as daq
# import dash_bootstrap_components as dbc

# SMTP client session object that can be used to send mail to any internet machine with an SMTP
import smtplib
import imaplib
import email

import time
from time import sleep

import secrets
import string

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itertools import chain

subject = ""
body = ""
sender = "python01100922@gmail.com"
password = "txlzudjyidtoxtyj"
# recipients = "leonellalevymartel@gmail.com"
recipients = "extramuffin0922@gmail.com"
# recipients = "damianovisa@gmail.com"

token_length = 16

# Light images
img_light_off = 'assets/images/light_off.png'
img_light_on = 'assets/images/light_on.png'

# Fan images
fan_off = 'assets/images/fan.png'
fan_on = 'assets/images/fan.gif'

# -----------------------------------------------
# RPi components :
import Freenove_DHT as DHT
from LED import LED
import RPi.GPIO as GPIO

# Motor 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

EN1 = 22 
IN1 = 27
IN2 = 17
    
GPIO.setup(EN1,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)

# Instantiating the LED component
LED_PIN = 16
led = LED(LED_PIN,False)

# Instantiating the DHT11 component
DHT_PIN = 26 
dht = DHT.DHT(DHT_PIN)     
temperature_threshold = 24
fan_state = False

# Email 
email_count = 0


# Initialize the app
app = Dash(__name__)

# Phase 2 content
fan_content = [

    html.Div(id='therm-hum-display',children=[
        html.Div(className="card-component",children=[

            html.H3('Temperature (°C)'),
            daq.Thermometer(   

                id='therm-id',       
                showCurrentValue=True, 
                height=120,min=-10,max=40,
                value=0, 

            ),
        ]),
        html.Div(className="card-component", children=[
            
            html.H3('Humidity (%)'),
            daq.Gauge(

                id='humid-id',
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                showCurrentValue=True, 
                size=150,min=0,max=100,
                value=0

            ),
        ]),
        dcc.Interval(id='refresh', interval=2*1000,n_intervals=0)
    ]),
    html.Div(id='fan-display',children=[

        html.Div(className="card-component",children=[
            html.H3('DC Motor Fan'),
            html.Div(children=[
                html.Img( src='assets/images/fan.png', id='fan-img', className="feature-img" ),
            ]),
        ])

    ]),

]

# Phase 1 content
light_content =[
        
    html.Div(className="card-component", children=[

        html.H3('LED'),
        html.Div([
            html.Img( src=img_light_off, id='light-img', className="feature-img" )
        ]),
        html.Br(),
        daq.BooleanSwitch( on=False, id='light-switch', className='dark-theme-control' ),
    ])
        
]

# App layout
app.layout = html.Div( id='layout',
    children=[
        
        html.H1(style={},children=['IoT Project']),
        html.Div(id='container', children=[
            
            html.Div(id='column', children=[

                html.Div(id='left-container',children=fan_content),
                html.Div(id="right-container", children=[
                    html.Div(id='light-container', children=light_content),
                    # Phone scan thing for later on
                ])

            ])
        ]),

    ]
)

@app.callback(
    [Output('therm-id','value'),
     Output('humid-id','value')],
    # [Input('therm-id', 'value')],
    Input('refresh','n_intervals')

)
def update_temp(n_intervals):
    # print('-----------------------------------------')
    
    DHT11_data = getDHT11Data()
    temp = DHT11_data[0]
    humid = DHT11_data[1]
    # print('------------------------------------DHT11 info------------------------------------------')
    # print(f'{temp}°C')
    # print(f'{humid}%')
    return temp,humid
    # return 0 , 0

# Checking the value of the thermometer to see whether the application should send 
# the client an email or not. If they reply YES, then we turn on the fan, otherwise we leave it off
# This function will return the fan state (on or off)
@app.callback(
    Output('fan-img', 'src'),
    Input('therm-id', 'value'))
def fan_control(value):

    global fan_state
    global email_count
    
    print('------------------------------------Temp info------------------------------------------')
    # print(email_count)
    # print(fan_state)  
    print(f'{value}°C')  

    
    if(value > temperature_threshold ):

        if(fan_state == False):
            
            clientReply = False
            unique_token = ''

            if(email_count == 0):
                email_count = 1
                unique_token = generate_token(token_length)
                body =f'The current temperature is {value}°C. Would you like to turn on the fan?'
                send_email(subject, body, sender, recipients, password, unique_token)
                clientReply = readRecentEmailReply(unique_token, value) 
                sleep(5)
                print('send email')
                

            if(clientReply == True):

                fan_state = True
                print(f'email sent: {email_count}')
                print(f'fan on: {fan_state}') 
                print('reply said yes')

                GPIO.output(EN1,GPIO.HIGH)
                GPIO.output(IN1,GPIO.LOW)
                GPIO.output(IN2,GPIO.HIGH)

                return fan_on
            else:
                fan_state = False
                print(f'email sent: {email_count}')
                print(f'fan on: {fan_state}') 
                
                print('reply said no')
                GPIO.output(EN1,GPIO.LOW)
                GPIO.output(IN1,GPIO.LOW)
                GPIO.output(IN2,GPIO.LOW)

                return fan_off
        else:
            print(f'email sent: {email_count}')
            print(f'fan on: {fan_state}')  
            print('fan is already open')
            return fan_on
    else:
        email_count =0

    GPIO.output(EN1,GPIO.LOW)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)

    fan_state = False
    # print(f'email sent: {email_count}')
    # print(f'fan on: {fan_state}') 
    return fan_off
    


# callback to turn light on and off
@app.callback(
    Output('light-img', 'src'),
    Input('light-switch', 'on')
)
def update_button(on):

    # print(on)
    print('------------------------------------LED info------------------------------------------')
    if on == True:        
        led.setupLEDState(True)
        return img_light_on 
    
    else: 
        led.setupLEDState(False)
        return img_light_off
    

# GET the most RECENT email from recipients
def readRecentEmailReply(unique_token, value):

    
    # body =f'The current temperature is {value}. Would you like to turn on the fan?'
    # unique_token = generate_token(token_length);
    # send_email(subject, body, sender, recipients, password, unique_token)    
    

    while True:

        imap_ssl_host = 'imap.gmail.com'

        imap_ssl_port = 993
        imap = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
        imap.login(sender, password)
        # print(imap.login(sender, password)[0])
        imap.select("Inbox")
        _, msgnums = imap.search(None, f'FROM "{recipients}" UNSEEN') #to only check email of a specific person
        
        if msgnums[0]:

            msgnum = msgnums[0].split()[-1]

            _, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_string(data[0][1].decode("utf-8"))

            from_ = email.utils.parseaddr(message.get('From'))[1] #to only get the email address
            # to_ = message.get('To')
            # date_ = message.get('Date')
            subject_ = message.get('Subject')

            # Start of if statement
            if subject_ == f'Re: {unique_token}':

                print('#-----------------------------------------#')
                print(f"From: {from_}")  #to only get the email address
                # print(f"To: {to_}")
                # print(f"Date: {date_}")
                print(f"Subject: {subject_}")
                print("Content:")
                # print (f'{subject} {unique_token}')

                # Start of for loop
                for part in message.walk():

                        content_type = part.get_content_type()
                        content_disposition = str(part.get('Content-Disposition'))

                        if content_type == "text/plain" and 'attachment' not in content_disposition: 
                            msgbody = part.get_payload()

                            first_line = msgbody.split('\n', 1)[0]
                            print(first_line)

                            imap.close()
                            return checkYesResponse(first_line)
                            
                # end of for loop
            # end of if statement

            # else:
            print("Waiting...")
            # print(t)/
            imap.close()  
            # return False;

def checkYesResponse(first_line):
    if str(first_line).strip().lower() == "yes":
        print("Fan will turn ON")
        return True
    else:
        print("Fan will stay OFF.")
        return False
    
def generate_token(length):
    
    # combines all alphabet (uppercase and lowercase) with 0 to 9
    alphabet = string.ascii_letters + string.digits 
    # secrets.choice() Return a randomly chosen element from a non-empty sequence.
    token = ''.join(secrets.choice(alphabet) for i in range(length)) 
    return token

# def send_email(subject, body, sender, recipients, password, unique_token, temperature):
def send_email(subject, body, sender, recipients, password, unique_token):

    # TODO have to add the message here to add the temperature
    msg = MIMEMultipart()
    msg['Subject'] = f'{unique_token}'
    msg['From'] = sender
    msg['To'] = recipients
    # msg.attach(MIMEText(body, 'plain'))
    msg.attach(MIMEText(body))

    print("Connecting to server..")
    smtp_server =  smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # smtp_server =  imaplib.IMAP4_SSL("imap.gmail.com", 465)

    print("Logging in..")
    smtp_server.login(sender, password)
    print("Successfully Logged In!")

    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

    print('Email sent successfully.')
    print("Please respond in time")

def getDHT11Data():

    for i in range(0,15):
        chk = dht.readDHT11()	#read DHT11 and get a return value. Then determine whether
                                #data read is normal according to the return value
        if(chk is dht.DHTLIB_OK):	#read DHT11 and get a return value. Then determine
                                    #whether data read is normal according to the return value.
            # print("temp DHT11,OK!")
            break

    data=[]
    data.append(dht.temperature)
    data.append(dht.humidity)
    return data
   

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
    # monitor_temperature_and_send_email()