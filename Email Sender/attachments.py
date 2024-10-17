import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


smtp_port = 587                 
smtp_server = "smtp.gmail.com"  

# Set up the email lists
email_from = "" #Enter your email address
email_attachments = [
    ("gmail1@gmail.com", "image0.pdf"),
    ("gmail2@gmail.com", "image1.png"),
    ("gmail3@gmail.com", "image2.png")
]

# Define the password for the email
pswd = "" #password after 2 factor authentication 

subject = "Hello!"

# Define the email function
def send_emails(email_attachments):
    for recipient, filename in email_attachments:
       
        body = f"""
        Its WORKING!!!  :D
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        attachment = open(filename, 'rb') 
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        text = msg.as_string()

        # Connect with the server
        print("Have Patience bro...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Connected to server :-)")
        print()

        # Send email to recipient
        print(f"Sending email to: {recipient}...")
        TIE_server.sendmail(email_from, recipient, text)
        print(f"Email sent to: {recipient}")
        print()

        # Close the attachment file
        attachment.close()

    # Close the port
    TIE_server.quit()

send_emails(email_attachments)
