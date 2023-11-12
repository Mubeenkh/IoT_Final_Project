# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc
import dash_daq as daq
# from datetime import datetime
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




# Light images
img_light_off = 'assets/images/light_off.png'
img_light_on = 'assets/images/light_on.png'

# Fan images
# fan_off = 'assets/images/fan.png'
# fan_on = 'assets/images/fan.gif'
fan_off = 'assets/images/staticfan.png'
fan_on = 'assets/images/fan.png'

# -----------------------------------------------
# RPi components :
import Freenove_DHT as DHT
from LED import LED
from DCMotor import DCMotor
from Photoresistor import Photoresistor

# Instantiating the DHT11 component
DHT_PIN = 26 
dht = DHT.DHT(DHT_PIN)     
fan_state = False

#Instantiating the Motor component
EN1 = 22 
IN1 = 27
IN2 = 18
motor = DCMotor(EN1,IN1,IN2,fan_state)
motor_count = 0

# Instantiating the LED component
LED_PIN = 16
led = LED(LED_PIN,False)
LED_State = False
led_count = 0
LED_img = img_light_off

# Instantiating MQTT Client subscribe
# PR = Photoresistor()
resistor = Photoresistor()
lightIntensity = 0

# Email 
email_count = 0
clientReply = False
token_length = 16

subject = ""
body = ""
sender = "python01100922@gmail.com"
password = "txlzudjyidtoxtyj"
recipients = "extramuffin0922@gmail.com"
# recipients = "damianovisa@gmail.com"
userID = "123456"
userName = "Johnny Sins"
temperature_threshold = 24
humidity_threshold = 70
lightIntensity_threshold = 400


# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div( id='layout',
    children=[
        
        html.Div(style={'text-align':'center'},children=[
            html.H1('IoT Dashboard'),
        ]),
        html.Div(className='container', children=[
            
            html.Div(className="column-left", children=[
                # html.Div(className="card-component",children=[

                    html.Div(style={'display':'grid', 'text-align':'left'},children=[
                       html.Div( style={'text-align':'center'},children=[
                            html.Img( src='assets/images/user.png', className="profile-img" ),
                        ]),
                        
                        html.Div(style={'display':'grid', 'gap':'5px'},children=[

                            html.Div(className='',children=[
                                # html.Label(f'Name: {userName}'),
                                html.Label(f'{userName}', style={}),
                                html.Label(f'ID: {userID}', 
                                            style={
                                               'color':'rgb( 213 213 213)',
                                               'font-size':'15px'
                                            }),
                            ], style={'display':'grid', 'text-align':'center'}),

                            # html.Div(className='profile-label',children=[
                            #     html.Label(f'ID: {userID}'),
                            # ]),
                            
                            html.Div(className='profile-label',children=[
                                html.Div(children=[
                                    html.Img( src='assets/images/tempThreshold.png',style={'height':'30px'}),
                                    
                                    html.Label(f'Temperature: {temperature_threshold}°C', style={'margin-left':'5px'}),
                                ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                            ]),
                            html.Div(className='profile-label',children=[
                                html.Div(children=[
                                    html.Img( src='assets/images/humidityThreshold.png',style={'height':'30px'}),
                                    
                                    html.Label(f'Humidity: {humidity_threshold}%', style={'margin-left':'5px'}),
                                ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                                
                            ]),
                            html.Div(className='profile-label', children=[
                                html.Div(children=[
                                    html.Img( src='assets/images/lightThreshold.png',style={'height':'30px'}),
                                    
                                    html.Label(f'Light Intensity: {lightIntensity_threshold}', style={'margin-left':'5px'}),
                                ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                            ]),


                        ])
                    ])
                    
                # ]),
            ]),
            html.Div(className='column-right', children=[

                html.Div(className='top-container',children=[


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
                            value=0,

                        ),
                    ]),
                    html.Div(className="card-component",children=[
                        

                        html.Div(style={},children=[
                            html.H3('Light Intensity',),
                        ]),
                        
                        html.Div(className="light-intensity-container",children=[

                            
                            html.Div(id="brightness", className="brightness",children=[]),
                            # html.Img( src='assets/images/brightness.png', className="feature-img"),
                        
                            daq.Slider(
                                id='light-intensity',
                                min=0,
                                max=1024,
                                value=0,
                                size=200,
                                handleLabel={"showCurrentValue": True,"label": "Intensity", "color":"#1b1e2b"},
                                # color="#a56dc7",
                                # color="rgb(255, 255, 0)",
                                labelPosition='bottom',
                                marks={'0': '0', '1024': '1024'},
                                targets={
                                    f'{lightIntensity_threshold}': {
                                        "label": "Threshold",
                                        "color": "#1b1e2b",
                                        # "color": "rgb(255, 255, 0)",
                                    },
                                },

                            ),
                                
                        ]),
                    ]),

                    dcc.Interval(id='refresh', interval=3*1000,n_intervals=0)
                    
                ]),
                html.Div(className="bottom-container", children=[

                    html.Div(className="card-component", children=[

                        html.Div(style={'display':'grid', 'grid-template-columns':'auto auto auto', },children=[
                            html.H3('DC Motor Fan:'),
                            html.Div(style={ 'grid-column': '3', 'padding-top':'20px'},children=[   
                                # daq.PowerButton( on=False, id='light-switch', className='dark-theme-control', size=35 , color='#faff00'),
                                daq.BooleanSwitch( on=False, id='fan-switch', className='dark-theme-control', color='#707798'),
                            ])
                        ]),
                       
                        html.Div(children=[
                            html.Img( src=fan_off, id='fan-img', className="fan-img" ),
                        ]),
                        
                    ]),

                    html.Div(className="card-component", children=[

                        html.Div(style={'display':'grid', 'grid-template-columns':'auto auto auto', },children=[
                            html.H3('LED:'),
                             #'justify-content': 'center','display': 'flex','align-items': 'center',
                            html.Div(style={ 'grid-column': '3', 'padding-top':'20px'},children=[   
                                # daq.PowerButton( on=False, id='light-switch', className='dark-theme-control', size=35 , color='#faff00'),
                                daq.BooleanSwitch(disabled=True, on=False, id='light-switch', className='dark-theme-control', color='#707798'),
                            ])
                        ]),
                        html.Div([
                            html.Img( src=img_light_off, id='light-img',  className="feature-img" )
                        ]),
                        
                    ]),
                   
                ])

            ],)
        ]),

    ]
)

@app.callback(
    [Output('light-intensity','value'),
     Output('brightness','style'),
     Output('light-intensity','color')],
    Input('refresh','n_intervals')
)
def update_light_intensity(n_intervals):
    
    global lightIntensity

    # print('------------------------------Light intensity------------------------------')
    # print(PR.getLightIntensity())
    # lightIntensity = PR.getLightIntensity()
    lightIntensity = resistor.getLightIntensity()

    photo_to_rgb = (lightIntensity/1024) *255
    styleBrightness={'--intensity':f'{20+photo_to_rgb}', '--brightness-value':f'{photo_to_rgb}'}
    styleSlider = f'rgb({photo_to_rgb},{photo_to_rgb},0)'

    return lightIntensity, styleBrightness, styleSlider


@app.callback(
    [Output('light-img', 'src'),
    Output('light-switch', 'on')],
    Input('light-intensity','value')
)
def update_LED(value):

    # I made these counters so we dont call the same function multiple time
    global LED_State
    global led_count
    global LED_img

    # print(f'LED state: {LED_State}, LED count: {led_count}')
    
    if value < lightIntensity_threshold:   
        t = time.localtime()
        current_time = time.strftime("%H:%M",t) 
        # current_time = datetime.now()

        if(led_count == 0):
            body =f'The Light is ON at {current_time}'
            subject = "Low Room Light Intensity"
            send_email("sds", body, sender, recipients, password, subject)
            led.setupLEDState(True)

        led_count = 1
        LED_img = img_light_on
        LED_State = True
    else:
        if(led_count == 1):
            led.setupLEDState(False)
            
        led_count = 0
        LED_State = False
        LED_img = img_light_off
        
    return LED_img, LED_State


# ------------------------------------------------------


@app.callback(
    [Output('therm-id','value'),
     Output('humid-id','value')],
    Input('refresh','n_intervals')

)
def update_temp(n_intervals):

    DHT11_data = getDHT11Data()
    temp = DHT11_data[0]
    humid = DHT11_data[1]
    return temp,humid
    # return 0 , 0

# Checking the value of the thermometer to see whether the application should send 
# the client an email or not. If they reply YES, then we turn on the fan, otherwise we leave it off
# This function will return the fan state (on or off)
@app.callback(
    [Output('fan-img', 'src'),
    Output('fan-img', 'className'),],
    Input('therm-id', 'value'))
def fan_control(value):

    global fan_state
    global email_count
    global clientReply
    fan_img = fan_off
    fan_class = 'fan-img'
    # -------------------
    print('------------------------------------Temp info------------------------------------------')
    print(f' Temp: {value}°C')  
    print(f' Email Sent: {email_count}')
    print(f' Fan on: {fan_state}') 
    
    if(value > temperature_threshold ):

        if(fan_state == False):
            
            # clientReply = False
            unique_token = ''

            if(email_count == 0):
                email_count = 1
                unique_token = generate_token(token_length)
                body =f'The current temperature is {value}°C. Would you like to turn on the fan? Yes/No'
                send_email(subject, body, sender, recipients, password, unique_token)
                clientReply = readRecentEmailReply(unique_token, value) 

                fan_state = clientReply
                motor.control_fan(fan_state)   
                 
                if(fan_state == True):
                    print('====> System: Client reply was Yes')
                    fan_img = fan_on
                    fan_class = 'fan-spin-img'
                else:
                    print('====> System: Client reply was not Yes')
                    fan_img = fan_off
                    fan_class = 'fan-img'

            return fan_img, fan_class
        else:

            # print('====> System: Fan is already on')
            # return fan_on
            return fan_on, 'fan-spin-img'
    else:
        fan_state = False
        if(email_count == 1):
            motor.control_fan(fan_state)
            email_count =0

        # return fan_off
        return fan_img, fan_class
    

# GET the most RECENT email from recipients
def readRecentEmailReply(unique_token, value):

    t = 60

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
            subject_ = message.get('Subject')

            # Start of if statement
            if subject_ == f'Re: {unique_token}':

                print('#-----------------------------------------#')
                print(f"From: {from_}")  #to only get the email address
                print(f"Subject: {subject_}")
                print("Content:")

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
            print("Waiting...")
            imap.close()  
        # end of if statement
        time.sleep(1) 
        t -= 1

        if(t == 0):
            print('====> Session Expired')
            imap.close()
            return False

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
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

    print('Email sent successfully.')
    # print("Please respond in time")

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
    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)