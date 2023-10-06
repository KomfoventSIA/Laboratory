from Hardware.Class_Serial import Serial


class Nozzles2(Serial):

    def __init__(self):
        super().__init__()
        self.nozzle_pressure_coef: int = 10
        self.open_nozzles: dict = {'nz1': True,   # nozzle 76.2
                                   'nz2': True,  # nozzle 101.6
                                   'nz3': True,  # nozzle 127
                                   'nz4': True,  # nozzle 152.4
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
        Specific for stand 2
        Calculates air flow from nozzles for Stand 2 from measured pressure in procedure: def nozzle_pressure(serial)
        Opened and Closed nozzles should be marked as True or Fals
        """

        if self.open_nozzles['nz1']:    # equation for nozzle 76.2
            first_nozzle_flow = 20.937 * pow(nozzles_pressure, 0.498)
        else:
            first_nozzle_flow = 0

        if self.open_nozzles['nz2']:    # equation for nozzle 101.6
            second_nozzle_flow = 35.9 * pow(nozzles_pressure, 0.505)
        else:
            second_nozzle_flow = 0

        if self.open_nozzles['nz3']:    # equation for nozzle 127
            third_nozzle_flow = 58.8 * pow(nozzles_pressure, 0.497)
        else:
            third_nozzle_flow = 0

        if self.open_nozzles['nz4']:    # equation for nozzle 152.4
            fourth_nozzle_flow = 76.9 * pow(nozzles_pressure, 0.515)
        else:
            fourth_nozzle_flow = 0

        air_flow = first_nozzle_flow + second_nozzle_flow + third_nozzle_flow + fourth_nozzle_flow
        return round(air_flow)
