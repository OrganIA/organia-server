
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def getContent():
    res = ''
    with open('mailRes.txt') as f:
        contract = f.readlines()
        for lines in contract :
            res = res+lines          
    f.close()
    return res

def sendMail(From, To, Subject, Content):
    
    message = Mail(
        from_email=From,
        to_emails=To,
        subject=Subject,
        html_content=Content
        )
    try:
        # os.environ.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def sendEmails(From, To, Subject):
    Content = getContent()
    sendMail(From, To, Subject, Content)

# main('mailRes.txt', 'botorgania@gmail.com', 'botorgania@gmail.com', 'test subject')