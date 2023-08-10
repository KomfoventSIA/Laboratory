import PySimpleGUI as sg

class ConfigWindow:
    def __init__(self):
        cwt1 = sg.Text('Delay between Fan set and measurements start')
        cwi1 = sg.Input(size=(10, 1), default_text=60, key='-measurement_delay-')
        cwt1_2 = sg.Text('sec')
        cwt2 = sg.Text('Delay between measurements')
        cwi2 = sg.Input(size=(10, 1), default_text=10, key='-meas_step_delay-')
        cwt2_2 = sg.Text('sec')
        cwt3 = sg.Text('Measurements in one point')
        cwi3 = sg.Input(size=(10, 1), default_text=3, key='-meas_step-')
        cwt4 = sg.Text('Actuator open time')
        cwi4 = sg.Input(size=(10, 1), default_text=120, key='-act_open_time-')
        cwt4_2 = sg.Text('sec')
        cwt5 = sg.Text('Actuator change position time')
        cwi5 = sg.Input(size=(10, 1), default_text=30, key='-act_cp_time-')
        cwt5_2 = sg.Text('sec')
        cwb1 = sg.Button('OK')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Layout section. ~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.layout = [
            [cwt1, cwi1, cwt1_2],
            [cwt2, cwi2, cwt2_2],
            [cwt3, cwi3],
            [cwt4, cwi4, cwt4_2],
            [cwt5, cwi5, cwt5_2],
            [cwb1]
        ]

    def create_config_window(self, obj):
        window = sg.Window('Stand Nr.1 Config', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'OK':
                try:
                    obj.measurement_delay = int(values['-measurement_delay-'])
                    obj.meas_step_delay = int(values['-meas_step_delay-'])
                    obj.meas_step = int(values['-meas_step-'])
                    obj.actuator_open_time = int(values['-act_open_time-'])
                    obj.actuator_change_position_time = int(values['-act_cp_time-'])
                except ValueError:
                    sg.popup_error('Should be a number.')
                window.close()

        window.close()

