import smtplib, ssl

def send_gmail(Subject, Body, user_email):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "deepinderbrardeep03@gmail.com"  # Enter your address
    receiver_email = user_email  # Enter receiver address
    password = "ziinatmkccvtyzqq"
    message = f"""\
    Subject: {Subject}.

    {Body}."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
