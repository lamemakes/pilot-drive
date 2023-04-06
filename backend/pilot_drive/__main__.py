from pilot_drive.PilotDrive import PilotDrive
import signal
import asyncio


def run() -> None:
    """
    The main entrypoint method for PILOT Drive. This initializes the PILOT Drive class in an asyncio event loop.
    """
    pilot_drive = PilotDrive()
    signal.signal(signalnum=signal.SIGINT, handler=pilot_drive.terminate)
    signal.signal(signalnum=signal.SIGTERM, handler=pilot_drive.terminate)

    loop = asyncio.get_event_loop()
    main_task = asyncio.ensure_future(pilot_drive.main())
    for stop_signal in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(stop_signal, main_task.cancel)
    try:
        loop.run_until_complete(main_task)
    finally:
        loop.close()


if __name__ == "__main__":
    run()
