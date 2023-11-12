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
#recipients = "extramuffin0922@gmail.com"
recipients = "damianovisa@gmail.com"

token_length = 16

# Light images
img_light_off = 'assets/images/light_off.png'
img_light_on = 'assets/images/light_on.png'

# Fan images
fan_off = 'assets/images/fan.png'
fan_on = 'assets/images/fan.gif'

#Intensity images
intensity_off = 'assets/images/sun_off.png'
intensity_on = 'assets/images/sun_on.png'

# -----------------------------------------------
# RPi components :
import Freenove_DHT as DHT
from LED import LED
from DCMotor import DCMotor
from Photoresistor import Photoresistor

resistor = Photoresistor()

# Instantiating the LED component
LED_PIN = 16
led = LED(LED_PIN,False)

# Instantiating the DHT11 component
DHT_PIN = 26 
dht = DHT.DHT(DHT_PIN)     
temperature_threshold = 24
intensity_threshold = 400
fan_state = False

#Instantiating the Motor component
EN1 = 22 
IN1 = 27
IN2 = 18
motor = DCMotor(EN1,IN1,IN2,fan_state)


# Email 
email_count = 0


# Initialize the app
app = Dash(__name__)

# Phase 2 content
fan_content = [

    # html.Div(id='therm-hum-display',children=[
    #     html.Div(className="card-component",children=[

    #         html.H3('Temperature (°C)'),
    #         daq.Thermometer(   

    #             id='therm-id',       
    #             showCurrentValue=True, 
    #             height=120,min=-10,max=40,
    #             value=0, 

    #         ),
    #     ]),
    #     html.Div(className="card-component", children=[
            
    #         html.H3('Humidity (%)'),
    #         daq.Gauge(

    #             id='humid-id',
    #             color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
    #             showCurrentValue=True, 
    #             size=150,min=0,max=100,
    #             value=0

    #         ),
    #     ]),
    #     dcc.Interval(id='refresh', interval=2*1000,n_intervals=0)
    # ]),
    # html.Div(id='fan-display',children=[

    #     html.Div(className="card-component",children=[
    #         html.H3('DC Motor Fan'),
    #         html.Div(children=[
    #             html.Img( src='assets/images/fan.png', id='fan-img', className="feature-img" ),
    #         ]),
    #     ])

    # ]),

]

# Phase 1 content
light_content =[
        
    # html.Div(className="card-component", children=[

    #     html.H3('LED'),
    #     html.Div([
    #         html.Img( src=img_light_off, id='light-img', className="feature-img" )
    #     ]),
    #     html.Br(),
    #     daq.BooleanSwitch( on=False, id='light-switch', className='dark-theme-control' ),
    # ])
        
]

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

                            html.Div(className='profile-label',children=[
                                html.Label('ID: '),
                            ]),
                            html.Div(className='profile-label',children=[
                                html.Label('Name: '),
                            ]),
                            html.Div(className='profile-label',children=[
                                html.Label('Temp:'),
                            ]),
                            html.Div(className='profile-label',children=[
                                html.Label('Humidity:'),
                            ]),
                            html.Div(className='profile-label', children=[
                               html.Label('Light Intensity:'),
                            ]),


                        ])
                    ])
                    
                # ]),
            ]),
            html.Div(className='column-right', children=[

                html.Div(className='left-container',children=[


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
                        
                        html.Div(className="light-intensity",children=[
                            html.Img( src=intensity_off, className="feature-img", id="intensity-img"),
                            # html.Img( src='assets/images/sun_on.png', className="feature-img"),
                            daq.Slider(
                                id='intensity-id',
                                min=0,
                                max=1024,
                                value=0,
                                size=200,
                                handleLabel={"showCurrentValue": True,"label": "Intensity", "color":"#1b1e2b"},
                                color="#a56dc7",
                                labelPosition='bottom',
                                marks={'0': '0', '1024': '1024'},
                                targets={
                                    intensity_threshold: {
                                        # "showCurrentValue": "False",
                                        "label": "Threshold",
                                        "color": "#1b1e2b",
                                    },
                                },

                            ),
                                
                        ]),
                    ]),

                    dcc.Interval(id='refresh', interval=2*1000,n_intervals=0)
                    
                ]),
                html.Div(className="right-container", children=[

                    html.Div(className="card-component", children=[

                        html.Div(style={'display':'grid', 'grid-template-columns':'auto auto auto', },children=[
                            html.H3('LED:'),
                             #'justify-content': 'center','display': 'flex','align-items': 'center',
                            html.Div(style={ 'grid-column': '3', 'padding-top':'20px'},children=[   
                                # daq.PowerButton( on=False, id='light-switch', className='dark-theme-control', size=35 , color='#faff00'),
                                daq.BooleanSwitch( on=False, id='light-switch', className='dark-theme-control', color='#707798', disabled=True),
                            ])
                        ]),
                        html.Div([
                            html.Img( src=img_light_off, id='light-img',  className="feature-img" )
                        ]),
                        
                    ]),

                    html.Div(className="card-component", children=[

                        html.Div(style={'text-align':'left', 'padding-left':'40px'}, children=[
                            html.H3('DC Motor Fan:'),
                        ]),
                       
                        html.Div(children=[
                            html.Img( src='assets/images/fan.png', id='fan-img', className="feature-img" ),
                        ]),
                        
                    ])
                   
                ])

            ],)
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
    
@app.callback(
    Output('intensity-id','value'),
    Input('refresh','n_intervals')

)    
def update_intensity(n_intervals):
    intensity = resistor.getLightIntensity()
    light = intensity

    return light


# Checking the value of the thermometer to see whether the application should send 
# the client an email or not. If they reply YES, then we turn on the fan, otherwise we leave it off
# This function will return the fan state (on or off)
@app.callback(
    Output('fan-img', 'src'),
    Input('therm-id', 'value'))
def fan_control(value):

    global fan_state
    global email_count
    # -------------------
    print('------------------------------------Temp info------------------------------------------')
    # print(email_count)
    # print(fan_state)  
    print(f' Temp: {value}°C')
    print(f' Email Sent: {email_count}')
    print(f' Fan on: {fan_state}') 
    
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
                # print(f'email sent: {email_count}')
                # print(f'fan on: {fan_state}') 
                print('System: Client reply was yes')

                motor.control_fan(fan_state)

                return fan_on
            else:
                fan_state = False
                # print(f'email sent: {email_count}')
                # print(f'fan on: {fan_state}') 
                
                print('Syatem: Waiting for reply/Client reply was no')
                motor.control_fan(fan_state)

                return fan_off
        else:
            # print(f'email sent: {email_count}')
            # print(f'fan on: {fan_state}')  
            print('System: Fan is already on')
            return fan_on
    else:
        email_count =0

        fan_state = False
        motor.control_fan(fan_state)
        # print(f'email sent: {email_count}')
        # print(f'fan on: {fan_state}') 
        return fan_off
    


# callback to turn light on and off
@app.callback(
    [Output('light-img', 'src'),
    Output('intensity-img', 'src'),
    Output('light-switch','on')],
    Input('intensity-id', 'value')
)
def update_button(value):

    # print('------------------------------------LED info------------------------------------------')
    if value < intensity_threshold:        
        led.setupLEDState(True)
        return img_light_on, intensity_on, True
    
    else: 
        led.setupLEDState(False)
        return img_light_off, intensity_off, False


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
    #app.run(debug=True)
    