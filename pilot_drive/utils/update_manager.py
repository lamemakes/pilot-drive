# TODO: Add better error handling! Rather than returning None an error should be returned an handled.

import requests
import subprocess
import sys
import pilot_drive.utils.sys_utils as sys_utils
import json


class PilotUpdater:
    # Initialize the PlotUpdater object, take in current PILOT version and PyPi project URL.
    def __init__(self, current_version, pypi_url):
        self.current_version = current_version
        self.pypi_url = pypi_url

    # Pull all JSON information and convert it to dict from PyPi
    def get_versions(self, pypi_url):
        if sys_utils.get_network_connection():
            package_info = requests.get(pypi_url).text
            return json.loads(package_info).get("releases")
        else:
            return None

    # Sorts the list of versions and returns the latest
    def get_latest_version(self):
        releases = self.get_versions(self.pypi_url)
        if releases:
            versions = list(releases.keys())
            # Sort by release version
            versions.sort(key = lambda x: [int(y) for y in x.split('.')])
            return versions[-1]
        else:
            return None
    
    def check_update(self):
        releases = self.get_versions(self.pypi_url)
        if releases:
            latest_version = self.get_latest_version()
            if latest_version != self.current_version:
                # The following is a pretty sloppy way of comparing the two semantic versions
                remote_v_local = [latest_version, self.current_version]
                remote_v_local.sort(key = lambda x: [int(y) for y in x.split('.')])
                higher_ver = remote_v_local[-1]
                print("*************" + higher_ver)
                if higher_ver == self.current_version:
                    return {"error" : "current version (v" + self.current_version + ") is higher than remote (v" + latest_version +")!"}
                else:
                    # There is a new update, prompt the user to update
                    self.new_release_info = releases.get(higher_ver)
                    self.new_release_version = higher_ver
                    return {"update" : "a new update has been found: v" + higher_ver + " would you like to update now?"}
            else:
                return {"error" : "PILOT Drive v" + self.current_version + " is up to date!"}
        else:
            return {"error" : "Failed to connect to remote!"}


    # Method to pull in a specified PILOT package
    # TODO: Add path verification
    def pull_package(self, release_info, download_path):
        if download_path[-1] != "/":
            download_path += "/"
        filename = release_info[0].get("filename")
        url = release_info[0].get("url")

        try:
            print("Attempting to pull package...")
            # Make request to pull pypi package
            response = requests.get(url)

            with open(download_path + filename, "wb") as updated_package:   
                updated_package.write(response.content)
            
            return download_path + filename
        except:
            return None

    def update_pilot(self, release_info, update_path):
        package_path = self.pull_package(release_info, update_path)
        if package_path:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_path])
            sys_utils.restart_pilot()
        else:
            return {"error" : "failed to pull package from remote!"}