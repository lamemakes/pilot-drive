import os
import json
import logging
import re
import pilot_drive.__init__

log = logging.getLogger()

# LUT for the logging config option.
LOGGING_LUT = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL}


config_file = "config.json"

def generate_config(enable_cam, btn_pin, enable_adb, enable_obd, obd_port):

    # Get the version of the current PILOT Drive build
    pilot_version = pilot_drive.__init__.__version__
    

    with open(config_file, "w") as cfg:
        # Populate the config with a skeleton of the config
        config_contents = {"pilot-drive" : {
                                    "version" : pilot_version,
                                    "updates" : {"projectUrl" : "https://pypi.org/pypi/pilot-drive/json", "downloadPath" : "/tmp/"},
                                    "obd" : {"enabled" : enable_obd, "port" : obd_port},
                                    "adb" : {"enabled" : enable_adb},
                                    "logging" : {"logLevel" : "INFO", "logToFile" : False, "logPath" : ""},
                                    "camera" : {"enabled" : enable_cam, "buttonPin" : btn_pin}
                                    }}
        
        cfg.writelines(json.dumps(config_contents, indent=2))

def read_config():
    log.info("Attempting to read config file: " + config_file)
    with open(config_file, "r") as cfg:
        pilot_cfg = json.loads(cfg.read())
    
    return pilot_cfg

def write_config(pilot_cfg):
    log.info("Attempting to write to config file: " + config_file)
    full_config = {"pilot-drive" : pilot_cfg}
    with open(config_file, "w") as cfg:
        cfg.write(json.dumps(full_config, indent=2))

if not os.path.isfile(config_file):
    log.info("Attemping to create config file at: " + config_file)
    # Generic config, disabling all main features to allow for running on a machine that isn't an RPi.
    generate_config(enable_cam=False, enable_adb=False, enable_obd=False, obd_port=None, btn_pin=0)

# Open the JSON config file and read it
try:
    pilot_cfg = read_config()["pilot-drive"]
except KeyError:
    log.error("Invalid configuration file! \"pilot-drive\" key not found!")
    exit()


# Get the logging object associated with the provided string and set it.
if pilot_cfg.get("logging").get("logLevel") in LOGGING_LUT:
    pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get(pilot_cfg.get("logging").get("logLevel"))
    log.info("Logging level set to: " + str(pilot_cfg.get("logging").get("logLevel")))
else:
    log.info("No valid log level found in \"" + config_file + "\", defaulting to INFO.")
    pilot_cfg["logging"]["logLevel"] = LOGGING_LUT.get("INFO")

if __name__ == "__main__":
    import sys
    arguments = sys.argv[1:]
    for i in range(len(arguments)):
        if arguments[i] == "0":
            arguments[i] = False
        elif arguments[i] == "1":
            arguments[i] = True

    enable_cam, btn_pin, enable_adb, enable_obd, obd_port = arguments

    generate_config(enable_cam, btn_pin, enable_adb, enable_obd, obd_port)