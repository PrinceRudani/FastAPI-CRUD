import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from param.ipython import message

from base.custom_enum.static_enum import StaticVariables
from base.utils.custom_exception import AppServices


class NotificationController:

    @staticmethod
    def send_email_notification(
        to_email=StaticVariables.RECEIVER_EMAIL, subject=None, message=None
    ):
        sender_email = StaticVariables.SENDER_EMAIL
        sender_password = "scau jsvu vjcp lxex"

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.quit()
            return True
        except Exception as exception:
            print("Failed to send email:", exception)
            return AppServices.handle_exception(exception, is_raise=True)
