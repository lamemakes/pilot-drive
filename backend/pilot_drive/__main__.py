"""
The entrypoint for PILOT Drive. This initializes the PilotDrive class, which starts the program.
"""
import signal
import os
import sys
import asyncio
import argparse
from pilot_drive.pilot_drive import PilotDrive
from pilot_drive.installer import Installer

parser = argparse.ArgumentParser(
    prog="pilot-drive", description="An open source vehicle headunit"
)

parser.add_argument(
    "-i",
    "--install",
    action="store_true",
    help="Run the PILOT Drive configuration & installation tool",
)
parser.add_argument(
    "-d",
    "--default",
    action="store_true",
    help="""When used alongside the -i/--install argument,
     uses all preset default values to configure PILOT Drive""",
)


def start() -> None:
    '''
    Entrypoint for PILOT Drive. Handle arguments and determine to run main, or install.
    '''
    if os.geteuid() != 0:
        sys.exit(
            """You need to have root privileges to run PILOT Drive.\n
            Please try again, this time using 'sudo'. Exiting."""
        )
    args = parser.parse_args()
    if args.install is True:
        pilot_drive_install = Installer(use_default=args.default)
        pilot_drive_install.main()


def run() -> None:
    """
    The main entrypoint method for PILOT Drive. This initializes the PILOT Drive class in an
    asyncio event loop.
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
