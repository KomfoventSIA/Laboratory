from Measurements.Measurements import Measurements
from GUI.ModbusWindow import ModbusWindow
from Measurements.Stand_Exception import StandException
import PySimpleGUI as sg
import time
from threading import Thread

class ManualModeWindow(Measurements):
    def __init__(self, stand='Stand Nr.1'):
        super().__init__()
        self.stand = stand
        print('Manual Window', self.stand)

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
        if self.stand == 'Stand Nr.2':
            sn = [
                sg.Checkbox('76.2', key='-nz1-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('101.6', key='-nz2-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('127', key='-nz3-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('152.4', key='-nz4-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('fake', key='-nz5-', default=False, visible=False)
            ]
        else:  # in case stand == 'Stand Nr.1'
            sn = [
                sg.Checkbox('19.05', key='-nz5-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('25.4', key='-nz4-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('38.1', key='-nz3-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('50.8', key='-nz2-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
                sg.Checkbox('76.2', key='-nz1-', default=True, enable_events=True, pad=(5, 5), expand_x=True)
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
        # t1 = Thread(target=self.constantly_read_nozles_flow(), args=())
        # t1.start()

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            try:
                if event == 'Modbus':
                        mb_window = ModbusWindow()
                        mb_window.create_modbus_window()

                elif event == '-nz5-':
                    self.set_nozzle('nz5', window['-nz5-'].get())
                elif event == '-nz4-':
                    self.set_nozzle('nz4', window['-nz4-'].get())
                elif event == '-nz3-':
                    self.set_nozzle('nz3', window['-nz3-'].get())
                elif event == '-nz2-':
                    self.set_nozzle('nz2', window['-nz2-'].get())
                elif event == '-nz1-':
                    self.set_nozzle('nz1', window['-nz1-'].get())

                elif event == '-belimo-':
                    self.set_actuator('Belimo')
                    if values['-vav-']:
                        self.actuator.application_vav()
                    else:
                        self.actuator.application_pos()
                elif event == '-siemens-':
                    self.set_actuator('Siemens')
                    if values['-vav-']:
                        self.actuator.application_vav()
                    else:
                        self.actuator.application_pos()
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
                    if values['-gruner-']:
                        raise StandException('Not allowed for Gruner')
                    else:
                        self.actuator.application_pos()

                elif event == 'Submit':
                    self.actuator.set_setpoint(int(values['-setpoint-']))

                elif event == 'Set Fan':
                    self.fan.set_fan_power(int(values['-fan_load-']))

                elif event == 'Get Flow [m3/h]':
                    # window['Get Flow [m3/h]'].click()
                    window['-airflow-'].update(str(self.read_nozles_flow()))

                # elif event == 'Get Flow [m3/h]':
                    # flow = []
                    # for i in range(5):
                    #     pressure = self.nozzles.read_nozzle_pressure()
                    #     flow.append(self.nozzles.nozzle_air_flow(pressure))
                    #     time.sleep(1)
                    # average_flow = sum(flow)/5
                    # window['-airflow-'].update(str(average_flow))

            except StandException as sx:
                sg.popup_error(sx.get_exception_name())

        window.close()
