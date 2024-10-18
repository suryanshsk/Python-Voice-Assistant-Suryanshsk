import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email validation function
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to send an email
def send_email(subject, body, to_email):
    try:
        # Environment variables for sensitive data
        smtp_server = os.getenv('SMTP_SERVER', 'sandbox.smtp.mailtrap.io')
        smtp_port = int(os.getenv('SMTP_PORT', 2525))
        sender_email = os.getenv('SENDER_EMAIL', 'yourusername')
        send_password = os.getenv('SEND_PASSWORD', 'yourpassword')

        # Validate recipient email
        if not is_valid_email(to_email):
            raise ValueError("Invalid recipient email address.")

        # Create a MIME multipart message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = to_email
        message['Subject'] = subject

        # Attach the email body as plain text
        message.attach(MIMEText(body, 'plain'))

        # Establish SMTP connection and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, send_password)
            server.sendmail(sender_email, to_email, message.as_string())

        print(f"Email successfully sent to {to_email}")

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Please check your email username and password.")
    except smtplib.SMTPConnectError:
        print("Failed to connect to the SMTP server.")
    except ValueError as ve:
        print(f"Value Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Test email sending
    send_email("Enhanced Test Email", "This is an enhanced test email body.", "testemail@gmail.com")
