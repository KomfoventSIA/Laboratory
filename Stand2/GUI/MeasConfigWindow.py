import PySimpleGUI as sg
from Measurements.Stand_Exception import StandException

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
        window = sg.Window('Stand Nr.2 Config', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'OK':
                try:
                    if int(values['-measurement_delay-']) > 0:
                        obj.measurement_delay = int(values['-measurement_delay-'])
                    else:
                        raise StandException('Delay between Fan set and measurements start could not be 0 or less')

                    if int(values['-meas_step_delay-']) > 0:
                        obj.meas_step_delay = int(values['-meas_step_delay-'])
                    else:
                        raise StandException('Delay between measurements could not be 0 or less')

                    if int(values['-meas_step-']) > 0:
                        obj.meas_step = int(values['-meas_step-'])
                    else:
                        raise StandException('Measurement quantity could not be 0 or less')

                    if int(values['-act_open_time-']) > 0:
                        obj.actuator_open_time = int(values['-act_open_time-'])
                    else:
                        raise StandException('Actuator open time could not be 0 or less')

                    if int(values['-act_cp_time-']) > 0:
                        obj.actuator_change_position_time = int(values['-act_cp_time-'])
                    else:
                        raise StandException('Actuator change position time could not be 0 or less')

                    window.close()

                except ValueError:
                    sg.popup_error('Should be a number.')
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())

        window.close()

