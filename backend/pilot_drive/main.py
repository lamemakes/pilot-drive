import json
from multiprocessing import Process
import constants
import asyncio
import websockets

from MasterEventQueue import MasterEventQueue, EventType
from web import ServeStatic
from services import Settings, Bluetooth, Vehicle


class PilotDrive:
    def __init__(self):
        self.master_queue = MasterEventQueue()

        self.__processes = []

        web_server = ServeStatic(constants.STATIC_WEB_PORT, constants.STATIC_WEB_PATH)
        self.__processes.append(web_server)

        self.settings = Settings(master_event_queue=self.master_queue, service_type=EventType.SETTINGS)
        self.__processes.append(self.settings)

        self.vehicle = Vehicle(master_event_queue=self.master_queue, service_type=EventType.VEHICLE, obd_port="/dev/pts/4")
        self.__processes.append(self.vehicle)

        self.bluetooth = Bluetooth(master_event_queue=self.master_queue, service_type=EventType.BLUETOOTH)
        self.__processes.append(self.bluetooth)

        self.process_factory(processes=self.__processes)

        # Set message handlers for your services, ie. if there is a new "settings" type recieved from the websocket, pass it to 
        # settings.set_web_settings as it is a settings change event.
        self.service_msg_handlers = {EventType.SETTINGS.value: self.settings.set_web_settings, EventType.BLUETOOTH.value: self.bluetooth.bluetooth_control}

    def process_factory(self, processes: list):
        for process in processes:
            p = Process(target=process.main)
            p.start()


    def refresh(self):
        self.settings.refresh()
        self.bluetooth.refresh()


    def handle_message(self, message: str):
        if message:
            try:
                message_in = json.loads(s=message)
                try:
                    print("")
                    print(message_in)
                    handler = self.service_msg_handlers.get(message_in["type"]) # Get the handler for the message type
                    handler(message_in.get(message_in["type"])) # Pass in the content of the websocket message
                except KeyError:
                    print("Failed to find a service handler for message of type: " + message_in["type"])    # TODO: Replace with logging!
            except json.JSONDecodeError as err:
                print('Failed to decode recieved websocket message: ' + err.msg + ' "' + message_in + '"')  # TODO: Replace with logging!


    async def consumer(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                self.handle_message(message=message)
            except websockets.ConnectionClosedOK:
                    break

    async def producer(self, websocket):
        self.refresh() # When the app is initialized/the UI is refreshed, it expects a settings even on the bus.
        while True:
            try:
                if self.master_queue.is_new_event():
                    event = self.master_queue.get()
                    await websocket.send(json.dumps(event))
                await asyncio.sleep(0.05)
            except websockets.ConnectionClosedOK:
                    break


    async def handler(self, websocket):
        self.settings.refresh() # When the app is initialized/the UI is refreshed, it expects a settings even on the bus.
        await asyncio.gather(self.consumer(websocket=websocket), self.producer(websocket=websocket))
    

    async def main(self):
        print("MAIN RUN!") # WA DEBUG
        async with websockets.serve(self.handler, "", constants.WS_PORT):
            print("Starting WebSocket server!") # TODO: Replace with logging!
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    pd = PilotDrive()

    asyncio.run(pd.main())
