import time
import PySimpleGUI as sg
import os
from Measurements.Measurements import Measurements
from ModbusWindow import ModbusWindow
from MeasConfigWindow import ConfigWindow
from Measurements.Stand_Exception import StandException



class MainWindow:
    def __init__(self):

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Menu bar~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        menu_def = [['Tools', ['Modbus', 'Config', 'Manual Mode', 'Custom Actuator', 'E-mail Notification']]]
        menu = sg.Menu(menu_def, key='-menu-', size=(30, 10))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Choose actuator Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        ca = [
            sg.Radio('Belimo', 'actuator', key='-belimo-', enable_events=True),
            sg.Radio('Siemens', 'actuator', key='-siemens-', enable_events=True),
            sg.Radio('Gruner', 'actuator', key='-gruner-', enable_events=True),
            sg.Radio('None', 'actuator', key='-none-', enable_events=True, default=True),
            sg.Radio('Custom', 'actuator', key='-custom-', enable_events=True, disabled=True)
        ]

        # Set or not damper blade position
        dp = sg.Checkbox('Set blade position', key='-sbp-', default=False, enable_events=True)
        choose_actuator_frame = sg.Frame('Choose actuator type', [ca, [dp]], expand_x=True, expand_y=True,
                                         pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Nozzles Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Stand construction allows only manual nozzle switching. Air flow range  depends on from nozzle configuration
        sn = [
            sg.Checkbox('76.2', key='-76-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('101.6', key='-101-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('127', key='-127-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
            sg.Checkbox('152.4', key='-152-', default=True, enable_events=True, pad=(5, 5), expand_x=True),
        ]
        set_nozzles_frame = sg.Frame('Set open nozzles', [sn], size=(340, 50), expand_x=True, expand_y=True,
                                     pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Set Addition Device Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        adcb = sg.Checkbox('External device', key='-add_dev-', default=False, enable_events=True)
        adt1 = sg.Text('Device Name', pad=((0, 5), (5, 5)))
        adi1 = sg.Input(size=(50, 1), pad=((0, 5), (5, 5)), key='-dev_name-',
                        default_text='External Pressure Sensor, Pa',
                        disabled=True, disabled_readonly_background_color='#8294C4', enable_events=True)
        adt2 = sg.Text('Modbus ID', pad=((0, 5), (5, 5)))
        adi2 = sg.Input(size=(5, 1), pad=((0, 30), (5, 5)), key='-ad_mb_id-', default_text='3',
                        disabled=True, disabled_readonly_background_color='#8294C4', enable_events=True)
        adt3 = sg.Text('Read command', pad=((0, 5), (5, 5)))
        adi3 = sg.Input(size=(5, 1), pad=((0, 30), (5, 5)), key='-ad_mb_command-', default_text='3',
                        disabled=True, disabled_readonly_background_color='#8294C4', enable_events=True)
        adt4 = sg.Text('Read register Nr.', pad=((0, 5), (5, 5)))
        adi4 = sg.Input(size=(5, 1), pad=((0, 5), (5, 5)), key='-ad_mb_reg-', default_text='0',
                        disabled=True, disabled_readonly_background_color='#8294C4', enable_events=True)
        adt5 = sg.Text('Coefficient', pad=((0, 5), (5, 5)))
        adi5 = sg.Input(size=(5, 1), pad=((0, 5), (5, 5)), key='-ad_coef-', default_text='1',
                        disabled=True, disabled_readonly_background_color='#8294C4', enable_events=True)

        addition_device_frame = sg.Frame('Addition Device', [[adcb],
                                                             [adt1, adi1],
                                                             [adt2, adi2, adt3, adi3, adt4, adi4],
                                                             [adt5, adi5]],
                                         expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create Table Frame ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        bpt = sg.Text('Blade Position [%]')
        bpi = sg.Input(size=(5, 1), pad=(0, 5), key='-blade_pos-', do_not_clear=False, metadata=0,
                       disabled=True, disabled_readonly_background_color='#8294C4')
        flt = sg.Text('Fan Load [%]:')
        fli = sg.Input(size=(5, 1), pad=(0, 5), key='-fan_load-', do_not_clear=False)  # Fan Load Input
        arb = sg.Button('Add Row')
        drb = sg.Button('Delete Row')
        dab = sg.Button('Delete All')
        ppp = sg.Push()  # Push next elements max to the right
        fnt = sg.Text('File name: ', pad=((0, 0), (0, 0)))
        fni = sg.Input(default_text='New File', size=(30, 1), pad=(0, 0), key='-file_name-')
        sab = sg.Button('Save File')

        # automatic measurement template load
        current_directory = os.getcwd()
        mtlt = sg.Text('Load Table')
        mtli = sg.InputText(key='-file_path-')
        mtlb = sg.FileBrowse(initial_folder=current_directory, file_types=(('Excel Files', '*.xlsx'),))
        mtlb2 = sg.Button('Submit')

        ct_org_column1 = sg.Column([[bpt],
                                    [flt]])

        ct_org_column2 = sg.Column([[bpi],
                                    [fli]])

        table_conf_frame = sg.Frame('Create Table',
                                    [[ct_org_column1, ct_org_column2, arb, drb, dab, ppp, fnt, fni, sab],
                                     [mtlt, mtli, mtlb, mtlb2]],
                                    expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))

        column_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        default_headers = [['Nr', 'Fan Power, %', 'Nozzle Pressure, Pa', 'Nozzle Flow, m3/h']]
        table = sg.Table(headings=column_num, values=default_headers,
                         vertical_scroll_only=False,
                         auto_size_columns=False,
                         col_widths=[5],
                         pad=(10, 10),
                         def_col_width=15,
                         max_col_width=25,
                         justification='center',
                         key='-table-')
        tableframe = sg.Frame('Table', [[table]], expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Start Button ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        start = sg.Button('START', expand_x=True, expand_y=True, pad=((5, 5), (5, 5)))

        org_column = sg.Column([[choose_actuator_frame],
                                [set_nozzles_frame]])

        self.layout = [[menu],
                       [org_column, addition_device_frame],
                       [table_conf_frame, start],
                       [tableframe]]

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create Window Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def create_main_window(self):
        window = sg.Window('Stand Nr.2', self.layout, size=(915, 500))
        measurements = Measurements()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Create Window Function Section ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        def blade_position_true():
            if window['-blade_pos-'].Disabled:
                window['-blade_pos-'].update(disabled=False, background_color='white')
                measurements.table_headers_config['blade position'] = True
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            else:
                window['-blade_pos-'].update(disabled=True)
                measurements.table_headers_config['blade position'] = False
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)

        def addition_device_true():
            if window['-dev_name-'].Disabled:
                window['-dev_name-'].update(disabled=False, background_color='white')
                window['-ad_mb_id-'].update(disabled=False, background_color='white')
                window['-ad_mb_command-'].update(disabled=False, background_color='white')
                window['-ad_mb_reg-'].update(disabled=False, background_color='white')
                window['-ad_coef-'].update(disabled=False, background_color='white')
                measurements.table_headers_config['addition device'] = True
            else:
                window['-dev_name-'].update(disabled=True)
                window['-ad_mb_id-'].update(disabled=True)
                window['-ad_mb_command-'].update(disabled=True)
                window['-ad_mb_reg-'].update(disabled=True)
                window['-ad_coef-'].update(disabled=True)
                measurements.table_headers_config['addition device'] = False

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
            elif event == 'Config':
                cf_window = ConfigWindow()
                cf_window.create_config_window(measurements)
            elif event == '-belimo-':
                measurements.set_actuator('Belimo')
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == '-siemens-':
                measurements.set_actuator('Siemens')
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == '-gruner-':
                measurements.set_actuator('Gruner')
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == '-none-':
                measurements.set_actuator('None')
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == '-custom-':
                pass

            elif event == '-sbp-':
                blade_position_true()

            elif event == '-76-':
                measurements.set_nozzle('76.2', window['-76-'].get())
            elif event == '-101-':
                measurements.set_nozzle('101.6', window['-101-'].get())
            elif event == '-38-':
                measurements.set_nozzle('127', window['-127-'].get())
            elif event == '-50-':
                measurements.set_nozzle('152.4', window['-152-'].get())

            elif event == '-add_dev-':
                addition_device_true()
                measurements.set_addition_device(device_name=values['-dev_name-'],
                                                 device_id=values['-ad_mb_id-'],
                                                 read_command=values['-ad_mb_command-'],
                                                 write_command=6,
                                                 register_address=values['-ad_mb_reg-'],
                                                 read_coefficient=values['-ad_coef-'],
                                                 )
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)

            elif event == '-dev_name-':
                measurements.additional_device.device_name = values['-dev_name-']
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == '-ad_mb_id-':
                measurements.additional_device.device_id = int(values['-ad_mb_id-'])
            elif event == '-ad_mb_command-':
                measurements.additional_device.read_command = int(values['-ad_mb_command-'])
            elif event == '-ad_mb_reg-':
                measurements.additional_device.register_address = int(values['-ad_mb_reg-'])
            elif event == '-ad_coef-':
                measurements.additional_device.register_address = int(values['-ad_coef-'])

            elif event == 'Add Row':
                try:
                    measurements.add_row(values['-fan_load-'], values['-blade_pos-'])
                    window['-table-'].update(measurements.table_data)
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())
            elif event == 'Delete Row':
                measurements.delete_row()
                window['-table-'].update(measurements.table_data)
            elif event == 'Delete All':
                measurements.update_table_headers()
                window['-table-'].update(measurements.table_data)
            elif event == 'Submit':
                try:
                    measurements.load_measurement_template(values['-file_path-'])
                    window['-table-'].update(measurements.table_data)
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())
            elif event == 'Save File':
                try:
                    measurements.write_to_excel(values['-file_name-'])
                    sg.popup_ok('File Saved')
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())
            elif event == 'START':
                try:
                    measurements.measurement_start_time()
                    if measurements.table_headers_config['actuator type'] != 'None':
                        measurements.actuator.actuator_open()
                        print('Actuator opens. Sleep time: ', measurements.actuator_open_time)
                        time.sleep(measurements.actuator_open_time)
                    for index in range(1, len(measurements.table_data)):
                        measurements.set_measurement_conditions(index)
                        measurements.make_measurement(index)
                        window['-table-'].update(measurements.table_data)
                    measurements.measurement_end_time()
                    measurements.fan.set_fan_power(0)
                    sg.popup_ok('Measurements are finished')
                except StandException as sx:
                    sg.popup_error(sx.get_exception_name())

        window.close()
