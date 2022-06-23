
# RESTful naming conventions https://restfulapi.net/resource-naming/

from flask import Flask, jsonify, render_template
from utils import adb_manager, update_manager, bt_ctl, sys_utils
from time import sleep
from pilot_drive.config import PilotConfig
import logging

log = logging.getLogger()

config_man = PilotConfig(log)
pilot_cfg = config_man.run()

log.info("Logging level set to: " + str(pilot_cfg["logging"]["logLevel"]))

# Initalize the updater
updater = update_manager.PilotUpdater(current_version=pilot_cfg["version"], pypi_url=pilot_cfg["updates"]["projectUrl"])

# Initalize the backup camera (if enabled)
try:
    if pilot_cfg["camera"]["enabled"]:
        from utils import camera_manager
        backup_camera = camera_manager.CameraManager(pilot_cfg["camera"]["buttonPin"])
except Exception as e:
    log.error("Failed to enable camera:")

# Initialize the OBDII controller
if pilot_cfg["obd"]["enabled"]:
    from utils import obd_manager
    car_man = obd_manager.CarManager(port=pilot_cfg["obd"]["port"])
    car_man.run()

# Initialize the android debug bus controller
if pilot_cfg["adb"]["enabled"]:
    adb_man = adb_manager.AndroidManager()
    adb_man.run()

# Initialize the bluetooth controller
bt_man = bt_ctl.BluetoothManager()
bt_man.run()

# Initialize the app object and set the static/templates folders
# TODO: Make this class based
app = Flask(__name__, static_folder="web/static", template_folder="web/templates")


""" 
==================
UI HTML Page
================== 
"""

# Returns the main landing page of PILOT
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


"""
==================
System methods
==================
"""

# The time getting function to keep PILOT's clock realtively on par
# TODO: Better method of implementation? This is inacurate to about a half minute.
@app.route("/get-cpuload", methods=["POST"])
def get_cpuload():
    return jsonify({"cpu" : sys_utils.get_cpu_state() + "%"})


# Return the system hostname
@app.route("/get-hostname", methods=["POST"])
def get_hostname():
    return jsonify({"hostname" : sys_utils.get_hostname()})


"""
==================
Auto-Updater methods
==================
"""

# Check for updates
@app.route("/check-updates/get-updates", methods=["POST"])
def check_updates():
    # A python dict is returned describing the status of the update (error or success)
    status_message = updater.check_update()
    return jsonify(status_message)

@app.route("/check-updates/confirm-update", methods=["POST"])
def install_updates():
    # Re-write the config with the new version
    pilot_cfg["version"] = updater.new_release_version
    config_man.write_config(pilot_cfg)

    # A python dict is returned describing the status of the update (error or success)
    updater.update_pilot(release_info=updater.new_release_info, update_path=pilot_cfg["updates"]["downloadPath"])
        

"""
==================
Bluetooth methods
================== 
"""

# Gets the track information, returns track metadata and status in a JSON string.
@app.route("/bt-info", methods=["POST"])
def music_info():
    if bt_man.connected:
        # Get all track data
        bt_man.get_track_data()
        if bt_man.track_info:
            track_info = bt_man.track_info
        else:
            track_info = None

        # Get track playback status
        track_status = bt_man.get_track_status()
        
        return jsonify({"btInfo" : {"connected" : bt_man.connected,
                                    "connectedDevice" : {"name" : bt_man.device_name, "address" : bt_man.device_addr},
                                    "track" : {"metadata" : track_info, "status" : track_status}}})

    # If conditionals are False, return a null value
    return jsonify({"btInfo" : {"connected" : bt_man.connected}})


# Deals with track control. Valid commands are "prev", "next", or "playback-change"
# TODO: Remove returns
@app.route("/bt-ctl/track-ctl/<command>", methods=["POST"])
def prev_track(command):
    if bt_man.connected:
        if command == "prev" or command =="next":
            bt_man.bluetooth_ctl(command)
            
            # Delay and return full track info
            sleep(0.5)

        elif command == "playback-change":
            # A little logic to change the state to the opposite of what it currently is
            if bt_man.status == "playing":
                bt_man.bluetooth_ctl("pause")
                bt_man.status = "paused"
            elif bt_man.status == "paused":
                bt_man.bluetooth_ctl("play")
                bt_man.status = "playing"

            return jsonify({"track" : {"status" : bt_man.status}})

    # If conditionals are False, return a null value
    return jsonify({"connected" : bt_man.connected})



""" 
==================
Vehicle methods
================== 
"""

# The car command endpoint, uses conditionals to determine how the values need to be manipulated
# TODO: Should this have individual endpoints? Seems convoluted
@app.route("/vehicle-info", methods=["POST"])
def car_command():
    if pilot_cfg["obd"]["enabled"]:
        if car_man.connected:

            try:
                # Conditionals to check what command was used 
                speed = round(car_man.get_command("speed"), 2)
                # TODO: Fix this, temporary as emmulator doesn't support gas
                # fuel_level = round(car_man.get_command("fuel_level"), 2)
                fuel_level = 56
                voltage = round(car_man.get_command("voltage"), 2)
                rpm = car_man.get_command("rpm")
                eng_load = car_man.get_command("eng_load")
                dtc = car_man.get_command("dtc")

            except TypeError:
                return jsonify({"vehicleInfo" : None})

            return jsonify({"vehicleInfo" : {"connection" : car_man.connected,
                                            "speed" : speed, 
                                            "fuelLevel" : fuel_level, 
                                            "voltage" : voltage, 
                                            "rpm" : rpm, 
                                            "engLoad" : eng_load,
                                            "dtc" : dtc}})
                                            
    return jsonify({"vehicleInfo" : {"connection" : False}})

""" 
==================
ADB methods
================== 
"""
@app.route("/adb-info", methods=["POST"])
def get_adb():
    if pilot_cfg["adb"]["enabled"]:
        if adb_man.connected:
            return jsonify ({"android" : {
                                "connection" : adb_man.connected,
                                "notifications" : adb_man.get_notifications(), 
                                "battery" : adb_man.get_battery_level(),
                                "hostname" : adb_man.device_name,
                                "macAddr" : adb_man.bt_addr}})
        
    return jsonify({"android" : {
                        "connection" : False}})


    

def main():
    log.info("Starting Flask Application...")
    app.run(host="0.0.0.0", port=5000)

# Run the Application
if __name__ == "__main__":
    main()