from Hardware.Class_Actuator import Actuator


class BelimoMOD(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type: str = 'Belimo'
        # registers
        self.setpoint_register_address: int = 0
        self.setpoint_coefficient: int = 100

        self.override_register_address: int = 1
        self.override_off: int = 0
        self.command_open: int = 1
        self.command_close: int = 2

        self.mode_register_address: int = 116
        self.vav_mode: int = 1
        self.pos_mode: int = 0

        self.airflow_register_address: int = 7
        self.airflow_coefficient: int = 1


    def read_pressure(self):
        """
        """
        raise Exception('Pressure not available for Belimo actuator')
