import smtplib

def sendemail(message) :
    email = '' # Your email
    password = '' # Your email account password
    send_to_email = '' # Who you are sending the message to
    server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
    server.starttls() # Use TLS
    server.login(email, password) # Login to the email server
    server.sendmail(email, send_to_email , message) # Send the email
    server.quit() # Logout of the email server