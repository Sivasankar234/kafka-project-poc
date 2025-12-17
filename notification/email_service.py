import sys
import os

from dotenv import load_dotenv
# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.logger import get_logger

load_dotenv()
logger = get_logger("EmailService")

class EmailService:
    def __init__(self):
        self.user = os.getenv("GMAIL_USER")
        self.password = os.getenv("GMAIL_PASS")

    def send_email(self, to_email, subject, message):
        try:
            logger.info(f"Sending email to {to_email}")

            msg = MIMEMultipart()
            msg["From"] = self.user
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(message, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.user, self.password)
            server.sendmail(self.user, to_email, msg.as_string())
            server.quit()

            logger.info("Email sent successfully")

        except Exception:
            logger.exception("Failed to send email")
