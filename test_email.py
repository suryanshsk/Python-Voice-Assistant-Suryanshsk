import smtplib

def send_email(subject, body, to_email):
    try:

        smtp_server = 'sandbox.smtp.mailtrap.io'
        smtp_port = 2525                # Provided by Mailtrap
        sender_email = 'yourusername'  # Use Mailtrap's provided username
        send_password = 'yourpassword'  # Use Mailtrap's provided password

        message = f'Subject: {subject}\n\n{body}'

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  
            server.login(sender_email, send_password)
            server.sendmail(sender_email, to_email, message)

            print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    send_email("Test Email", "This is a test email body", "testemail@gmail.com")
