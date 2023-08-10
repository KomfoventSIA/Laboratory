from Hardware.Class_Serial import Serial

class Device(Serial):
    def __init__(self, device_name='Noname', device_id=None, read_command=None, write_command=None,
                 register_address=None, read_coefficient=None, write_coefficient=None):
        super().__init__()
        self.device_name: str = device_name
        self.device_id: int = device_id
        self.read_command: int = read_command
        self.write_command: int = write_command
        self.register_address: int = register_address
        self.read_coefficient: int = read_coefficient
        self.write_coefficient: int = write_coefficient

    def write_to_device(self, data):
        """
        """
        setpoint = data * self.write_coefficient
        package = Serial.create_package(self.device_id, self.write_command, self.register_address, setpoint)
        Serial.communicate(package)

    def read_from_device(self):
        """
        """
        package = Serial.create_package(self.device_id, self.read_command, self.register_address, 1)
        response = Serial.communicate(package)
        return Serial.mod_response_to_int(response)/self.read_coefficient

