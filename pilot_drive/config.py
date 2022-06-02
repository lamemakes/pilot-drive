import os
import json
import logging
import re
import pilot_drive.__init__


# LUT for the logging config option.
LOGGING_LUT = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL}

class PilotConfig:
    def __init__(self, log):
        self.log = log

        self.config_file = "/etc/pilot-drive/config/config.json"

        # Create logging dir path which will create pilot-drive dir path 
        os.makedirs("/etc/pilot-drive/logging/", exist_ok=True)

    def generate_config(self, enable_cam, btn_pin, enable_adb, enable_obd, obd_port):

        # Get the version of the current PILOT Drive build
        pilot_version = pilot_drive.__init__.__version__
        
        self.log.info("Attempting to write to config file: " + self.config_file)
        if "/" in self.config_file:
            # Create the directories recursively if they don't exist
            directory_path = "/".join(self.config_file.split("/")[:-1]) + "/"
            print("Attempting to create directory path: \"" + directory_path + "\"")
            os.makedirs(directory_path, exist_ok=True)

        with open(self.config_file, "w") as cfg:
            # Populate the config with a skeleton of the config
            config_contents = {"pilot-drive" : {
                                        "version" : pilot_version,
                                        "updates" : {"projectUrl" : "https://pypi.org/pypi/pilot-drive/json", "downloadPath" : "/tmp/"},
                                        "obd" : {"enabled" : enable_obd, "port" : obd_port},
                                        "adb" : {"enabled" : enable_adb},
                                        "logging" : {"logLevel" : "INFO", "logToFile" : True, "logPath" : ""},
                                        "camera" : {"enabled" : enable_cam, "buttonPin" : btn_pin}
                                        }}
            
            cfg.writelines(json.dumps(config_contents, indent=2))

            # Return the absolute path of the config file
            return os.path.abspath("config.json")

    def read_config(self):
        self.log.info("Attempting to read config file: " + os.path.abspath(self.config_file))
        with open(self.config_file, "r") as cfg:
            pilot_cfg = json.loads(cfg.read())
        
        return pilot_cfg

    def write_config(self, pilot_cfg):
        self.log.info("Attempting to write to config file: " + self.config_file)
        if "/" in self.config_file:
            # Create the directories recursively if they don't exist
            directory_path = "/".join(self.config_file.split("/")[:-1]) + "/"
            print("Attempting to create directory path: \"" + directory_path + "\"")
            os.makedirs(directory_path, exist_ok=True)

        full_config = {"pilot-drive" : pilot_cfg}

        with open(self.config_file, "w") as cfg:
            cfg.write(json.dumps(full_config, indent=2))
    
    def run(self):
        if not os.path.isfile(self.config_file):
            self.log.info("Attemping to create config file at: " + self.config_file)
            # Generic config, disabling all main features to allow for running on a machine that isn't an RPi.
            self.generate_config(enable_cam=False, enable_adb=False, enable_obd=False, obd_port=None, btn_pin=0)

        # Open the JSON config file and read it
        try:
            pilot_cfg = self.read_config()["pilot-drive"]
        except KeyError:
            self.log.error("Invalid configuration file! \"pilot-drive\" key not found!")
            exit()

        # Get the logging object associated with the provided string and set it.
        if pilot_cfg.get("logging").get("logLevel") in LOGGING_LUT:
            pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get(pilot_cfg.get("logging").get("logLevel"))
            self.log.info("Logging level set to: " + str(pilot_cfg.get("logging").get("logLevel")))
        else:
            self.log.info("No valid log level found in \"" + self.config_file + "\", defaulting to INFO.")
            pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get("INFO")

        logging.basicConfig(level=pilot_cfg["logging"]["logLevel"], filename=pilot_cfg["logging"]["logPath"])

        self.log.info("Attempting to read config file: " + os.path.abspath(self.config_file))

        return pilot_cfg

if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:]
    for i in range(len(arguments)):
        if arguments[i] == "0":
            arguments[i] = False
        elif arguments[i] == "1":
            arguments[i] = True

    pilot_cfg = PilotConfig(logging.getLogger())

    enable_cam, btn_pin, enable_adb, enable_obd, obd_port = arguments

    print(pilot_cfg.generate_config(enable_cam, btn_pin, enable_adb, enable_obd, obd_port))