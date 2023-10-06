import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Notification:
    def __init__(self):
        self.notification: bool = False

        self.mail_config: dict = {'host': '',
                                  'port': 0,
                                  'login': '',
                                  'password': '',
                                  'from': '',
                                  'to': '',
                                  'subject': ''}

    def send_mail_notification(self, message: str):
        s = smtplib.SMTP(host=self.mail_config['host'], port=self.mail_config['port'])
        s.login(self.mail_config['login'], self.mail_config['password'])

        msg = MIMEMultipart()

        msg['From'] = self.mail_config['from']
        msg['To'] = self.mail_config['to']
        msg['Subject'] = self.mail_config['subject']
        msg.attach(MIMEText(message))
        s.send_message(msg)
        del msg

