# The code below imports all the needed libraries
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import time

# Email configuration (Variables)
smtp_server = 'smtp.example.com'  # Website URL that has the SMTP server
smtp_port = 587  # Connection port with your SMTP server Default port is 587 for SSL/TLS
sender_email = 'marketingagency.mih@gmail.com'  # Company Email that the emails will be sent from, Gmail don't work
password = 'your_password'  # The password for the email account sending emails
subject = 'Elevate Your Earnings with MIH Marketing Agency\'s Dynamic Affiliate Program!'  # Subject of the email
body = open('mihemailtemplate.txt', 'r')  # Email template file
emails = open('emaillist.txt', 'r')  # File with all the emails
lines = emails.readlines()  # Array of individual email addresses and names

# Number of emails to send per minute
emails_per_minute = 300


# The main function that sends email while changing the name of the recipient and email address
def send_emails(email, name):
    try:
        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject

        user_body = body.read().replace('{name}', name)  # This gets the message and changes the recipients name

        # Add customised body to the email
        message.attach(MIMEText(user_body, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, password)  # Login to the server

        # Send email
        text = message.as_string()
        server.sendmail(sender_email, email, text)

        # Close the connection
        server.quit()
    except Exception as e:
        print(f"Error sending email: {e}")


# Calculate the time interval between sending each email
interval = 60 / emails_per_minute

# Start sending emails in a loop
while True:
    start_time = time.time()
    threads = []

    # Open the file
    with open(r"emaillist.txt", 'r') as fp:
        # length of lines
        x = len(fp.readlines())

        # Loop through emails and names and send the customised email
        for i in range(x):
            thread = threading.Thread(target=send_emails(lines[i].split(',')[0], lines[i].split(',')[1]))
            threads.append(thread)
            thread.start()
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Calculate time taken to send emails
    elapsed_time = time.time() - start_time

    # Wait for the remaining time in the minute
    if elapsed_time < 60:
        time.sleep(60 - elapsed_time)