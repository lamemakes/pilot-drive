import logging
import re
import subprocess
import threading
import time

from utils.adb_notification import Notificaton


class AndroidManager:
    def __init__(self):

        # Initial var declarations
        self.log = logging.getLogger()
        self.connected = False
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
        
        return self.notifications

    def get_battery_level(self):
        dump_battery_cmd = "adb shell dumpsys battery"

        battery_dump = subprocess.getoutput(dump_battery_cmd)

        self.battery_level = int(re.search("level: (.*)\n", battery_dump).group(1))

        return self.battery_level
    

    def get_bt_info(self):
        device_name_cmd = "adb shell settings get secure bluetooth_name"
        mac_addr_cmd = "adb shell settings get secure bluetooth_address"

        self.device_name = subprocess.getoutput(device_name_cmd)
        self.bt_addr = subprocess.getoutput(mac_addr_cmd)

        return [self.device_name, self.bt_addr]


    def check_connection(self):
        check_connection_cmd = "adb get-state"
        self.connected = ("device" in subprocess.getoutput(check_connection_cmd))
        return self.connected


    def android_manager(self):
        self.log.debug("ADB Manager Started.")
        while True:
            while not self.connected:
                time.sleep(0.2)
                self.check_connection()

            if not self.device_name:
                self.get_bt_info()
                self.log.debug("ADB Device: " + self.device_name + " connected!")
            
            time.sleep(0.5)


    def run(self):
        adb_thread = threading.Thread(target=self.android_manager, name = 'adb_manager', daemon=True)
        adb_thread.start()
        

if __name__ == "__main__":
    adb_test = AndroidManager()
    print("=" * 32)
    for id in adb_test.notifications:
        for key in adb_test.notifications.get(id).notification_keys:
            print(key + " : " + str(adb_test.notifications.get(id).attributes.get(key)))
        print("Icon Path : " + str(adb_test.notifications.get(id).icon_path))
        
        print("=" * 32)
    print("Battery Level : " + str(adb_test.battery_level) + "%")


