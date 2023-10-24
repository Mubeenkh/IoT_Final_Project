# Import packages
from dash import Dash, html, Input, Output, State, callback, dcc
import dash_daq as daq

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

# Instantiating the LED component
LED_PIN = 37
l = LED(LED_PIN,False)

# Instantiating the DHT11 component
DHT_PIN = 11    
dht = DHT.DHT(DHT_PIN)     
temperature_threshold = 23
fan_state = False

email_count = 0

# Initialize the app
app = Dash(__name__)

# Phase 2 content
fan_content = [

    html.Div(id='therm-hum-display',children=[
        html.Div(children=[
            daq.Thermometer(     
                id='therm-id',       
                showCurrentValue=True, label='Temperature (°C)',

                # TODO: change the value with current Temperature °C
                height=120,min=-10,max=40,units="°C",
                # value=0, 
                value=0, 
                # value=int(getTemperature()), 
            ),
        ]),
        html.Div(
            daq.Gauge(
                id='humid-id',
                color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
                showCurrentValue=True, label='Humidity (%)',

                # TODO: change the value with current Humidity %
                size=150,min=0,max=100,units="%",
                value=0
                # value=int(getHumidity())
            ),
        ),
        dcc.Interval(id='refresh', interval=3*1000,n_intervals=0)

    ]),
    html.Div(children=[

        html.Div(children=[
            html.Img( src='assets/images/fan.png', id='fan-img', className="feature-img" ),
        ]),
        daq.BooleanSwitch(
            on=False,
            disabled=True,
            label="Off",
            labelPosition="top",
            color="#9B51E0"
        )

    ]),

];

# Phase 1 content
light_content =[

        html.Div([
            html.Img( src=img_light_off, id='light-img', className="feature-img" )
        ]),
        daq.BooleanSwitch( on=False, id='light-switch', className='dark-theme-control' ),

        
];

# App layout
app.layout = html.Div( id='layout',style={},
    children=[
        html.H2(style={},children=['IoT Project']),
        html.Div(id='container', children=[
            
            html.Div(id='column', children=[

                html.Div(id='fan-container',children=fan_content),
                html.Div(id='light-container', children=light_content),

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
    # temp = getTemperature()
    # humid = getHumidity()
    DHT11_data = getDHT11Values()
    temp = DHT11_data[0]
    humid = DHT11_data[1]
    # print(DHT11_data[0])
    # print(DHT11_data[1])
    # print()
    return temp,humid

# 
@app.callback(
    Output('fan-img', 'src'),
    Input('therm-id', 'value'))
def fan_control(value):
    # temp = getTemperature()
    
    
    global fan_state
    global email_count
    
    print('------------------------------------Temp info------------------------------------------')
    # print(email_count)
    # print(fan_state)  
    print(f'{value}°C')  
    if(value > temperature_threshold ):

        if(fan_state == False):
            # THIS DOESN TWORK IT JSUT SPAMS EMAILS -----------------------------------------------------------------------
            clientReply = False
            unique_token = ''
            if(email_count == 0):
                email_count = 1
                unique_token = generate_token(token_length)
                body =f'The current temperature is {value}°C. Would you like to turn on the fan?'
                send_email(subject, body, sender, recipients, password, unique_token)
                clientReply = readRecentEmailReply(unique_token, value) 
                sleep(5)
                # print(clientReply)
                print('send email')
                
            # clientReply = readRecentEmailReply(unique_token) 
            # print(clientReply)
            
            # clientReply = checkYesResponse('NO')
            if(clientReply == True):

                fan_state = True
                print(f'email sent: {email_count}')
                print(f'fan on: {fan_state}') 
                print('reply said yes')
                # print('openning fan')
                return fan_on
            else:
                fan_state = False
                print(f'email sent: {email_count}')
                print(f'fan on: {fan_state}') 
                
                print('reply said no')
                return fan_off
        else:
            print(f'email sent: {email_count}')
            print(f'fan on: {fan_state}')  
            print('fan is already open')
            return fan_on
    else:
        email_count =0

    fan_state = False
    print(f'email sent: {email_count}')
    print(f'fan on: {fan_state}') 
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
        
        l.setupLEDState(True)

        return img_light_on 
    else: 

        l.setupLEDState(False)

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
                            print(first_line);

                            imap.close();
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
        return True;
    else:
        print("Fan will stay OFF.")
        return False;
    
def generate_token(length):
    
    # combines all alphabet (uppercase and lowercase) with 0 to 9
    alphabet = string.ascii_letters + string.digits 

    # secrets.choice() Return a randomly chosen element from a non-empty sequence.
    token = ''.join(secrets.choice(alphabet) for i in range(length)) 
    
    return token; 

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

def getDHT11Values():

    # dht = DHT.DHT(DHT_PIN)	#create a DHT class object
    #counts = 0	# Measurement counts, basically count for output
    # print('hello')
    # while(True):

    for i in range(0,15):
        chk = dht.readDHT11()	#read DHT11 and get a return value. Then determine whether
                                #data read is normal according to the return value
        if(chk is dht.DHTLIB_OK):	#read DHT11 and get a return value. Then determine
                                    #whether data read is normal according to the return value.
            # print("temp DHT11,OK!")
            break
        
    # tempValue = dht.temperature
    # print("temp: %.2f" %(dht.temperature))
    # return float(dht.temperature)
    data=[]
    data.append(dht.temperature)
    data.append(dht.humidity)
    return data

# def getHumidity():

#     # dht = DHT.DHT(DHT_PIN)	#create a DHT class object
#     #counts = 0	# Measurement counts, basically count for output
#     # print('humid')
#     # while(True):

#     for i in range(0,15):
#         chk = dht.readDHT11()	#read DHT11 and get a return value. Then determine whether
#                                 #data read is normal according to the return value
#         if(chk is dht.DHTLIB_OK):	#read DHT11 and get a return value. Then determine
#                                     #whether data read is normal according to the return value.
#             # print("humid HT11,OK!")
#             break
    
#     # tempValue = dht.temperature
#     # print("humid: %.2f" %(dht.humidity))
#     return float(dht.humidity)
    
# def getTemperature():

#     # dht = DHT.DHT(DHT_PIN)	#create a DHT class object
#     #counts = 0	# Measurement counts, basically count for output
#     # print('hello')
#     # while(True):

#     for i in range(0,15):
#         chk = dht.readDHT11()	#read DHT11 and get a return value. Then determine whether
#                                 #data read is normal according to the return value
#         if(chk is dht.DHTLIB_OK):	#read DHT11 and get a return value. Then determine
#                                     #whether data read is normal according to the return value.
#             # print("temp DHT11,OK!")
#             break
        
#     # tempValue = dht.temperature
#     # print("temp: %.2f" %(dht.temperature))
#     return float(dht.temperature)
   

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    # app.run(debug=True)
    # monitor_temperature_and_send_email()
