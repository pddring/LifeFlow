import ssl
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json


def send(emergency_sender_name):
    #this function is called from the main python script
    # Record the MIME types of both parts - text/plain and text/html.

    # me == my email address
    # you == recipient's email address
    me = "noreply.lifeflow@gmail.com"
    you = "noreply.lifeflow@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    message = MIMEMultipart("alternative")
    message["From"] = "LifeFlow <noreply.lifeflow@gmail.com>"
    message["To"] = you
    message["Subject"] = "LifeFlow Alert System"

    # Create the body of the message (a plain-text and an HTML version).
    text = """\
        LifeFlow Alert System, Please Enable Email HTML
    """

    html = """\
    <html>
    <head></head>
    <body style="
    width: 100%;
    padding: 1pc 0;
    overflow: hidden;">
        <div class="content" style="width: 300px;
        border: 2px solid rgb(229, 229, 229);
        background-color: white;
        padding: 1pc;
        text-align: center;
        margin: 0 auto;
        border-radius: 0.5pc;
        font-family: 'Roboto Condensed', sans-serif;">
            <h1 style="text-align: center;
            font-family: 'Roboto Condensed', sans-serif;">Emergency Alert</h1>
            <hr style="border: 1px solid #89A02C;">
            <br>
            <p style="font-size: 1.2rem;"><b>""" + emergency_sender_name + """</b> has activated their emergency alert button. We Strongly suggest you attempt to get in touch with them as soon as possible.
            </p>
            <p style="font-size: 1.2rem;">
            The necessary emergency services have been notified.
            </p>
            <br>
            <a style="font-size: 1.2rem; color: black; text-decoration: none; background-color: #89A02C; margin: 0 auto; padding: 0.7pc 2pc; border-radius: 0.1pc;" href="https://sites.google.com/view/life-flow/email/whathappens">Learn More</a>
            <br>
            <br>
            <p class="fine" 8stlye="font-size: 1rem;
            color: rgb(158, 158, 158);">For security purposes, more information will be shared with you via an SMS message.</p>
            
            <br>
            <a href="#" style="style="cursor:default;"><img src="https://github.com/megacooki/petabyte-studios/blob/main/icons/large.png?raw=true" style="width: 60%; padding: 0 20%; "></a>
            <br>
            <br>
        </div>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    mail = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)

    mail.ehlo()

    with open("key.json", "r") as f:
        data = json.load(f)

    mail.login('noreply.lifeflow@gmail.com', data["key"])
    mail.sendmail(me, you, message.as_string())  
    mail.quit()

if __name__ == '__main__':
    #if this script is executed on its own (not via antother script)  run the fololowing code:
    send()