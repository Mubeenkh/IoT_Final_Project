import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from time import sleep
from itertools import chain
import email
import imaplib
import pprint

subject = "The current temperature is ***. Would you like to turn on the fan?"
body = ""

sender = "python01100922@gmail.com"
password = "txlzudjyidtoxtyj"

recipients = "extramuffin0922@gmail.com"


def send_email(subject, body, sender, recipients, password):

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg.attach(MIMEText(body, 'plain'))

    print("Connecting to server..")
    smtp_server =  smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # smtp_server =  imaplib.IMAP4_SSL("imap.gmail.com", 465)

    # print("Starting TTLS..")
    # smtp_server.starttls()

    print("Logging in..")
    smtp_server.login(sender, password)
    print("Successfully Logged In!")

    smtp_server.sendmail(sender, recipients, msg.as_string())
    # smtp_server.quit()
    print('Email sent successfully.')


    print("Message sent! Please respond within 60sec!")

    sleep(30)


# GET the most RECENT email from recipients
def receiveRecentEmail():
# https://www.youtube.com/watch?v=4iMZUhkpWAc

    send_email(subject, body, sender, recipients, password)
    

    # imap_ssl_host = 'imap.mail.me.com'
    imap_ssl_host = 'imap.gmail.com'
    # imap_ssl_host = 'smtp.gmail.com'
    imap_ssl_port = 993
    imap = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
    imap.login(sender, password)

    imap.select("Inbox")

    _, msgnums = imap.search(None, f'FROM "{recipients}" UNSEEN') #to only check email of a specific person
    
    # print(msgnums[0])
    
    # msgbody = ""

    #  GET the most recent email sent by the recipient  
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
        for part in message.walk():

            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))

            if content_type == "text/plain" and 'attachment' not in content_disposition: 
                msgbody = part.get_payload()

                first_line = msgbody.split('\n', 1)[0]
                # print(len(str(first_line).strip().lower()))
                # print(str(first_line).strip().lower())
                if str(first_line).strip().lower() == "yes":
                    print("Fan will turn ON")
                # imap.close()
                # break
    else:
        print("Failed to respond in time. Fan is OFF.")
    # time.sleep(10)
    imap.close()



if __name__ == '__main__':

    # send_email(subject, body, sender, recipients, password)
    
    # receiveEmail()
    
    receiveRecentEmail()

    # print("done")
    