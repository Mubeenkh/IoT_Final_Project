# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc
import dash_daq as daq

# SMTP client session object that can be used to send mail to any internet machine with an SMTP
import smtplib
import imaplib
import email

import time

import secrets
import string

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Light images
img_light_off = 'assets/images/light_off.png'
img_light_on = 'assets/images/light_on.png'

# Fan images
fan_off = 'assets/images/staticfan.png'
fan_on = 'assets/images/fan.png'

# -----------------------------------------------
# RPi components :
import Freenove_DHT as DHT
from LED import LED
from DCMotor import DCMotor
from IoTController import IoTController

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

lightIntensity = 0

# Email 
email_count = 0
clientReply = False
token_length = 16

subject = ""
body = ""
sender = "python01100922@gmail.com"
password = "txlzudjyidtoxtyj"
# recipients = "email@email.com"
# recipients = "damianovisa@gmail.com"
# userID = "123456"
# userName = "Johnny Sins"
# temp_threshold = 24
# hum_threshold = 70
# intensity_threshold = 400

user_info = None
recipients = ""
userID = ""
userName = ""
temp_threshold = 0
hum_threshold = 0
intensity_threshold = 0


# -------------------------------------------------
# Instantiating MQTT Client subscribe
broker = "192.168.0.157"
topic_sub1 = "ESP8266/Photoresister"
topic_sub2 = "ESP8266/RFID" 

photoresistor_controller = IoTController(broker, topic_sub1)
photoresistor_controller.start()

rfid_controller = IoTController(broker, topic_sub2)
rfid_controller.start()

