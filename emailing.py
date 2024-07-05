import smtplib  # For sending emails using SMTP protocol
import ssl  # For creating a secure SSL context
import os  # For operating system interactions
import imghdr  # For determining the type of an image
from email.message import EmailMessage  # For creating email messages

# Sender email address and receiver email address
username = "ibrohimovmuhammad2020@gmail.com"
receiver = "ibrohimovmuhammad2020@gmail.com"
# Password for the sender email account retrieved from environment variables
password = os.getenv("PASSWORD")


# Function to send an email with an image attachment
def send_email(image_path):
    print("emailing started")
    # Create an email message object
    email_message = EmailMessage()
    # Set the subject of the email
    email_message["Subject"] = "New customer showed up!"
    # Set the content of the email
    email_message.set_content("Hey, we just saw a new customer")

    # Open the image file in binary read mode
    with open(image_path, "rb") as file:
        content = file.read()
    # Add the image as an attachment to the email
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # Create an SMTP client session object for Gmail's SMTP server
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    # Identify the client to the SMTP server
    gmail.ehlo()
    # Put the SMTP connection in TLS (Transport Layer Security) mode
    gmail.starttls()
    # Log in to the SMTP server using the sender's email credentials
    gmail.login(username, password)
    # Send the email from the sender to the receiver
    gmail.sendmail(username, receiver, email_message.as_string())
    # Terminate the SMTP session
    gmail.quit()
    print("emailing ended")


# If this script is run directly (and not imported as a module), execute the following code
if __name__ == "__main__":
    # Call the send_email function with a sample image path
    send_email(image_path="images/23.png")
