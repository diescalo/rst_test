Logging events
==============

Logging is a fundamental part of applications, and every application includes
this feature. A well-designed logging system is a useful utility for system
administrators, developers and the support team and can save valuable time in
sorting through the cause of issues. As users execute programs on the front-end,
the system invisibly builds a vault of event information (log entries) for
system administrators and the support team.

The XBee Python Library uses the Python's standard logging module for
registering logging events. The logger works at module level, that is, there
is a logger with different name for each module that has logger.

The modules that have logging integrated are ``devices`` and ``reader``. By
default, all loggers are disabled. Because of this, you will not see any
logging message in the console if you do not activate them explicitly.

In the XBee Python Library, you need three things to enable the logger:

1. The logger itself.
2. A handler. This will determine if the messages will be displayed in the
   console, written in a file, sent through a socket, etc.
3. A formatter. This will determine the message format. For example, a format
   could be:

    * *Timestamp with the current date - logger name - level (debug, info,
      warning...) - data.*

To retrieve the logger, you have to use the ``get_logger()`` method of the
logging module, providing the name of the logger that you want to get as
parameter. In the XBee Python Library all loggers have the name of the module
they belong to. For example, the name of the logger of the ``devices`` module
is ``digi.xbee.devices``. You can get a module name with the special attribute
``\_\_name\_\_``.

**Retrieving a module name and its logger**

.. code:: python

  import logging

  [...]

  # Get the logger of the devices module.
  dev_logger = logging.getLogger(digi.xbee.devices.__name__)

  # Get the logger of the devices module providing the name.
  dev_logger = logging.getLogger("digi.xbee.devices")

  [...]

To retrieve a Handler, you can use the default Python handler or create your
own one. Depending on which type of handler you use, the messages created by
the logger will be printed in the console, in a file, etc. You can have more
than one handler per logger, this means that you can enable the default XBee
Python Library handler and add your own handlers.

**Retrieving a Handler and adding it to a logger**

.. code:: python

  import logging

  [...]

  # Get the logger of the devices module.
  dev_logger = logging.getLogger(digi.xbee.devices.__name__)

  # Get a handler and add it to the logger.
  handler = logging.StreamHandler()
  dev_logger.addHandler(handler)

  [...]

The previous code snippet shows how to add a handler to a logger, but the
logic way is to add a formatter to a handler, and then add the handler to the
logger.

When you create a formatter, you must specify which information will be printed
and in which format. This guide shows you how to create a formatter with a
simple format. If you want to create more complex formatters or handlers, read
the Python documentation.

**Creating a formatter and adding it to a handler**

.. code:: python

  import logging

  [...]

  # Get a handler.
  handler = (...)

  # Instantiate a formatter so the log entries are represented as defined here.
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                                '%(message)s')

  # Configure the formatter in the handler.
  handler.setFormatter(formatter)

  [...]

**Enabling a logger for the devices module**

.. code:: python

  import logging

  [...]

  # Get the logger of the devices module providing the name.
  dev_logger = logging.getLogger("digi.xbee.devices")

  # Get a handler and configure a formatter for it.
  handler = logging.StreamHandler()
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                                '%(message)s')
  handler.setFormatter(formatter)

  # Add the handler to the logger.
  dev_logger.addHandler(handler)

  [...]


Logging level
-------------

The XBee Python Library also provides a method in the ``utils`` module,
``enable_logger()``, to enable the logger with the default settings. These
settings are:

* Handler: ``StreamHandler``
* Format: *timestamp - logger name - level - message*

+----------------------------------------------+--------------------------------------------------------------------+
| Method                                       | Description                                                        |
+==============================================+====================================================================+
| **enable_logger(name, level=logging.DEBUG)** | Enables the logger.                                                |
|                                              |  - name: the name of the module whose logger you want to activate. |
|                                              |  - level: default ``DEBUG``. The level you want to see.            |
+----------------------------------------------+--------------------------------------------------------------------+

**Enabling a logger**

.. code:: python

  import logging

  [...]

  # Enable the logger in the digi.xbee.devices module with INFO level.
  dev_logger = enable_logger(digi.xbee.devices.__name__, logging.INFO)

  # This is a valid method to do the same, too.
  dev_logger = enable_logger("digi.xbee.devices", logging.INFO)

  [...]

  # Enable the logger in the digi.xbee.devices module with the default level
  # (DEBUG).
  dev_logger = enable_logger("digi.xbee.devices")

  # This is a valid method to do the same, too.
  dev_logger = enable_logger("digi.xbee.devices", logging.DEBUG)

  [...]

.. note::
  For further information about the Python logging module, read the
  `Python logging module official documentation <https://docs.python.org/3/library/logging.html>`_
  or the `Python logging cookbook <https://docs.python.org/3/howto/logging-cookbook.html>`_.
