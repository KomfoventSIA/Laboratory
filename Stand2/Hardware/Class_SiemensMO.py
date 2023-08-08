from Hardware.Class_Actuator import Actuator


class SiemensMO(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type: str = 'Siemens'
        # registers
        self.setpoint_register_address: int = 0
        self.setpoint_coefficient: int = 100

        self.override_register_address: int = 1
        self.override_off: int = 0
        self.command_open: int = 1
        self.command_close: int = 2

        self.mode_register_address: int = 258
        self.vav_mode: int = 0
        self.pos_mode: int = 1

        self.airflow_register_address: int = 4
        self.airflow_coefficient: int = 1

        self.dynamic_pressure_register_address: int = 5
        self.pressure_coefficient: int = 10




