
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sender = ''

key = "alilaijlijdalijli"
port_number = 5000 # temporary until domain name and url is decided upon 
confirm_link = f'<a href="http://127.0.0.1:{port_number}/confirm/{key}">Confirm </a>' 

message = Mail(
    from_email='gordon.site.mailing@gmail.com',
    to_emails='gordon.hamilton1110@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content=f'{confirm_link}')

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    # print("sent")
    response = sg.send(message)

except Exception as e:
    print(e.message)