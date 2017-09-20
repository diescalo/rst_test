Logging events
==============

Logging is a fundamental part of applications, and every application includes
this feature. A well-designed logging system is a useful utility for system
administrators, developers and the support team and can save valuable time in
sorting through the cause of issues. As users execute programs at the front
end, the system invisibly builds a vault of event information (log entries)
for system administrators and the support team.

The XBee Python Library uses the Python's standard logging module for
registering logging events. The logger works at module level, that is, there
is a logger with different name for each module that has logger.

The modules that have logging integrated are `devices` and `xreader`. By default,
all loggers are disabled. Because of this, you will not see any logging message
in the console if you do not activate them explicitly.

In the XBee Python Library, you need three things to enable the logger:

1. The logger itself.
2. A handler. This will determine if the messages will be displayed in the
   console, written in a file, sent through a socket, etc.
3. A formatter. This will determine the message format. For example, a format
   could be:
    * _Timestamp with the current date - logger name - level (debug, info,
      warning...) - data_.

To retrieve the logger, you have to use the `get_logger()` method of the
logging module, providing the name of the logger that you want to get as
parameter. In the XBee Python Library all loggers have the name of the module
they belong to. For example, the name of the logger of the `devices` module
is `src.devices`. You can get a module name with the special attribute
\_\_name\_\_.

**Retrieving a module name and its logger**
```python
import logging
import src.devices

[...]

# Get the logger of the devices module.
dev_logger = logging.getLogger(src.devices.__name__)

# Get the logger of the devices module providing the name.
dev_logger = logging.getLogger("src.devices")

[...]
```

To retrieve a Handler, you can use the default Python handler or create your
own one. Depending on which type of handler you use, the messages created by
the logger will be printed in the console, in a file, etc. You can have more
than one handler per logger, this means that you can enable the default XBee
Python Library handler and add your own handlers.

**Retrieving a Handler and adding it to a logger**

.. code:: python

  import logging
  import src.devices

  [...]

  # Get the logger of the devices module.
  dev_logger = logging.getLogger(src.devices.__name__)

  #
  handler = logging.StreamHandler()
  dev_logger.addHandler(handler)

  [...]

.. note:: This is a note

.. warning:: This is a warning
