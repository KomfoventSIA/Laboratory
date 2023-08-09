from Measurements.Measurements import Measurements
import PySimpleGUI as sg
class ManualModeWindow(Measurements):
    def __init__(self):
        super().__init__()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Actuator Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ca = [
            sg.Radio('Belimo', 'actuator', key='-belimo-', enable_events=True),
            sg.Radio('Siemens', 'actuator', key='-siemens-', enable_events=True),
            sg.Radio('Gruner', 'actuator', key='-gruner-', enable_events=True),
            sg.Radio('None', 'actuator', key='-none-', enable_events=True, default=True),
            sg.Radio('Custom', 'actuator', key='-custom-', enable_events=True, disabled=True)
        ]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Actuator Setpoint ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        mode = [
            sg.Radio('VAV', 'mode', key='-vav-', enable_events=True, default=True),
            sg.Radio('Pos', 'mode', key='-pos-', enable_events=True)
        ]

        spt = sg.Text('Setpoint 0-100%')
        spi = sg.Input(size=(5, 1), pad=(0, 5), key='-setpoint-', do_not_clear=False)
        spb = sg.Button('Submit')

        actuator_open = sg.Button('Open')
        actuator_close = sg.Button('Close')

        choose_actuator_frame = sg.Frame('Choose actuator type', [ca, [mode], [spt, spi, spb, actuator_open, actuator_close]],
                                         expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Nozzles Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sn = [
            sg.Checkbox('76.2', key='-76-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('101.6', key='-101-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('127', key='-127-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('152.4', key='-152-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
        ]
        set_nozzles_frame = sg.Frame('Set open nozzles', [sn], size=(340, 50), expand_x=True, expand_y=True,
                                     pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fan  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flt = sg.Text('Fan Load 20-100%:')
        fli = sg.Input(size=(5, 1), pad=(0, 5), key='-fan_load-', do_not_clear=False)  # Fan Load Input
        flb = sg.Button('Set Fan')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Stand Flow  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        nzt = sg.Text('Airflow:')
        flo = sg.Text('0', pad=(0, 5), key='-airflow-')

        self.layout = [[set_nozzles_frame],
                       [choose_actuator_frame],
                       [flt, fli, flb, nzt, flo]
                       ]

    def create_manual_window(self):
        window = sg.Window('Stand Nr.2 Manual mode', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            elif event == '-76-':
                self.nozzles.set_nozzle('76.2', window['-76-'].get())
            elif event == '-101-':
                self.nozzles.set_nozzle('101.6', window['-101-'].get())
            elif event == '-127-':
                self.nozzles.set_nozzle('127', window['-127-'].get())
            elif event == '-152-':
                self.nozzles.set_nozzle('152.4', window['-152-'].get())

            elif event == '-belimo-':
                self.actuator.set_actuator('Belimo')
            elif event == '-siemens-':
                self.actuator.set_actuator('Siemens')
            elif event == '-gruner-':
                self.actuator.set_actuator('Gruner')
            elif event == '-none-':
                self.actuator.set_actuator('None')
            elif event == '-custom-':
                pass

            elif event == 'Open':
                self.actuator.actuator_open()

            elif event == 'Close':
                self.actuator.actuator_close()

            elif event == '-vav-':
                self.actuator.application_vav()

            elif event == '-vav-':
                self.actuator.application_pos()

            elif event == 'Submit':
                self.actuator.set_setpoint(int(values['-setpoint-']))

            elif event == 'Set Fan':
                self.fan.set_fan_power(int(values['--fan_load--']))

            window['-airflow-'].update(str(self.nozzles.nozzle_air_flow(self.nozzles.read_nozzle_pressure())))

