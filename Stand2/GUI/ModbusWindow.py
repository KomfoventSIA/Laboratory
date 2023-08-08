import PySimpleGUI as sg
import serial
import serial.tools.list_ports_windows
from Hardware.Class_Serial import Serial
from Measurements.Stand_Exception import StandException


class ModbusWindow:
    def __init__(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ COM port configuration parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        available_com = serial.tools.list_ports_windows.comports()
        if not available_com:
            raise StandException('Connect serial port')
        mt1 = sg.Text('Port')
        mi1 = sg.Combo(values=available_com, default_value=available_com[0], size=(10, 1), key='-port-')
        mt2 = sg.Text('Baudrate')
        baudrate = [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800, 921600]
        mc2 = sg.Combo(values=baudrate, default_value=baudrate[3], size=(10, 1), key='-baudrate-')
        mt3 = sg.Text('Bytesize')
        bytesize = [5, 6, 7, 8]
        mi3 = sg.Combo(values=bytesize, default_value=bytesize[3], size=(10, 1), key='-bytesize-')
        mt4 = sg.Text('Parity')
        parities = ['Even', 'Mark', 'None', 'Odd', 'Space']
        # Serial object takes parities as E/M/N/O/S characters.
        self.parity_dic = {'Even': 'E', 'Mark': 'M', 'None': 'N', 'Odd': 'O', 'Space': 'S'}
        mc4 = sg.Combo(values=parities, default_value=parities[2], size=(10, 1), key='-parity-')
        mt5 = sg.Text('Stopbit')
        stop_bit = [1, 2, 1.5]
        mi5 = sg.Combo(values=stop_bit, default_value=stop_bit[0], size=(10, 1), key='-stopbit-')
        mt6 = sg.Text('Read timeout')
        mi6 = sg.Input(default_text=1, size=(10, 1), key='-r_timeout-')
        mt7 = sg.Text('Write timeout')
        mi7 = sg.Input(default_text=1, size=(10, 1), key='-w_timeout-')

        mb1 = sg.Button('OK')

        mb_col1 = sg.Column([[mt1], [mt2], [mt3], [mt4], [mt5], [mt6], [mt7]])
        mb_col2 = sg.Column([[mi1], [mc2], [mi3], [mc4], [mi5], [mi6], [mi7]])

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create serial port class ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.layout = [[mb_col1, mb_col2],
                       [mb1]
                       ]

    def create_modbus_window(self):
        window = sg.Window('Stand Nr.2 Modbus', self.layout)

        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            elif event == 'OK':
                Serial.com_port = serial.Serial(port=values['-port-'][0],
                                                baudrate=int(values['-baudrate-']),
                                                bytesize=int(values['-bytesize-']),
                                                parity=self.parity_dic[values['-parity-']],
                                                stopbits=int(values['-stopbit-']),
                                                timeout=int(values['-r_timeout-']),
                                                write_timeout=int(values['-w_timeout-']))
                Serial.com_port.close()
                window.close()

        window.close()
