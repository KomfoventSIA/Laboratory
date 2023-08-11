import PySimpleGUI as sg
import os


class NotificationWindow():
    def __init__(self, notfication_config_object):
        mwcb = sg.Checkbox('Send e-mail notification',
                           key='-send-',
                           enable_events=True,
                           default=notfication_config_object.notification)

        current_directory = os.getcwd()
        nfct = sg.Text('Load File')
        nfcti = sg.InputText(key='-file_path-',
                             disabled=True,
                             disabled_readonly_background_color='#8294C4'
                             )
        if notfication_config_object.notification:
            nfcti.Disabled = False
        nfctb = sg.FileBrowse(initial_folder=current_directory,
                              key='-browse-',
                              file_types=(('ALL Files', '*.mailconfig'),),
                              disabled=True
                              )
        if notfication_config_object.notification:
            nfctb.Disabled = False
        nfctb2 = sg.Button('Submit',
                           key='-submit-',
                           disabled=True
                           )
        if notfication_config_object.notification:
            nfctb2.Disabled = False

        mwt1 = sg.Text('Host:', pad=((5, 9), (1, 1)))
        mwi1 = sg.Input(default_text=notfication_config_object.mail_config['host'],
                        key='-host-',
                        size=(30, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi1.Disabled = False
        mwt2 = sg.Text('Port:', pad=((15, 5), (1, 1)))
        mwi2 = sg.Input(default_text=notfication_config_object.mail_config['port'],
                        key='-port-',
                        size=(20, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi2.Disabled = False
        mwt3 = sg.Text('Login:', pad=((5, 5), (1, 1)))
        mwi3 = sg.Input(default_text=notfication_config_object.mail_config['login'],
                        key='-login-',
                        size=(30, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi3.Disabled = False
        mwt4 = sg.Text('Password:', pad=((15, 5), (1, 1)))
        mwi4 = sg.InputText(default_text=notfication_config_object.mail_config['password'],
                            key='-password-',
                            password_char='*',
                            size=(20, None),
                            disabled=True,
                            disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi4.Disabled = False
        mwt5 = sg.Text('From:')
        mwi5 = sg.Input(default_text=notfication_config_object.mail_config['from'],
                        key='-from-',
                        size=(30, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi5.Disabled = False
        mwt6 = sg.Text('To:')
        mwi6 = sg.Input(default_text=notfication_config_object.mail_config['to'],
                        key='-to-',
                        size=(30, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi6.Disabled = False
        mwt7 = sg.Text('Subject:')
        mwi7 = sg.Input(default_text=notfication_config_object.mail_config['subject'],
                        key='-subject-',
                        size=(30, None),
                        disabled=True,
                        disabled_readonly_background_color='#8294C4')
        if notfication_config_object.notification:
            mwi7.Disabled = False
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
            [nfct, nfcti, nfctb, nfctb2],
            [frameSMTP],
            [frameLogin],
            [frameMail],
            [mwb1]]

    def create_notification_window(self, notfication_config_object):
        window = sg.Window('Stand Nr.1', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == '-send-':
                notfication_config_object.notification = values['-send-']
                if window['-file_path-'].Disabled:
                    window['-file_path-'].update(disabled=False, background_color='white')
                else:
                    window['-file_path-'].update(disabled=True)
                if window['-browse-'].Disabled:
                    window['-browse-'].update(disabled=False)
                else:
                    window['-browse-'].update(disabled=True)
                if window['-submit-'].Disabled:
                    window['-submit-'].update(disabled=False)
                else:
                    window['-submit-'].update(disabled=True)
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

            elif event == '-submit-':
                with open(values['-file_path-'], 'r') as file:
                    while True:
                        line = file.readline()
                        if line[0: 5] == 'Host:':
                            host = line[6: line.index('\n')]
                            window['-host-'].update(host)
                        elif line[0: 5] == 'Port:':
                            port = int(line[6: line.index('\n')])
                            window['-port-'].update(port)
                        elif line[0: 6] == 'Login:':
                            login = line[7: line.index('\n')]
                            window['-login-'].update(login)
                        elif line[0: 9] == 'Password:':
                            password = line[10: line.index('\n')]
                            window['-password-'].update(password)
                        elif line[0: 5] == 'From:':
                            mail_from = line[6: line.index('\n')]
                            window['-from-'].update(mail_from)
                        elif line[0: 3] == 'To:':
                            to = line[4: line.index('\n')]
                            window['-to-'].update(to)
                        elif line[0: 8] == 'Subject:':
                            subject = line[8: line.index('\n')]
                            window['-subject-'].update(subject)
                        elif not line:
                            break
                        else:
                            break

                # window['-host-'].update(notfication_config_object.mail_config['host'])
                # window['-port-'].update(notfication_config_object.mail_config['port'])
                # window['-login-'].update(notfication_config_object.mail_config['login'])
                # window['-password-'].update(notfication_config_object.mail_config['password'])
                # window['-from-'].update(notfication_config_object.mail_config['from'])
                # window['-to-'].update(notfication_config_object.mail_config['to'])
                #window['-subject-'].update(notfication_config_object.mail_config['subject'])

            elif event == 'Save and Close':
                notfication_config_object.mail_config['host'] = values['-host-']
                notfication_config_object.mail_config['port'] = int(values['-port-'])
                notfication_config_object.mail_config['login'] = values['-login-']
                notfication_config_object.mail_config['password'] = values['-password-']
                notfication_config_object.mail_config['from'] = values['-from-']
                notfication_config_object.mail_config['to'] = values['-to-']
                notfication_config_object.mail_config['subject'] = values['-subject-']
                window.close()

        window.close()
