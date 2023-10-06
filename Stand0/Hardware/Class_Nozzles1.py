from Hardware.Class_Serial import Serial


class Nozzles1(Serial):

    def __init__(self):
        super().__init__()
        self.nozzle_pressure_coef: int = 10
        self.open_nozzles: dict = {'nz1': True,  # nozzle 76.2
                                   'nz2': True,  # nozzle 50.8
                                   'nz3': True,  # nozzle 38.1
                                   'nz4': True,  # nozzle 25.4
                                   'nz5': True  # nozzle 19.05
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

    def nozzle_air_flow(self, nozzles_pressure: int):
        """
        Specific for stand 1
        Calculates air flow from nozzles for Stand 1 from measured pressure in procedure: def nozzle_pressure(serial)
        Opened and Closed nozzles should be marked as True or Fals
        """

        if self.open_nozzles['nz1']:    # equation for nozzle 76.2
            first_nozzle_flow = 20.937 * pow(nozzles_pressure, 0.498)
        else:
            first_nozzle_flow = 0

        if self.open_nozzles['nz2']:    # equation for nozzle 50.8
            second_nozzle_flow = 8.48 * pow(nozzles_pressure, 0.5157)
        else:
            second_nozzle_flow = 0

        if self.open_nozzles['nz3']:    # equation for nozzle 38.1
            third_nozzle_flow = 4.4173 * pow(nozzles_pressure, 0.5274)
        else:
            third_nozzle_flow = 0

        if self.open_nozzles['nz4']:    # equation for nozzle 25.4
            fourth_nozzle_flow = 2.0889 * pow(nozzles_pressure, 0.5152)
        else:
            fourth_nozzle_flow = 0

        if self.open_nozzles['nz5']:    # equation for nozzle 19.05
            fifth_nozzle_flow = 1.576 * pow(nozzles_pressure, 0.4668)
        else:
            fifth_nozzle_flow = 0

        air_flow = first_nozzle_flow + second_nozzle_flow + third_nozzle_flow + fourth_nozzle_flow + fifth_nozzle_flow
        return round(air_flow)
