# Import packages
# import RPi.GPIO as GPIO
from dash import Dash, html, Input, Output, State, callback, dcc
import dash_daq as daq
# -----------------------------------------------
import smtplib
import imaplib
import email

from time import sleep

# import Adafruit_DHT
import secrets
import string



from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itertools import chain



subject = "The current temperature is ***. Would you like to turn on the fan?"
body = ""

sender = "python01100922@gmail.com"
password = "txlzudjyidtoxtyj"

# recipients = "leonellalevymartel@gmail.com"
recipients = "extramuffin0922@gmail.com"
token_length = 16


# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# LED = 26
# DHT_PIN = 17          
# temperature_threshold = 24

# GPIO.setup(LED,GPIO.OUT,initial=0)
# GPIO.setup(DHT_PIN, GPIO.IN)


# Initialize the app
app = Dash(__name__)

# Light images and CSS 
img_light_off = 'assets/images/light_off.png'
style_img = {
    'height': '150px',
    'width':'150px',
}

img_light_on = 'assets/images/light_on.png'
style_img_light_on = {
    'height': '150px',
    'width':'150px',
    '-webkit-filter': 'drop-shadow(1px 1px 20px rgba(255, 255, 0, 1))',
    'filter': 'drop-shadow(1px 1px 20px rgba(255, 255, 0, 1))',
}


# Fan images and CSS
fan_off = 'assets/images/fan.png'
fan_on = 'assets/images/fan.gif'
style_img_fan = {
    'height': '150px',
    'width':'150px',
}


# App layout
app.layout = html.Div( id='layout',style={},
    children=[

        html.Div(id='container', children=[
            html.H2('IoT Project'),

            html.Div(id='column', children=[
                html.Div(id='feature-container', children=[
                    html.Div([
                        html.Img(
                            src=img_light_off,
                            className="feature-img",
                            id='light-img',
                            style={}
                        )
                    ]),
                    html.Div([
                        html.Button(
                            'Turn On', 
                            className="button-style", 
                            id='light-switch', 
                            n_clicks=0,
                            style={}
                        )
                    ])
                        
                ]),

                html.Div(id='feature-container',children=[
                    html.Div(children=[

                        html.Div(
                            # daq.Gauge(
                            #     showCurrentValue=True,
                            #     units="°C",
                            #     # TODO: change the value with current temperature
                            #     value=20,
                            #     min=-50,
                            #     max=50,
                            #     size=150
                            # ),
                            daq.Thermometer(
                                min=-10,
                                max=40,
                                value=20,
                                showCurrentValue=True,
                                units="C",
                                label='Temperature',
                                style={'font-size':'100px'}
                            )

                        ),
                        html.Div(
                            daq.Gauge(
                                color={
                                    "gradient":True,
                                    "ranges":{
                                        "green":[0,60],
                                        "yellow":[60,80],
                                        "red":[80,100]
                                    }
                                },
                                label='Humidity',
                                showCurrentValue=True,
                                units="%",
                                # TODO: change the value with current Humidity %
                                value=20,
                                min=0,
                                max=100,
                                size=150
                            ),
                        ),

                    ]),

                ]),
                html.Div(id='feature-container',children=[

                    html.Div(children=[

                        html.Img(
                            src='assets/images/fan.png',
                            className="feature-img", 
                            id='fan-img',
                            style=style_img_fan
                        ),

                    ]),
                    
                    html.Div([
                        html.Button(
                            'Fan On',
                            className="button-style", 
                            id='fan-switch', 
                            n_clicks=0,
                            style={}
                        )
                    ])
                    
                ]),
            ])
        ]),

    ]
)



@app.callback(
    [Output('light-switch', 'children'),
    #  Output('light-switch', 'style'),
     Output('light-switch', 'title'),
     Output('light-img', 'src'),
     Output('light-img', 'style'),],
    Input('light-switch', 'n_clicks')
)

def update_button(n_clicks):
    bool_disabled = n_clicks % 2
    if bool_disabled:
        # GPIO.output(LED,1)
        return 'Turn Off', 'Too bright', img_light_on, style_img_light_on
    else: 
        # GPIO.output(LED,0)
        return 'Turn On','Too dark', img_light_off, style_img


@app.callback(
    [Output('fan-switch','children'),
     Output('fan-img', 'src')],
    Input('fan-switch', 'n_clicks')
)

def control_fan(n_clicks):
    # print("dfd");
    bool_disabled = n_clicks % 2
    """ TODO find a way to resolve that
    if bool_disabled:
        GPIO.output(LED,1)
        return 'Fan is On', fan_on
    else: 
        GPIO.output(LED,0)
        return 'Fan is off', fan_off
    """
    
    if bool_disabled:
        reply = receiveRecentEmail()
        if reply == True:
            n_clicks == 0
            return 'Fan is On', fan_on
        else:
            n_clicks == 0
            return 'Fan is off', fan_off
    else:
        n_clicks == 0
        return 'Fan is off', fan_off
    




# GET the most RECENT email from recipients
def receiveRecentEmail():

    unique_token = generate_token(token_length);
    send_email(subject, body, sender, recipients, password, unique_token)    

    while True:
        imap_ssl_host = 'imap.gmail.com'
        # imap_ssl_host = 'smtp.gmail.com'
        imap_ssl_port = 993
        imap = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
        imap.login(sender, password)

        imap.select("Inbox")
        _, msgnums = imap.search(None, f'FROM "{recipients}" UNSEEN') #to only check email of a specific person
        if msgnums[0]:
            msgnum = msgnums[0].split()[-1]

            _, data = imap.fetch(msgnum, "(RFC822)")
            message = email.message_from_string(data[0][1].decode("utf-8"))

            from_ = email.utils.parseaddr(message.get('From'))[1] #to only get the email address
            to_ = message.get('To')
            date_ = message.get('Date')
            subject_ = message.get('Subject')

            # if subject_ == "Re: " + subject: 
            print('#-----------------------------------------#')
            print(f"From: {from_}")  #to only get the email address
            print(f"To: {to_}")
            print(f"Date: {date_}")
            print(f"Subject: {subject_}")
            print("Content:")
            # print (f'{subject} {unique_token}')
            for part in message.walk():

                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))

                if content_type == "text/plain" and 'attachment' not in content_disposition: 
                    msgbody = part.get_payload()

                    first_line = msgbody.split('\n', 1)[0]
                    print(first_line);
        
                    if str(first_line).strip().lower() == "yes" and subject_ == f'Re: {unique_token}':
                        print("Fan will turn ON")
                        imap.close()  
                        return True;
                    else:
                        print("2. Failed to respond in time. Fan is OFF.")
                        imap.close()  
                        return False;

        else:
            print("1. Failed to respond in time. Fan is OFF.")
            imap.close()  
            # return False;

    
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
    msg.attach(MIMEText(subject))

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


#TODO somehow implement it
# def monitor_temperature_and_send_email():
#     while True:
#         humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT_PIN)

#         if temperature is not None and temperature > temperature_threshold:
#             unique_token = generate_token(token_length)
#             send_email(subject, body, sender, recipients, password, unique_token, temperature)

#         sleep(60)

# Run the app
if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)
    app.run(debug=True)
    # monitor_temperature_and_send_email()