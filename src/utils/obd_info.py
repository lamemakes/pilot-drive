# Tested with the ELM27-emulator package: https://github.com/Ircama/ELM327-emulator

import logging
import os
import threading
import time
import obd
from pint import UnitRegistry

class CarInfo:
    def __init__(self, port):

        # Set logger
        self.log = logging.getLogger()

        # Initial vars
        self.port = port
        self.connected = False


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

    # Connection management loop for the OBDII functionality
    def obd_manager(self):
        path_warned = False
        while True:
            while not self.connected:
                if os.path.exists(self.port):
                    self.connection = obd.OBD(self.port)
                    time.sleep(0.2)
                    self.check_connection()
                else:
                    if not path_warned:
                        self.log.warn("ODBII path: " + self.port + " does not exist.")
                        path_warned = True
                    time.sleep(0.2)

            path_warned = False
            time.sleep(1)

    def run(self):
        obd_thread = threading.Thread(target=self.obd_manager, name = 'obd_manager', daemon=True)
        obd_thread.start()

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
    