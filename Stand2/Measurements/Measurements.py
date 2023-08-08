from os.path import exists
from time import gmtime, strftime  # for time mark
from Hardware.Class_Fan import Fan
from Hardware.Class_Nozzles import Nozzles
from Hardware.Class_Actuator import Actuator
from Hardware.Class_SiemensMO import SiemensMO
from Hardware.Class_BelimoMOD import BelimoMOD
from Hardware.Class_GrunerMOD import GrunerMOD
from Hardware.Class_Device import Device
from Measurements.Stand_Exception import StandException
import pandas as pd
import numpy
import xlsxwriter
import time


class Measurements:

    def __init__(self):
        self.measurement_start: str = 'No start time'
        self.measurement_end: str = 'No end time'
        self.table_headers_config: dict = {'default headers': ['Nr', 'Fan Power, %',
                                                               'Nozzle Pressure, Pa',
                                                               'Nozzle Flow, m3/h'],
                                           'blade position': False,
                                           'actuator type': 'None',
                                           'addition device': False}
        self.table_data: list = [['Nr', 'Fan Power, %', 'Nozzle Pressure, Pa', 'Nozzle Flow, m3/h']]
        self.rows_quantity: int = 0
        self.count_files: int = 0
        self.measurement_delay: int = 60

        self.actuator_open_time: int = 120  # in sec
        self.actuator_change_position_time: int = 30
        self.meas_step_delay: int = 10
        self.meas_step: int = 3


        self.fan = Fan()
        self.nozzles = Nozzles()
        self.actuator = Actuator()
        self.additional_device = Device()
        print(self.additional_device.device_name)

    def measurement_start_time(self):
        self.measurement_start = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def measurement_end_time(self):
        self.measurement_end = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def set_actuator(self, actuator_type: str = 'None'):

        if actuator_type == 'Belimo':
            self.actuator = BelimoMOD()
            self.table_headers_config['actuator type'] = self.actuator.actuator_type
        elif actuator_type == 'Siemens':
            self.actuator = SiemensMO()
            self.table_headers_config['actuator type'] = self.actuator.actuator_type
        elif actuator_type == 'Gruner':
            self.actuator = GrunerMOD()
            self.table_headers_config['actuator type'] = self.actuator.actuator_type
        elif actuator_type == 'None':
            self.table_headers_config['actuator type'] = 'None'
            self.actuator = None
        elif actuator_type == 'Custom':
            pass

    def set_addition_device(self, device_name='Noname', device_id=None, read_command=None, write_command=None,
                 register_address=None, read_coefficient=None):
        self.additional_device = Device(device_name=device_name,
                                        device_id=int(device_id),
                                        read_command=int(read_command),
                                        write_command=int(write_command),
                                        register_address=int(register_address),
                                        read_coefficient=int(read_coefficient))

    def update_table_headers(self):
        self.table_data = [[]]
        self.rows_quantity: int = 0
        self.table_data[0].append('Nr')
        self.table_data[0].append('Fan Power, %')
        self.table_data[0].append('Nozzle Pressure, Pa')
        self.table_data[0].append('Nozzle Flow, m3/h')
        for config in self.table_headers_config:
            if config == 'blade position':
                if self.table_headers_config[config]:
                    self.table_data[0].insert(1, 'Blade Position, %')
            if config == 'actuator type':
                if self.table_headers_config[config] == 'Belimo':
                    self.table_data[0].append('Actuator Flow, m3/h')
                elif self.table_headers_config[config] == 'Siemens' or self.table_headers_config[config] == 'Gruner':
                    self.table_data[0].append('Actuator Pressure, Pa')
                    self.table_data[0].append('Actuator Flow, m3/h')
            if config == 'addition device':
                if self.table_headers_config[config]:
                    self.table_data[0].append(self.additional_device.device_name)

    def set_nozzle(self, key, value: bool):
        self.nozzles.open_nozzles[key] = value

    def delete_row(self):
        if self.rows_quantity > 0:
            self.table_data.pop()
            self.rows_quantity -= 1
        else:
            self.rows_quantity = 0

    def add_row(self, fan_power, blade_position=None):
        self.table_data.append([])
        self.rows_quantity += 1
        for header in self.table_data[0]:
            if header == 'Nr':
                self.table_data[self.rows_quantity].insert(0, str(self.rows_quantity))
            elif header == 'Fan Power, %':
                try:
                    if int(fan_power) < 15 or int(fan_power) > 100:
                        raise StandException('Fan Power range could be from 15 to 100%')
                    else:
                        self.table_data[self.rows_quantity].insert(self.table_data[0].index(header), str(fan_power))
                except:
                    self.delete_row()
                    raise StandException('Fan Power range could be from 15 to 100%')
            elif header == 'Blade Position, %':
                try:
                    if int(blade_position) < 0 or int(blade_position) > 100:
                        raise StandException('Blade Position range could be from 0 to 100%')
                    else:
                        self.table_data[self.rows_quantity].insert(self.table_data[0].index(header), str(blade_position))
                except:
                    self.delete_row()
                    raise StandException('Blade Position range could be from 0 to 100%')
            else:
                self.table_data[self.rows_quantity].insert(self.table_data[0].index(header), '')

    def load_measurement_template(self, path: str = ''):
        try:
            excel_file = pd.read_excel(path)  # read Excel file
        except:
            raise StandException('Choose file')

        # creates Data frame from two defined columns
        data = pd.DataFrame(excel_file, columns=['Fan Power, %', 'Blade Position, %'])
        fan_power = data._get_column_array(0)  # gets from DF data for fan_power
        blade_pos = data._get_column_array(1)
        for row in range(len(fan_power)):
            if not isinstance(fan_power[row], numpy.int64) or fan_power[row] == 'nan':
                raise StandException('Incorrect "Fan Power, %" value in file!')
            else:
                if self.table_headers_config['blade position']:
                    if not isinstance(blade_pos[row], numpy.int64) or blade_pos[row] == 'nan':
                        raise StandException('Incorrect "Blade Position, %" value in file!')
                    else:
                        self.add_row(fan_power[row], blade_pos[row])
                else:
                    self.add_row(fan_power[row])

    def write_to_excel(self, file_name):
        nozzles_list = ''
        for nozzle in self.nozzles.open_nozzles:
            if self.nozzles.open_nozzles[nozzle]:
                nozzles_list += (nozzle + ', ')

        time_mark = strftime("%Y_%m_%d", gmtime())  # Get time mark.
        self.count_files += 1
        full_file_name = time_mark + '_' + file_name + '(' + str(self.count_files) + ')' + '.xlsx'
        if exists(full_file_name):
            raise StandException('File already exist. Set other file name')
        else:
            with xlsxwriter.Workbook(full_file_name) as workbook:
                worksheet = workbook.add_worksheet(file_name)  # add worksheet to file

                # write into table Headers with measurement configuration

                worksheet.write(0, 0, ('Actuator type: ' + self.actuator.actuator_type))
                worksheet.write(1, 0, 'Open Nozzles: ' + nozzles_list)
                worksheet.write(2, 0, 'Flow calm down time, sec: ' + str(self.measurement_delay), )
                worksheet.write(3, 0, 'Delay between measurements, sec: ' + str(self.meas_step_delay), )
                worksheet.write(4, 0, 'Measurements quantity in one point: ' + str(self.meas_step), )
                worksheet.write(5, 0, 'Measurement start time: ' + self.measurement_start)
                worksheet.write(6, 0, 'Measurement end time: ' + self.measurement_end)

                row_index = 8
                col_index = 0
                # write into table measurement results. Data array = [[x,x,x], [x,x,x], ...] row = [x,x,x]; x - value
                for row in self.table_data:
                    for value in row:
                        worksheet.write(row_index, col_index, value)
                        col_index += 1
                    col_index = 0
                    row_index += 1

    def set_measurement_conditions(self, data: int):
        for column in self.table_data[0]:
            column_index = self.table_data[0].index(column)
            if column == 'Nr':
                pass
            elif column == 'Blade Position, %':
                print('Blade pisitioning is active. Sleep time: ', self.actuator_change_position_time)
                self.actuator.override_mode_off()
                self.actuator.application_pos()
                ap_setpoint = self.table_data[data][column_index]
                self.actuator.set_setpoint(int(ap_setpoint))
                time.sleep(self.actuator_change_position_time)
            elif column == 'Fan Power, %':
                f_setpoint = self.table_data[data][column_index]
                print('Fan power set: ', f_setpoint)
                self.fan.set_fan_power(int(f_setpoint))
                print('Measurement delay: ', self.measurement_delay)
                time.sleep(self.measurement_delay)
            else:
                break

    def make_measurement(self, data: int):
        nozzle_pressure = []  # Array of measured pressures in order to get average
        nozzle_flow = []
        actuator_flow = []  # Array of measured actuator air flow in order to get average
        actuator_pressure = []  # Array of measured actuator pressure in order to get average
        addition_device = []  # Array of measured parameter from external device (pressure) in order to get average
        for point in range(self.meas_step):
            for column in self.table_data[0]:
                column_index = self.table_data[0].index(column)
                if column == 'Nozzle Pressure, Pa':
                    print('Column nozzle pressure')
                    nozzle_pressure_help_var = self.nozzles.read_nozzle_pressure()
                    nozzle_pressure.append(nozzle_pressure_help_var)
                    nozzle_flow.append(self.nozzles.nozzle_air_flow(nozzle_pressure_help_var))
                    if point == self.meas_step - 1:
                        print('Nozzle pressure: ', nozzle_pressure)
                        average_nozzle_pressure = round(sum(nozzle_pressure) / self.meas_step, 1)
                        self.table_data[data][column_index] = average_nozzle_pressure
                elif column == 'Nozzle Flow, m3/h':
                    print('Column nozzle flow')
                    if point == self.meas_step - 1:
                        print('Nozzle flow: ', nozzle_flow)
                        average_nozzle_flow = round(sum(nozzle_flow) / self.meas_step, 1)
                        self.table_data[data][column_index] = average_nozzle_flow
                elif column == 'Actuator Pressure, Pa':
                    print('Column actuator pressure')
                    actuator_pressure.append(self.actuator.read_pressure())
                    if point == self.meas_step - 1:
                        print('Actuator pressure: ', actuator_pressure)
                        average_actuator_pressure = round(sum(actuator_pressure) / self.meas_step, 1)
                        self.table_data[data][column_index] = average_actuator_pressure
                elif column == 'Actuator Flow, m3/h':
                    print('Column actuator flow')
                    actuator_flow.append(self.actuator.read_airflow())
                    if point == self.meas_step - 1:
                        print('Actuator flow: ', actuator_flow)
                        average_actuator_flow = round(sum(actuator_flow) / self.meas_step)
                        self.table_data[data][column_index] = average_actuator_flow
                elif column == self.additional_device.device_name:
                    print('Column addition device')
                    addition_device.append(self.additional_device.read_from_device())
                    if point == self.meas_step - 1:
                        print('Addition device: ', addition_device)
                        average_addition_device = round(sum(addition_device) / self.meas_step, 1)
                        self.table_data[data][column_index] = average_addition_device
                else:
                    pass
            time.sleep(self.meas_step_delay)
        print('Repeated measurements: ', self.meas_step)
        print('Delay between measurements: ', self.meas_step_delay)
        print(self.table_data[data])
