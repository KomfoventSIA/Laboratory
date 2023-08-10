from Hardware.Class_Serial import Serial

class Actuator(Serial):

    def __init__(self):
        super().__init__()
        self.actuator_type: str = 'Unknown Actuator'
        self.modbus_number: int = 2
        self.read_command: int = 3
        self.write_command: int = 6

        # registers
        self.setpoint_register_address: int = None
        self.setpoint_coefficient:int = None

        self.override_register_address: int = None
        self.override_off: int = None
        self.command_open: int = None
        self.command_close: int = None

        self.mode_register_address: int = None
        self.vav_mode: int = 0
        self.pos_mode: int = 1

        self.airflow_register_address: int = None
        self.airflow_coefficient: int = None

        self.dynamic_pressure_register_address: int = None
        self.pressure_coefficient: int = None


    def write_to_actuator(self, reg_number, data):
        """
        Set override control for siemens actuator. 0 - OFF, 1 - Open, 2 - Close, 3 - Stop, 4 - Vmin, 5 - Vmax
        """
        package = Serial.create_package(self.modbus_number, self.write_command, reg_number, data)
        Serial.communicate(package)

    def read_from_actuator(self, reg_number, data):
        """
        Set override control for siemens actuator. 0 - OFF, 1 - Open, 2 - Close, 3 - Stop, 4 - Vmin, 5 - Vmax
        """
        package = Serial.create_package(self.modbus_number, self.read_command, reg_number, data)
        response = Serial.communicate(package)
        return Serial.mod_response_to_int(response)

    def override_mode_off(self):
        """
        """
        self.write_to_actuator(self.override_register_address, self.override_off)

    def actuator_open(self):
        """
        """
        self.write_to_actuator(self.override_register_address, self.command_open)

    def actuator_close(self):
        """
        """
        self.write_to_actuator(self.override_register_address, self.command_close)

    def application_vav(self):
        """
        """
        self.write_to_actuator(self.mode_register_address, self.vav_mode)

    def application_pos(self):
        """
        """
        self.write_to_actuator(self.mode_register_address, self.pos_mode)

    def set_setpoint(self, setpoint):
        """
        """
        data = setpoint*self.setpoint_coefficient
        self.write_to_actuator(self.setpoint_register_address, data)

    def read_airflow(self):
        """
        """
        air_flow = self.read_from_actuator(self.airflow_register_address, 1)
        return air_flow/self.airflow_coefficient

    def read_pressure(self):
        """
        """
        pressure = self.read_from_actuator(self.dynamic_pressure_register_address, 1)
        return pressure/self.pressure_coefficient

