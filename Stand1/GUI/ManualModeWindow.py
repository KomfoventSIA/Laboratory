from Measurements.Measurements import Measurements
from GUI.ModbusWindow import ModbusWindow
from Measurements.Stand_Exception import StandException
import PySimpleGUI as sg
import time
class ManualModeWindow(Measurements):
    def __init__(self):
        super().__init__()

        menu_def = [['Tools', ['Modbus', ]]]
        menu = sg.Menu(menu_def, key='-menu-', size=(30, 10))

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

        choose_actuator_frame = sg.Frame('Choose actuator type', [ca,
                                                                  mode,
                                                                  [spt, spi, spb, actuator_open, actuator_close]],
                                         expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Nozzles Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sn = [
            sg.Checkbox('19.05', key='-19-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('25.4', key='-25-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('38.1', key='-38-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('50.8', key='-50-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('76.2', key='-76-', default=True, enable_events=True, pad=(5, 5), expand_x=True)
        ]
        set_nozzles_frame = sg.Frame('Set open nozzles', [sn], size=(340, 50), expand_x=True, expand_y=True,
                                     pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Fan  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flt = sg.Text('Fan Load 20-100%:')
        fli = sg.Input(size=(5, 1), pad=(0, 5), key='-fan_load-', do_not_clear=False)  # Fan Load Input
        flb = sg.Button('Set Fan')

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Stand Flow  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        flot1 = sg.Text('Airflow:')
        flot2 = sg.Text('0', pad=(0, 5), key='-airflow-')
        flob = sg.Button('Get Flow [m3/h]')

        self.layout = [[menu],
                       [set_nozzles_frame],
                       [choose_actuator_frame],
                       [flt, fli, flb, flot1, flot2, flob]
                       ]

    def create_manual_window(self):
        window = sg.Window('Stand Nr.2 Manual mode', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break

            elif event == 'Modbus':
                try:
                    mb_window = ModbusWindow()
                    mb_window.create_modbus_window()
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())
            elif event == '-19-':
                self.set_nozzle('19.05', window['-19-'].get())
            elif event == '-25-':
                self.set_nozzle('25.4', window['-25-'].get())
            elif event == '-38-':
                self.set_nozzle('38.1', window['-38-'].get())
            elif event == '-50-':
                self.set_nozzle('50.8', window['-50-'].get())
            elif event == '-76-':
                self.set_nozzle('76.2', window['-76-'].get())

            elif event == '-belimo-':
                self.set_actuator('Belimo')
            elif event == '-siemens-':
                self.set_actuator('Siemens')
            elif event == '-gruner-':
                self.set_actuator('Gruner')
            elif event == '-none-':
                self.set_actuator('None')
            elif event == '-custom-':
                pass

            elif event == 'Open':
                self.actuator.actuator_open()

            elif event == 'Close':
                self.actuator.actuator_close()

            elif event == '-vav-':
                self.actuator.application_vav()

            elif event == '-pos-':
                self.actuator.application_pos()

            elif event == 'Submit':
                self.actuator.set_setpoint(int(values['-setpoint-']))

            elif event == 'Set Fan':
                self.fan.set_fan_power(int(values['-fan_load-']))

            elif event == 'Get Flow [m3/h]':
                flow = []
                for i in range(5):
                    flow.append(self.nozzles.nozzle_air_flow(self.nozzles.read_nozzle_pressure()))
                    time.sleep(1)
                average_flow = sum(flow)/5
                window['-airflow-'].update(str(average_flow))

        window.close()
