from Hardware.Class_Actuator import Actuator


class GrunerMOD(Actuator):
    def __init__(self):
        super().__init__()
        self.actuator_type: str = 'Gruner'
        # registers
        self.setpoint_register_address: int = 0
        self.setpoint_coefficient: int = 100

        self.override_register_address: int = 1
        self.override_off: int = 0
        self.command_open: int = 1
        self.command_close: int = 2

        self.airflow_register_address: int = 7
        self.airflow_coefficient: int = 1

        self.dynamic_pressure_register_address: int = 200
        self.pressure_coefficient: int = 10

    def application_vav(self):
        """
        """
        raise Exception('Only VAV application allowed for Gruner actuator')

    def application_pos(self):
        """
        """
        raise Exception('Only VAV application allowed for Gruner actuator')


