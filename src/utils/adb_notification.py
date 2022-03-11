# A class to manage notifications
import re
import src.utils.adb_read__icon_db as adb_read__icon_db


class Notificaton:
    def __init__(self, raw_notification):
        
        self.notification_keys = ["key",
                                "pri",
                                "opPkg",
                                "when",
                                "tickerText",
                                "android.title",
                                "android.subText",
                                "android.bigText",
                                "icon"]

        self.known_package_names = {"com.android.messaging" : "Messaging",
                                    "com.spotify.music" : "Spotify",
                                    "com.nordvpn.android" : "NordVPN"}

        self.attributes = {}

        self.icon_path = None

        self.parse_notification(raw_notification)

    def check_null(self, value):
        # Converts null to none if it exists
        if value != "null":
            return value

        return None

    def get_icon(self, pkg, icon_db_path):
        return adb_read__icon_db.readBlobData(pkg, icon_db_path)

    def get_notification_value(self, line):
        if "=" in line:

            # Parse the line to pull the values from the notification dump
            search = re.search('=(.*)\n', line + "\n")
            if search:
                value = search.group(1)

                # Toss out any typing
                if "String (" in value or "SpannableString (" in value or "Icon(" in value:
                    value = re.search('\((.*)\)', value).group(1)   

                # Give a null check & send it off!
                return self.check_null(value)       

    def parse_notification(self, raw_notification):
        all_attributes = raw_notification.split("\n")

        iter = 0
        for attribute in all_attributes:
            attribute = attribute.strip()

            for key in self.notification_keys:
                if key == "android.bigText":
                    # Big text is two lined from what's been seen
                    # attribute = attribute + all_attributes[iter + 1]
                    pass

                if attribute.startswith(key):
                    if "." in key:
                        key = key.split(".")[1]
                    
                    self.attributes.update({key : self.get_notification_value(attribute)})

        print(self.attributes)
        if self.attributes.get("icon"):
            self.icon_path = self.get_icon(self.attributes.get("opPkg"), "app_icons.db")


            # # UGLY conditionals to parse out the notification, no clue how to clean this up and set class attrs at the same time.
            # if attribute.startswith("key"):
            #     self.key = self.get_notification_value(attribute)
            # elif attribute.startswith("pri"):
            #     self.pri = self.get_notification_value(attribute)
            # elif attribute.startswith("opPkg"):
            #     self.opPkg = self.get_notification_value(attribute)
            # elif attribute.startswith("when"):
            #     self.when = self.get_notification_value(attribute)
            # elif attribute.startswith("tickerText"):
            #     self.tickerText = self.get_notification_value(attribute)
            # elif attribute.startswith("android.title"):
            #     self.title = self.get_notification_value(attribute)
            # elif attribute.startswith("android.subText"):
            #     self.subText = self.get_notification_value(attribute)
            # elif attribute.startswith("android.bigText"):
            #     attribute = attribute + all_attributes[iter + 1]
            #     self.bigText = self.get_notification_value(attribute)
            
            iter += 1
            

