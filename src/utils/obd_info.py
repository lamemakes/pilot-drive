# Tested with the ELM27-emulator package: https://github.com/Ircama/ELM327-emulator

import obd
from pint import UnitRegistry

class CarInfo:
    def __init__(self, port):
        self.connection = obd.OBD(port)
        self.check_connection()
        # TODO: Potentially add a thread to continously check the connection if it isn't made?

    def get_command(self, command):
        self.check_connection()
        if self.connected:
            command_list = {
                "speed" : obd.commands.SPEED,
                "fuel_level" : obd.commands.FUEL_LEVEL,
                "voltage" : obd.commands.CONTROL_MODULE_VOLTAGE,
                "rpm" : obd.commands.RPM,
                "eng_load" : obd.commands.ENGINE_LOAD,
                "dtc" : obd.commands.GET_DTC
            }

            if command_list.get(command):
                response = self.connection.query(command_list.get(command))

                # Determine if value is numerical (Pint Quantity)
                quantity_type = UnitRegistry().Quantity
                if str(type(response.value)) == str(quantity_type):     # TODO: Fix this jenky solution
                    return response.value.magnitude
                
                # If type is not Pint Quantity, just return the value.
                return response.value

        # If not connected or value not found in dict, return None
        return None

    def check_connection(self):
        self.connected = (self.connection.status() == obd.OBDStatus.CAR_CONNECTED)
        return self.connected

if __name__ == "__main__":
    carInfo = CarInfo("/dev/pts/2")
    if carInfo.connected:
        print("Connection to car established!")
        print("Speed:  \t", carInfo.get_command("speed"))
        # TODO: Fuel Level not supported?
        # print("Fuel:   \t", carInfo.get_command("fuel_level"))
        print("Voltage:\t", carInfo.get_command("voltage"))
        print("RPM:    \t", carInfo.get_command("rpm"))
        print("Eng Load:\t", carInfo.get_command("eng_load"))
        print("DTC:    \t", carInfo.get_command("dtc"))
    