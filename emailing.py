
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


port_number = 5000 # temporary until domain name and url is decided upon 
to_email = 'gordon.hamilton1110@gmail.com'
site_email  = 'gordon.site.mailing@gmail.com'
    
    
def confirm_sub(key, email):
    confirm_link = f'<a href="http://127.0.0.1:{port_number}/confirm/{key}">Confirm </a>' 
    
    message = Mail(
    from_email= site_email,
    to_emails= email,
    subject='Confirm Stealth Blog Subscription',
    html_content=f'{confirm_link}')

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)

    except Exception as e:
        print("error when trying to confirm subscription: "+ e.message)
    return
    
# email can only be sent from verified user in Sendgrid
def quote_inquiry(name, email, company, message):
    message += f"\n Contact: {email}" 
    
    message = Mail(
    from_email= site_email,
    to_emails=to_email,
    subject=f'Quote Request from {name} at {company}',
    html_content = message)

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY')) 
        sg.send(message)

    except Exception as e:
        print("error when trying to send email quote inquiry: " + e.message)
    return