# email_sender.py

from settings import EMAIL_SENDER, EMAIL_RECEIVER, EMAIL_PASSWORD
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_grouped_email(ads):
    subject = f"{len(ads)} uutta ilmoitusta Tori.fi:ssä"
    body = "Seuraavat ilmoitukset löydettiin:\n\n"

    for ad in ads:
        body += f"""- {ad['title']} ({ad['price']})\n{ad['url']}\nJulkaistu: {ad['posted_time']}\n\n"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"Sähköposti lähetetty ({len(ads)} ilmoitusta).")
    except Exception as e:
        print(f"Virhe sähköpostin lähetyksessä: {e}")
