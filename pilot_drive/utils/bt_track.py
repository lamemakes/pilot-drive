import logging
from dbus.exceptions import DBusException

class Track:
    def __init__(self, mgr):
        
        self.log = logging.getLogger()

        self.track_obj = {"Track" : None}

        try:
            # Create the initial track object to be used to get info on the track
            for path, iface in mgr.GetManagedObjects().items():
                if "org.bluez.MediaPlayer1" in str(iface):
                    self.track_obj = iface.get("org.bluez.MediaPlayer1")

            self.active_track = False
            self.status = None

            # Set all needed values to be able to pull track metadata when class is instantiated.
            self.get_track()

            if self.active_track:
                if "Status" in str(self.track_obj):
                    self.get_status(self.track_obj)
                # TODO: Implement position
                if "Position" in str(self.track_obj):
                    self.position = ""
                    self.get_position()
        except DBusException as e:
            self.log.error(e)

    def prop_changed(self, iface, changed, invalidated):
        # TODO: Sync volume control here?, seems to be an update field.
        self.log.debug("Track properties updated: " + str(changed.items()))
        if "Title" in str(changed.items()):
            self.get_track(changed)
        if "Status" in str(changed.items()):
            self.get_status(changed)


    def get_track(self, prop_update=None):
        if prop_update:
            self.track_obj = prop_update
        
        track = self.track_obj.get("Track")


        # Confirm the track is not empty (track == None)
        if track:
            self.log.debug("Recieved bluetooth track: " + str(track))
            try:
                # Set values as default to prevent previous values from leaching over if values aren't populated
                self.title = ""
                self.artist = ""
                self.album = ""

                if track.get("Title"):
                # Title formatting, covering all my bases to make sure the title stays on one line (damn features!)
                    if len(track.get("Title")) > 34 and ("feat" in track.get("Title").lower() or "ft" in track.get("Title").lower() or "prod" in track.get("Title").lower()):
                        split_char = None
                        if "(" in track.get("Title"):
                            split_char = "("
                        elif "[" in track.get("Title"):
                            split_char = "["
                        elif "{" in track.get("Title"):
                            split_char = "{"
                        else:
                            if "FEAT" in track.get("Title"):
                                split_char = "FEAT"
                            if "feat" in track.get("Title"):
                                split_char = "feat"
                        
                        if split_char:
                            self.title = track.get("Title").split(split_char)[0]
                        else:
                            self.title = track.get("Title")

                    else:
                        self.title = track.get("Title")
                
                else:
                    self.title = track.get("Title")

                if track.get("Album"):
                # Album formatting
                    if len(track.get("Album")) > 34 and ("feat" in track.get("Album").lower() or "ft" in track.get("Album").lower()):
                        split_char = None
                        if "(" in track.get("Album"):
                            split_char = "("
                        elif "[" in track.get("Album"):
                            split_char = "["
                        elif "{" in track.get("Album"):
                            split_char = "{"
                        else:
                            if "FEAT" in track.get("Album"):
                                split_char = "FEAT"
                            if "feat" in track.get("Album"):
                                split_char = "feat"
                        
                        if split_char:
                            self.album = track.get("Album").split(split_char)[0]
                        else:
                            self.album = track.get("Album")
                        
                    else:
                        self.album = track.get("Album")
                
                else:
                    self.album = track.get("Album")
                    
                # TODO: Implement duration
                self.duration = track.get("Duration")

                if track.get("Artist"):
                    self.artist = track.get("Artist")
                
                self.active_track = True
            except KeyError as e:
                self.log.error("Key Error returned from bt_track.py:", e)

        else:
            self.active_track = False

    def get_status(self, props):
        self.log.error("GET_STATUS: " + str(props.get("Status")))     # WA DEBUG
        self.status = props.get("Status")
        return self.status

    def get_position(self):
        self.position = self.track_obj.get("Position")