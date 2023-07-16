import smtplib
from email.mime.text import MIMEText
import yagmail


#Option 1 for sending email: works fine but quite verbose

# def send_email(email_message,email_subject,recipient_email):
#             my_email_address = 'enter_your_email_address'
#             msg = MIMEText(email_message)
#             msg['Subject'] = email_subject
#             msg['From'] = my_email_address
#             msg['To'] = recipient_email
#             with smtplib.SMTP_SSL('smtp.gmail.com',465 ) as smtp_server:#smptm.mail.yahoo.com smtp.gmail.com 465
#                 smtp_server.login(my_email_address, 'enter_your_app_password')
#                 smtp_server.sendmail(my_email_address, recipient_email, msg.as_string())
#             print("Message sent!")
#         

#Option 2 for sending email: works fine and very concise. Highly recommended
# do not forget to do pip install yagmail, might also need to do pip install keyring

def send_email(email_message,email_subject,recipient_email):
    yag = yagmail.SMTP("duis4billion@gmail.com")
    try:
        yag.send(to=recipient_email,
                subject=email_subject,
                contents=email_message)
        return 1
    except Exception:
        return 0
 