# --------------------------------------------------------------------------

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div( id='layout',
    children=[
        
        html.Div(style={'text-align':'center'},children=[
            html.H1('IoT Dashboard'),
        ]),
        html.Div(className='container', children=[
            
            # left side of dashboard
            html.Div(className="column-left", children=[

                html.Div(style={'display':'grid', 'text-align':'left'},children=[

                    # Profile Picture
                    html.Div( style={'text-align':'center'},children=[
                        html.Img( src='assets/images/pfp.png', className="profile-img"),
                    ]),
                        
                    html.Div(style={'display':'grid', 'gap':'5px'},children=[

                        # User Information
                        html.Div(className='',children=[
                            html.Label(f'Username', style={}, id='user_name'),
                            html.Label(f'email@email.com', 
                                        style={
                                            'color':'rgb( 213 213 213)',
                                            'font-size':'12px'
                                        }, id='user_email'),
                        ], style={'display':'grid', 'text-align':'center'}),
                        
                        # Temperature Threshold
                        html.Div(className='profile-label',children=[
                            html.Div(children=[
                                html.Img( src='assets/images/tempThreshold.png',style={'height':'30px'}),
                                
                                html.Label(f'Temperature:', style={'margin-left':'5px'}),
                                html.Label('0°C', style={'margin-left':'5px'}, id='temp_threshold'),
                            ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                        ]),

                        # Humidity Threshold
                        html.Div(className='profile-label',children=[
                            html.Div(children=[
                                html.Img( src='assets/images/humidityThreshold.png',style={'height':'30px'}),
                                
                                html.Label(f'Humidity:', style={'margin-left':'5px'}),
                                html.Label('0%', style={'margin-left':'5px'}, id='hum_threshold'),
                            ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                            
                        ]),

                        # Light Intensity Threshold
                        html.Div(className='profile-label', children=[
                            html.Div(children=[
                                html.Img( src='assets/images/lightThreshold.png',style={'height':'30px'}),
                                
                                html.Label(f'Light Intensity:', style={'margin-left':'5px'}),
                                html.Label('0', style={'margin-left':'5px'}, id='intensity_threshold'),
                            ],style={'display':'flex', 'align-items':'center','margin-left':'10px',}),
                        ]),

                    ])
                ])
                    
            ]),

            # right side of dashboard
            html.Div(className='column-right', children=[

                # Top-Right of the dashboard
                html.Div(className='top-container',children=[

                    # Temperature Information
                    html.Div(className="card-component",children=[

                        html.H3('Temperature (°C)'),
                        daq.Thermometer(   

                            id='therm-id',       
                            showCurrentValue=True, 
                            height=120,min=-10,max=40,
                            value=0, 

                        ),
                    ]),

                    # Humidity Information
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

                    # Light Intensity Information
                    html.Div(className="card-component",children=[
                        
                        html.Div(style={},children=[
                            html.H3('Light Intensity',),
                        ]),
                        
                        html.Div(className="light-intensity-container",children=[
                            
                            html.Div(id="brightness", className="brightness",children=[]),
                        
                            daq.Slider(
                                id='light-intensity',
                                min=0,
                                max=1024,
                                value=0,
                                size=200,
                                handleLabel={"showCurrentValue": True,"label": "Intensity", "color":"#1b1e2b"},
                                labelPosition='bottom',
                                marks={'0': '0', '1024': '1024'},
                                targets={
                                    f'{intensity_threshold}': {
                                        "label": "Threshold",
                                        "color": "#1b1e2b"
                                    },
                                },

                            ),
                                
                        ]),
                    ]),

                    dcc.Interval(id='refresh', interval=3*1000,n_intervals=0)
                    
                ]),

                # Bottom-Right of the dashboard
                html.Div(className="bottom-container", children=[

                    # DC Motor Fan
                    html.Div(className="card-component", children=[

                        html.Div(style={'display':'grid', 'grid-template-columns':'auto auto auto', },children=[
                            html.H3('DC Motor Fan:'),
                        ]),
                       
                        html.Div(children=[
                            html.Img( src=fan_off, id='fan-img', className="fan-img" ),
                        ]),
                        
                    ]),

                    # LED 
                    html.Div(className="card-component", children=[

                        html.Div(style={'display':'grid', 'grid-template-columns':'auto auto auto', },children=[
                            html.H3('LED:'),
                            html.Div(style={ 'grid-column': '3', 'padding-top':'20px'},children=[   
                                daq.BooleanSwitch(
                                    disabled=True, 
                                    on=False, 
                                    id='light-switch', 
                                    className='dark-theme-control', 
                                    color='#707798'
                                ),
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
    [Output('user_email','children'),
    Output('user_name','children'),
    Output('temp_threshold','children'),
    Output('hum_threshold','children'),
    Output('intensity_threshold','children'),
    Output('light-intensity','targets')],
    Input('refresh','n_intervals')    
)
def update_user(n_intervals):
    global user_info
    global recipients
    global temp_threshold
    global intensity_threshold 

    user_info = rfid_controller.getRfid()

    if(user_info):
        userID = user_info['user_id']
        user_name = user_info['user_name']
        recipients = user_info['user_email']
        temp_threshold = user_info['temp_threshold']
        hum_threshold = user_info['hum_threshold']
        intensity_threshold = user_info['intensity_threshold']
        slider_threshold = {
            f'{intensity_threshold}': {
                "label": "Threshold",
                "color": "#1b1e2b",
            },
        }
        return recipients, user_name, f'{temp_threshold}°C', f'{hum_threshold}%', intensity_threshold, slider_threshold
    else:
        userID = 'User ID'
        user_name = 'Username'
        recipients = 'email@email.com'
        temp_threshold = 0
        hum_threshold = 0
        intensity_threshold = 0
        slider_threshold = {
            f'{intensity_threshold}': {
                "label": "Threshold",
                "color": "#1b1e2b",
            },
        }
        return recipients, user_name, f'{temp_threshold}°C', f'{hum_threshold}%', intensity_threshold, slider_threshold


@app.callback(
    [Output('light-intensity','value'),
     Output('brightness','style'),
     Output('light-intensity','color')],
    Input('refresh','n_intervals')
)
def update_light_intensity(n_intervals):
    
    global lightIntensity
    # print('------------------------------Light intensity------------------------------')
    lightIntensity = photoresistor_controller.getLightIntensity()

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
    global intensity_threshold 

    if (value < intensity_threshold and intensity_threshold != 0): 
        t = time.localtime()
        current_time = time.strftime("%H:%M",t) 

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
    global temp_threshold
    fan_img = fan_off
    fan_class = 'fan-img'
    # -------------------
    print('------------------------------------Temp info------------------------------------------')
    print(f' Temp: {value}°C')  
    print(f' Email Sent: {email_count}')
    print(f' Fan on: {fan_state}') 
    
    if(value > temp_threshold and temp_threshold != 0):

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
            # print(data[0][1])
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

    msg.attach(MIMEText(body))

    print("Connecting to server..")
    smtp_server =  smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()

    print('Email sent successfully.')

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