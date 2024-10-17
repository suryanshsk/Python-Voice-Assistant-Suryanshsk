import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_port = 587
smtp_server = "smtp.gmail.com"

# Set up the email lists
email_from = ""
email_recipients = [
    "",
    ""
    #Enter array of email addresses
]

# Define the password for the email
pswd = "" #password after 2 factor authentication 

subject = "" #Subject of the email

# Define the email function
def send_emails(email_recipients):
    try:
        # Connect with the server
        print("Connecting, Please wait...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")
        print()
        
        for recipient in email_recipients:
            body = f"""
            Its WORKING!!!  :D  

            """
            
            # Set up the email message
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            text = msg.as_string()

            # Send email to recipient
            print(f"Sending email to: {recipient}...")
            TIE_server.sendmail(email_from, recipient, text)
            print(f"Email sent to: {recipient}")
            print()
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Close the connection
        TIE_server.quit()

send_emails(email_recipients)
