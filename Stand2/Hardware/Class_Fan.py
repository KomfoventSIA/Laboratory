from Hardware.Class_Serial import Serial

class Fan(Serial):
    def __init__(self):
        super().__init__()
        self.power_coeficent: int = 100
        self.modbus_number: int = 60
        self.command: int = 6
        self.setpoint_register_number: int = 1
        self.mode_register_number: int = 0

    def set_run_mode(self):
        package = Serial.create_package(self.modbus_number, self.command, self.mode_register_number, 1)
        Serial.communicate(package)

    def set_fan_power(self, fan_power: int):
        """
        """
        self.set_run_mode()
        power = fan_power*self.power_coeficent
        package = Serial.create_package(self.modbus_number, self.command, self.setpoint_register_number, power)
        Serial.communicate(package)



