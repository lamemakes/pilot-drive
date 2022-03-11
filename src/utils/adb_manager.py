import logging
import os
import re
import subprocess

from src.utils.adb_notification import Notificaton

class AndroidManager:
    def __init__(self):

        # Initial var declarations
        self.log = logging.getLogger()
        self.device_name = None
        self.notifications = {}

        # Initialize ADB
        run_adb_root = "adb root"
        run_root = subprocess.getoutput(run_adb_root)

        self.get_notifications()
        self.get_battery_level()

    # This should run in a thread to update on the side
    def get_notifications(self):
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
                self.notifications.update({key : new_notification})

    def get_battery_level(self):
        dump_battery_cmd = "adb shell dumpsys battery"

        battery_dump = subprocess.getoutput(dump_battery_cmd)

        self.battery_level = int(re.search("level: (.*)\n", battery_dump).group(1))
        

if __name__ == "__main__":
    adb_test = AndroidManager()
    for id in adb_test.notifications:
        for key in adb_test.notifications.get(id).notification_keys:
            print(key + " : " + str(adb_test.notifications.get(id).attributes.get(key)))
        print("=" * 32)
        print("Battery Level : " + str(adb_test.battery_level) + "%")


