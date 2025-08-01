import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender_email = "mohamedlafram500@gmail.com"
password = "lieb quyj cbjw ziol"  

receiver_email = "mohamedlafram004@gmail.com"



def send_email(recipient,subject,body):
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        message.attach(MIMEText(body,'plain'))

        with smtplib.SMTP('smtp.gmail.com',587) as server:
            server.starttls()
            server.login(sender_email,password)
            server.sendmail(sender_email,recipient,message.as_string())
        print('email sended')
    except Exception as e:
        print(f'erreur {e}')



subject = 'test email sent'

body = 'this is a test of a script that send emails'
send_email(receiver_email,subject,body)
print('cheack email')