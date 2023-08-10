from modbus_crc import add_crc  # library for signature - add at the end of bytearray CRC sum
from modbus_crc import check_crc  # library for check CRC sum of received package
from time import gmtime, strftime  # for time mark
from Measurements.Stand_Exception import StandException


class Serial:

    com_port = None

    @classmethod
    def write_to_log(cls, info: str, comment: str):
        """
        Writes to log.txt file specific information with time mark
        """

        time_mark = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        file = open('log.txt', 'a')
        file.write(time_mark + ' ' + info + ' ' + comment + '\n')
        file.write('' + '\n')  # add empty line for better perception
        file.close()

    @classmethod
    def create_package(cls, unit_number: int, command: int, reg_number: int, data: int):
        """
        Create package for sentd to serial port
        Input: Hardware unit number, command, register number, data for write or bit for read
        Transforms to bytearray for send as output package
        """
        byte_unit_number = bytearray(unit_number.to_bytes(1, 'big'))  # transfer unit number to bytearray
        byte_command = bytearray(command.to_bytes(1, 'big'))  # transfer command to bytearray
        byte_reg_number = bytearray(reg_number.to_bytes(2, 'big'))  # transfer register number to bytearray
        byte_data = bytearray(data.to_bytes(2, 'big'))  # transfer read/write datas to bytearray

        # make data array
        package = byte_unit_number + byte_command + byte_reg_number + byte_data
        output_package = add_crc(package)  # add to array Modbus CRC checksum
        return output_package
    @classmethod
    def communicate(cls, package):
        """
        Input: bytearray
        Methode send package to Serial port, gets an answer, check the answer and returns answer as bytearray
        Methode writes to log.txt file time mark, send package and received package.
        """
        response = b''
        try:
            cls.com_port.open()  # opens COM port
        except:
            # cls.com_port.close()
            raise StandException('Can`t open COM port')
        for i in range(3):
            cls.com_port.write(package)  # send a package
            response = cls.com_port.read(8)
            cls.write_to_log(str(package), 'To Port')
            cls.write_to_log(str(response), 'From Port')

            if response != b'':
                if check_crc(response):
                    if package[0] == response[0] and package[1] == response[1]:
                        break
                    elif i < 2:
                        continue
                    else:
                        cls.write_to_log('Error: ', 'Wrong answer from external unit')
                        cls.com_port.close()
                        raise StandException('Wrong answer from external unit')
                elif i < 2:
                    continue
                else:
                    cls.write_to_log('Error: ', 'Wrong CRC summ')
                    cls.com_port.close()
                    raise StandException('Wrong CRC summ')
            elif i < 2:
                continue
            else:
                cls.write_to_log('Error: ', 'No answer from external unit')
                cls.com_port.close()
                raise StandException('No answer from external unit')

        cls.com_port.close()
        return response
    @classmethod
    def mod_response_to_int(cls, modbus_response: bytearray):
        """
        Transfers Modbus response for 03 command for one register to int.
        """

        hex_data = [modbus_response[3], modbus_response[4]]
        byte_data = bytes(hex_data)
        int_data = int.from_bytes(byte_data, 'big')
        return int_data
