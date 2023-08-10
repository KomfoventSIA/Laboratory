import PySimpleGUI as sg

class NotificationWindow():
    def __init__(self):
        self.notification: bool = False
        mwcb = sg.Checkbox('Send e-mail notification', key='-send-', enable_events=True, default=self.notification)
        mwt1 = sg.Text('Host:', pad=((5, 9), (1, 1)))
        mwi1 = sg.Input(default_text='mx.ays.lt', key='-host-', size=[30, None], disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi1.Disabled = False
        mwt2 = sg.Text('Port:', pad=((15, 5), (1, 1)))
        mwi2 = sg.Input(default_text='587', key='-port-', size=[20, None], disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi2.Disabled = False
        mwt3 = sg.Text('Login:', pad=((5, 5), (1, 1)))
        mwi3 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-login-', size=[30, None], disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi3.Disabled = False
        mwt4 = sg.Text('Password:', pad=((15, 5), (1, 1)))
        mwi4 = sg.InputText(default_text='BhtVye1298', key='-password-', password_char='*', size=[20, None],
                            disabled=True, disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi4.Disabled = False
        mwt5 = sg.Text('From:')
        mwi5 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-from-', size=[30, None], disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi5.Disabled = False
        mwt6 = sg.Text('To:')
        mwi6 = sg.Input(default_text='genadijs.jeniceks@komfovent.com', key='-to-', size=[30, None], disabled=True,
                        disabled_readonly_background_color='#8294C4')
       # if MeasObj.notification: mwi6.Disabled = False
        mwt7 = sg.Text('Subject:')
        mwi7 = sg.Input(default_text='Notification from Stand 1', key='-subject-', size=[30, None], disabled=True,
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

    def create_notification_window(self):
        window = sg.Window('Stand Nr.1', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
