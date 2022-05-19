import logging
import re
import subprocess
import threading
import time

from pilot_drive.utils.adb_notification import Notificaton


class AndroidManager:
    def __init__(self):

        # Initial var declarations
        self.log = logging.getLogger()
        self.connected = None
        self.device_name = None
        self.bt_mac = None
        self.notifications = []


        # Initialize ADB
        run_adb_root = "adb root"
        run_root = subprocess.getoutput(run_adb_root)


    # This should run in a thread to update on the side
    def get_notifications(self):
        self.notifications = []

        notif_icon_path = "/data/data/com.android.launcher3/databases/app_icons.db"
        pull_db_cmd = "adb pull " + notif_icon_path

        notif_dump_cmd = "adb shell dumpsys notification --noredact"

        # Get the icon database off the phone
        subprocess.getoutput(pull_db_cmd)

        # Dump the notifications
        notif_dump = subprocess.getoutput(notif_dump_cmd)


        # Prune the list to get only the notifications
        # TODO: Clean this up if possible
        notif_list = notif_dump.split("NotificationRecord(")
        finalNotif = notif_list[len(notif_list) - 1].split("mAdjustments=[]")[0]
        notif_list[len(notif_list) - 1] = finalNotif
        notif_list.pop(0)

        for raw_notification in notif_list:
            new_notification = Notificaton(raw_notification)
            key = new_notification.attributes.get("key").split("|")[4]
            if key:
                self.notifications.append(new_notification.attributes)
        
        # Sort notifications by priority. The highest priority will appear at the top of the JSON.
        self.notifications.sort(reverse=True, key=self.sort_by_priority)
        
        return self.notifications


    # Method to get the battery level of the connected device
    def get_battery_level(self):
        dump_battery_cmd = "adb shell dumpsys battery"

        battery_dump = subprocess.getoutput(dump_battery_cmd)
        self.battery_level = int(re.search("level: (.*)\n", battery_dump).group(1))

        return self.battery_level
        

    # Pull hostname and mac address to compare in the web interface
    def get_bt_info(self):
        device_name_cmd = "adb shell settings get secure bluetooth_name"
        mac_addr_cmd = "adb shell settings get secure bluetooth_address"

        self.device_name = subprocess.getoutput(device_name_cmd)
        self.bt_addr = subprocess.getoutput(mac_addr_cmd)

        return [self.device_name, self.bt_addr]


    # Method to sort the notifications by priority
    def sort_by_priority(self, notification):
        return (notification.get("pri"))


    # Method to constantly check the state of the ADB connection
    def check_connection(self):
        check_connection_cmd = "adb get-state"
        connection_status = subprocess.getoutput(check_connection_cmd)
        if connection_status == "device":
            self.connected = True
        else:
            if self.connected == None or self.connected:
                self.log.error("ADB Device disconnected: " + subprocess.getoutput(check_connection_cmd))
            self.connected = False

        return self.connected


    # Manages the ADB connection, listens for a new connection
    def android_manager(self):
        self.log.debug("ADB Manager Started.")
        while True:
            while not self.connected:
                time.sleep(0.2)
                self.check_connection()

            if not self.device_name:
                self.get_bt_info()
                self.log.debug("ADB Device: " + self.device_name + " connected!")
            
            self.check_connection()
            time.sleep(0.5)


    # Starts the manager thread to monitor the connection
    def run(self):
        adb_thread = threading.Thread(target=self.android_manager, name = 'adb_manager', daemon=True)
        adb_thread.start()


