from Hardware.Class_Serial import Serial

class Fan(Serial):
    def __init__(self):
        super().__init__()
        self.power_coeficent: int = 10
        self.modbus_number: int = 1
        self.command: int = 6
        self.register_number: int = 203

    def set_fan_power(self, fan_power: int):
        """
        Set AOUT1 voltage signal from E2408DF sensor in order to regulate fan in stand Nr.1
        Input: serial - created COM port object, load - unsigned int from 0 to 100 what corresponds 0-100% of load
        return nothing
        """
        power = fan_power*self.power_coeficent
        package = Serial.create_package(self.modbus_number, self.command, self.register_number, power)
        Serial.communicate(package)



