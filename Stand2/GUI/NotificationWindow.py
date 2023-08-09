import PySimpleGUI as sg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

notification: bool = False

class NotificationWindow():
    def __init__(self):
        self.smtp_host: str = 'mx.ays.lt'
        self.mail_port: int = 587
        self.mail_login: str = ''
        self.mail_password: str = ''
        self.mail_from: str = ''
        self.mail_to: str = ''
        self.mail_subject: str = ''

        mwcb = sg.Checkbox('Send e-mail notification', key='-send-', enable_events=True, default=notification)
        mwt1 = sg.Text('Host:', pad=((5, 9), (1, 1)))
        mwi1 = sg.Input(default_text='mx.ays.lt', key='-host-', size=(30, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi1.Disabled = False
        mwt2 = sg.Text('Port:', pad=((15, 5), (1, 1)))
        mwi2 = sg.Input(default_text='587', key='-port-', size=(20, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi2.Disabled = False
        mwt3 = sg.Text('Login:', pad=((5, 5), (1, 1)))
        mwi3 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-login-', size=(30, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi3.Disabled = False
        mwt4 = sg.Text('Password:', pad=((15, 5), (1, 1)))
        mwi4 = sg.InputText(default_text='BhtVye1298', key='-password-', password_char='*', size=(20, None),
                            disabled=True, disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi4.Disabled = False
        mwt5 = sg.Text('From:')
        mwi5 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-from-', size=(30, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi5.Disabled = False
        mwt6 = sg.Text('To:')
        mwi6 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-to-', size=(30, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi6.Disabled = False
        mwt7 = sg.Text('Subject:')
        mwi7 = sg.Input(default_text='Notification from Stand 2', key='-subject-', size=(30, None), disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi7.Disabled = False
        ppp = sg.Push()  # Push next elements max to the right

        frameSMTP = sg.Frame('SMTP server config', [[mwt1, mwi1, ppp, mwt2, mwi2]], expand_x=True)
        frameLogin = sg.Frame('Account Login', [[mwt3, mwi3, mwt4, mwi4]])

        col_mail_1 = sg.Column([[mwt5], [mwt6], [mwt7]])
        col_mail_2 = sg.Column([[mwi5], [mwi6], [mwi7]])
        frameMail = sg.Frame('Mail', [[col_mail_1, col_mail_2]])

        mwb1 = sg.Button('Save and Close')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Layout section. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.layout = [
            [mwcb],
            [frameSMTP],
            [frameLogin],
            [frameMail],
            [mwb1]]

    def send_mail_notification(self):

        s = smtplib.SMTP(host=self.smtp_host, port=self.mail_port)
        s.login(self.mail_login, self.mail_password)

        msg = MIMEMultipart()

        msg['From'] = self.mail_from
        msg['To'] = self.mail_to
        msg['Subject'] = self.mail_subject
        msg.attach(MIMEText(self.finish_message))


        s.send_message(msg)

        del msg

    def create_notification_window(self):
        window = sg.Window('Stand Nr.2', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            if event == '-send-':
                if window['-host-'].Disabled:
                    window['-host-'].update(disabled=False, background_color='white')
                else:
                    window['-host-'].update(disabled=True)

                if window['-port-'].Disabled:
                    window['-port-'].update(disabled=False, background_color='white')
                else:
                    window['-port-'].update(disabled=True)

                if window['-login-'].Disabled:
                    window['-login-'].update(disabled=False, background_color='white')
                else:
                    window['-login-'].update(disabled=True)

                if window['-password-'].Disabled:
                    window['-password-'].update(disabled=False, background_color='white')
                else:
                    window['-password-'].update(disabled=True)

                if window['-from-'].Disabled:
                    window['-from-'].update(disabled=False, background_color='white')
                else:
                    window['-from-'].update(disabled=True)

                if window['-to-'].Disabled:
                    window['-to-'].update(disabled=False, background_color='white')
                else:
                    window['-to-'].update(disabled=True)

                if window['-subject-'].Disabled:
                    window['-subject-'].update(disabled=False, background_color='white')
                else:
                    window['-subject-'].update(disabled=True)

            if event == 'Save and Close':
                notification = values['-send-']
                MeasObj.smtp_host = values['-host-']
                MeasObj.mail_port = int(values['-port-'])
                MeasObj.mail_login = values['-login-']
                MeasObj.mail_password = values['-password-']
                MeasObj.mail_from = values['-from-']
                MeasObj.mail_to = values['-to-']
                MeasObj.mail_subject = values['-subject-']
                mw_window.close()
