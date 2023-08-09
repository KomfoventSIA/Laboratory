from Hardware.Class_Serial import Serial


class Nozzles(Serial):

    def __init__(self):
        super().__init__()
        self.nozzle_pressure_coef: int = 10
        self.open_nozzles: dict = {'76.2': True,
                                   '101.6': True,
                                   '127': True,
                                   '152.4': True,
                                   }
        self.modbus_number: int = 1
        self.command: int = 3
        self.register_number: int = 259  # Pressure reg. address: 259

    def read_nozzle_pressure(self):
        """
        Read measured pressure from E2408DF sensor for stand Nr.1
        Input: serial port object where package should be sent
        return pressure as float with decimal range/
        """

        package = Serial.create_package(self.modbus_number, self.command, self.register_number, 1)
        response = Serial.communicate(package)
        pressure = Serial.mod_response_to_int(response) / self.nozzle_pressure_coef  # Recalculate received int to pressure
        return round(pressure, 1)

    def nozzle_air_flow(self, nozzles_pressure: float):
        """
        Specific for stand 1
        Calculates air flow from nozzles for Stand 1 from measured pressure in procedure: def nozzle_pressure(serial)
        Opened and Closed nozzles should be marked as True or Fals
        """

        if self.open_nozzles['76.2']:
            first_nozzle_flow = 20.937 * pow(nozzles_pressure, 0.498)
        else:
            first_nozzle_flow = 0

        if self.open_nozzles['101.6']:
            second_nozzle_flow = 35.9 * pow(nozzles_pressure, 0.505)
        else:
            second_nozzle_flow = 0

        if self.open_nozzles['127']:
            third_nozzle_flow = 58.8 * pow(nozzles_pressure, 0.497)
        else:
            third_nozzle_flow = 0

        if self.open_nozzles['152.4']:
            fourth_nozzle_flow = 76.9 * pow(nozzles_pressure, 0.515)
        else:
            fourth_nozzle_flow = 0

        air_flow = first_nozzle_flow + second_nozzle_flow + third_nozzle_flow + fourth_nozzle_flow
        return round(air_flow)
