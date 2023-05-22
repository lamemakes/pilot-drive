as a developer...
====================

Developer How-To's for PILOT Drive

create a new service
----------------------

Making a new service has some basic prerequisites to allow for modularity:

#. It has it's own module within the ``backend/pilot-drive/services/`` directory (requiring an ``__init__.py``).
#. Within the module, it has a "main" file, with the same name as the module directory.
    - ie. if the service is named "bluetooth" located at backend/pilot-drive/services/bluetooth/, it has a ``bluetooth.py`` main file
#. The service name needs to be added to the ``EventType`` Enum in ``backend/pilot-drive/master_event_queue.py``
#. In the main file, the service inherents the ``AbstractService`` class, located at ``backend/pilot-drive/services/abstract_service.py``.
#. With the ``AbstractService`` as a parent class, the service is required to accept and implement the follow parameters:
    - ``master_event_queue`` - a ``MasterEventQueue`` instance to push new events to
    - ``service_type`` - the ``EventType`` enum value created in step #3, used to identify the service when it pushes to Queue
    - ``logger`` - a ``MasterLogger`` instance to handle logging events
#. The service needs to contain a ``main`` method, that will run as a process upon PILOT Drive's start.
    - The service can either utilize a loop to run until SIGINT, or it can terminate after some work on startup.
#. Each service also needs a ``refresh`` method, which runs on the UI's initial connection, along with refreshes.
    - This might not last long, and most services do not have any logic contained in the refresh. Doesn't work well with multiprocessing.
#. The ``PilotDrive`` located at ``backend/pilot-drive/pd_manager.py`` manager initializes the service
    - This should happen in the ``__init__`` method, using the ``service_factory`` method.
    - *(Optional)* Add a callback for commands sent from the UI by adding a method to ``PilotManager.service_msg_handlers``
#. **Get Creative!**
    - This is where the fun happens! Build your services' logic, and make sure it can be leveraged by the frontend.

**NOTE: Do not use the Python logging module in services, only the provided PILOT Drive Logger!**