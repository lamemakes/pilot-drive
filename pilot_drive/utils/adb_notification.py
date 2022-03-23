# A class to manage notifications
import re
import pilot_drive.utils.adb_read_icon_db as adb_read_icon_db


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

        self.icon_path = "adb_icons/"

        self.parse_notification(raw_notification)

    def check_null(self, value):
        # Converts null to none if it exists
        if value != "null":
            return value

        return None

    def get_icon(self, pkg, icon_db_path):
        return adb_read_icon_db.readBlobData(pkg, icon_db_path)

    def get_notification_value(self, line):
        if "=" in line:

            # Parse the line to pull the values from the notification dump
            search = re.search('=(.*)\n', line + "\n")
            if search:
                value = search.group(1)

                # Toss out any typing
                if "String (" in value or "SpannableString (" in value or "Icon(" in value:
                    value = re.search('\((.*)\)', value).group(1)
                    
                    if "&^&" in value:
                        value = value.replace("&^&", "\n")
                   

                # Give a null check & send it off!
                return self.check_null(value)       

    def parse_notification(self, raw_notification):
        all_attributes = raw_notification.split("\n")

        iter = 0
        for attribute in all_attributes:
            attribute = attribute.strip()

            for key in self.notification_keys:

                # Iterate through keys and put values...
                if attribute.startswith(key):
                    if key == "android.bigText":
                        # Big text is multi-lined
                        line_count = 1
                        for line in all_attributes[iter:]:
                            if line[-1] == ")":
                                break
                            line_count += 1
                        
                        # Uses " &&" as a newline sequence because the newline char is filtered out later. 
                        attribute = "" + "&^&".join(all_attributes[iter:iter + line_count])

                        iter += line_count

                    
                    # and keep all notification attributes in a dictionary
                    self.attributes.update({key : self.get_notification_value(attribute)})
            
            iter += 1

        if self.attributes.get("icon"):
            self.attributes.update({"icon_path" : self.get_icon(self.attributes.get("opPkg"), "app_icons.db")})
            
            

