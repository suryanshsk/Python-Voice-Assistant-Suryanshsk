import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_bulk_email(gmail_user, gmail_password, recipients, subject, body):
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587) 
        session.starttls()
        session.login(gmail_user, gmail_password)
        
        for to_email in recipients:
            # Set up the MIME
            message = MIMEMultipart()
            message['From'] = gmail_user
            message['To'] = to_email
            message['Subject'] = subject
            
            # Attach the body with the msg instance
            message.attach(MIMEText(body, 'plain'))
            
            # Convert the message to a string
            text = message.as_string()
            
            # Send the email
            session.sendmail(gmail_user, to_email, text)
            print(f'Mail Sent to {to_email}')
        
        session.quit()
        
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")


