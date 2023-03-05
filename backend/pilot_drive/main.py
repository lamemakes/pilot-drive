import json
from multiprocessing import Process
import constants
import asyncio
import websockets

from MasterEventQueue import MasterEventQueue, EventType
from web import ServeStatic
from services import Settings


class PilotDrive:
    def __init__(self):
        self.master_queue = MasterEventQueue()

        processes = []

        web_server = ServeStatic(constants.STATIC_WEB_PORT, constants.STATIC_WEB_PATH)
        processes.append(web_server)

        self.settings = Settings(master_event_queue=self.master_queue, service_type=EventType.SETTINGS)
        processes.append(self.settings)

        self.process_factory(processes=processes)

        # Set message handlers for your services, ie. if there is a new "settings" type recieved from the websocket, pass it to 
        # settings.set_web_settings as it is a settings change event.
        self.service_msg_handlers = {EventType.SETTINGS.value : self.settings.set_web_settings}

    def process_factory(self, processes: list):
        for process in processes:
            p = Process(target=process.main)
            p.start()

    def handle_message(self, message: str):
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


    async def handler(self, websocket):
        self.settings.refresh() # When the app is initialized/the UI is refreshed, it expects a settings even on the bus.
        while True:
            try:
                if self.master_queue.is_new_event():
                    event = self.master_queue.get()
                    await websocket.send(json.dumps(event))
                message = await websocket.recv()
                self.handle_message(message=message)
            except websockets.ConnectionClosedOK:
                break
    

    async def main(self):
        print("MAIN RUN!") # WA DEBUG
        async with websockets.serve(self.handler, "", constants.WS_PORT):
            print("Starting WebSocket server!") # TODO: Replace with logging!
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    pd = PilotDrive()

    asyncio.run(pd.main())
