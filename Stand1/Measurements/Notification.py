from Measurements.Stand_Exception import StandException
import  os
class Notification:
    def __init__(self):
        self.mail_config = {}

        self.users: list = []
        self.config_file_path = os.getcwd() + '.mailconfig'
        try:
            with open('.mailconfig', 'r') as mail_config_file:
                while True:
                    line = mail_config_file.readline()
                    print(line, line[0], line[1])
                    if line[0] == 'User':
                        self.users.append(line[1])
                        print(line[1])
                    if not line:
                        break
        except:
            StandException("'.mailconfig' file do not exist")


        self.notification: bool = False
        self.smtp_host: str = 'mx.ays.lt'
        self.mail_port: int = 587
        self.mail_login: str = ''
        self.mail_password: str = ''
        self.mail_from: str = ''
        self.mail_to: str = ''
        self.mail_subject: str = ''