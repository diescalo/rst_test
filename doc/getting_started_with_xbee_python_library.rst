Getting started with XBee Python library
========================================

This getting started guide describes how to set up your environment and use
the XBee Python Library to communicate with your XBee devices. It explains
how to configure your modules and write your first XBee Python application.

The guide is split in 3 main sections:

* :ref:`gsgInstall`
* :ref:`gsgConfigure`
* :ref:`gsgRunApp`


.. _gsgInstall:

Installing your software
------------------------

The following software components are required to write and run your first
XBee Python application:

* :ref:`gsgInstallPython3`
* :ref:`gsgInstallPySerial3`
* :ref:`gsgInstallXBeePythonLibrarySoftware`
* :ref:`gsgInstallXCTU`


.. _gsgInstallPython3:

Python 3
````````

The Xbee Python library requires Python 3 to work properly. If you don't have
it already installed, you can get it from https://www.python.org/getit/

.. warning::
   At the moment the library is only compatible with Python 3.


.. _gsgInstallPySerial3:

PySerial 3
``````````

Serial communication with the radio modules is something mandatory for library.
For that purpose the XBee Python library uses the **PySerial** module.

The best way to install PySerial is with the
`pip <https://pip.pypa.io/en/stable>`_ tool (which is what Python uses to
install packages). Note, this comes with Python in recent versions. You can
install PySerial running this command in your terminal aplication:

.. code::

  $ pip install pyserial

For further information about the installation of PySerial, refer to the
`PySerial installlation guide
<http://pythonhosted.org/pyserial/pyserial.html#installation>`_.


.. _gsgInstallXBeePythonLibrarySoftware:

XBee Python library software
````````````````````````````

The XBee Python library is also installed with
`pip <https://pip.pypa.io/en/stable>`_. To install the library, simply run this
command in your terminal application:

.. code::

  $ pip install xbee-python-library

It will download and install the library automatically in your Python
interpreter.


Get the source code
*******************

The XBee Python library is actively developed on GitHub, where the code is
`always available <https://github.com/digidotcom/XBeePythonLibrary>`_. You can
clone the repository with:

.. code::

  $ git clone git://github.com/requests/xbee-python-library.git


.. _gsgInstallXCTU:

XCTU
````

XCTU is a free multi-platform application that enables developers to interact
with Digi RF modules through a simple-to-use graphical interface. It includes
new tools that make it easy to set up, configure, and test XBee RF modules.

For instructions on downloading and using XCTU, go to:

http://www.digi.com/xctu

Once you have downloaded XCTU, run the installer and follow the steps to finish
the installation process.

After you load XCTU, a message about software updates appears. We recommend you
always update XCTU to the latest available version.


.. _gsgConfigure:

Configuring your XBee modules
-----------------------------

You need to configure **two XBee devices**. One module (the sender) sends
“Hello XBee World!” using the Python application. The other device (the
receiver) receives the message.

Both devices must be working in the same protocol (802.15.4, ZigBee, DigiMesh,
Point-to-Multipoint, or Wi-Fi) and must be configured to operate in the same
network to enable communication.

.. note::
   If you are getting started with Cellular, you only need to configure one
   device. Cellular protocol devices are connected directly to the Internet,
   so there is not a network of remote devices to communicate with them. For
   the Cellular protocol, the XBee application demonstrated in the getting
   started guide differs from other protocols. The Cellular protocol sends and
   reads data from an echo server.

Use XCTU to configure the devices. Plug the devices into the XBee adapters and
connect them to your computer’s USB or serial ports.

.. note::
   For more information about XCTU, see the embedded help or see the `XCTU User
   Guide <https://www.digi.com/resources/documentation/digidocs/90001458-13>`_.
   You can access the Help Contents from the Help menu of the tool.

Once XCTU is running, add your devices to the tool, and then select them from
the **Radio Modules** section. When XCTU is finished reading the device
parameters, complete the following steps, according to your device type.
Repeat these steps to configure your XBee devices using XCTU.

* :ref:`gsgConfig802devices`
* :ref:`gsgConfigZBdevices`
* :ref:`gsgConfigDMdevices`
* :ref:`gsgConfigDPdevices`
* :ref:`gsgConfigCellulardevices`
* :ref:`gsgConfigWiFidevices`


.. _gsgConfig802devices:

802.15.4 devices
````````````````

#. Click **Load default firmware settings** in the **Radio Configuration**
   toolbar to load the default values for the device firmware.
#. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP**
   parameter value must be **1** (API mode without escapes) or **2** (API mode
   with escapes).
#. Configure **ID** (PAN ID) setting to **CAFE**.
#. Configure **CH** (Channel setting) to **C**.
#. Click **Write radio settings** in the **Radio Configuration** toolbar to
   apply the new values to the module.
#. Once you have configured both modules, check to make sure they can see each
   other. Click **Discover radio modules in the same network**, the second
   button of the device panel in the **Radio Modules** view. The other device
   must be listed in the **Discovering remote devices** dialog.

.. note::
   If the other module is not listed, reboot both devices by pressing the
   **Reset** button of the carrier board and try adding the device again. If
   the list is still empty, go to the corresponding product manual for your
   devices.


.. _gsgConfigZBdevices:

ZigBee devices
``````````````
#. For old ZigBee devices (S2 and S2B), ensure the devices are using
   **API firmware**. The firmware appears in the **Function** label of the
   device in the Radio Modules view.

   * One of the devices must be a coordinator - Function: ZigBee Coordinator
     API
   * We recommend the other one is a router - Function: ZigBee Router AP.

   .. note::
      If any of the two previous conditions is not satisfied, you must change
      the firmware of the device. Click the **Update firmware** button of the
      Radio Configuration toolbar.
#. Click **Load default firmware settings** in the **Radio Configuration**
   toolbar to load the default values for the device firmware.
#. Do the following:

   * If the device has the **AP** parameter, set it to **1** (API mode without
     escapes) or **2** (API mode with escapes).
   * If the device has the **CE** parameter, set it to **Enabled** in the
     coordinator.

#. Configure **ID** (PAN ID) setting to **C001BEE**.
#. Configure **SC** (Scan Channels) setting to **FFF**.
#. Click **Write radio settings** in the **Radio Configuration** toolbar to
   apply the new values to the module.
#. Once you have configured both modules, check to make sure they can see each
   other. Click **Discover radio modules in the same network**, the second
   button of the device panel in the **Radio Modules** view. The other device
   must be listed in the **Discovering remote devices** dialog.

.. note::
   If the other module is not listed, reboot both devices by pressing the
   **Reset** button of the carrier board and try adding the device again. If
   the list is still empty, go to the corresponding product manual for your
   devices.


.. _gsgConfigDMdevices:

DigiMesh devices
````````````````

#. Click **Load default firmware settings** in the **Radio Configuration**
   toolbar to load the default values for the device firmware.
#. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP**
   parameter value must be **1** (API mode without escapes) or **2** (API mode
   with escapes).
#. Configure **ID** (PAN ID) setting to **CAFE**.
#. Configure **CH** (Operating Channel) to **C**.
#. Click **Write radio settings** in the **Radio Configuration** toolbar to
   apply the new values to the module.
#. Once you have configured both modules, check to make sure they can see each
   other. Click **Discover radio modules in the same network**, the second
   button of the device panel in the **Radio Modules** view. The other device
   must be listed in the **Discovering remote devices** dialog.

.. note::
  If the other module is not listed, reboot both devices by pressing the
   **Reset** button of the carrier board and try adding the device again. If
   the list is still empty, go to the corresponding product manual for your
   devices.


.. _gsgConfigDPdevices:

DigiPoint devices
`````````````````

#. Click **Load default firmware settings** in the **Radio Configuration**
   toolbar to load the default values for the device firmware.
#. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP**
   parameter value must be **1** (API mode without escapes) or **2** (API mode
   with escapes).
#. Configure **ID** (PAN ID) setting to **CAFE**.
#. Configure **HP** (Hopping Channel) to **5**.
#. Click **Write radio settings** in the **Radio Configuration** toolbar to
   apply the new values to the module.
#. Once you have configured both modules, check to make sure they can see each
   other. Click **Discover radio modules in the same network**, the second
   button of the device panel in the **Radio Modules** view. The other device
   must be listed in the **Discovering remote devices** dialog.

.. note::
  If the other module is not listed, reboot both devices by pressing the
  **Reset** button of the carrier board and try adding the device again. If
  the list is still empty, go to the corresponding product manual for your
  devices.


.. _gsgConfigCellulardevices:

Cellular devices
````````````````

#. Click **Load default firmware** settings in the Radio Configuration toolbar
   to load the default values for the device firmware.
#. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP**
   parameter value must be **1** (API mode without escapes) or **2** (API mode
   with escapes).
#. Click **Write radio settings** in the Radio Configuration toolbar to apply
   the new values to the module.
#. Verify the module is correctly registered and connected to the Internet.
   To do so check that the LED on the development board blinks. If it is solid
   or has a double-blink, registration has not occurred properly. Registration
   can take several minutes.

.. note::
   In addition to the LED confirmation, you can check the IP address assigned
   to the module by reading the **MY** parameter and verifying it has a value
   different than **0.0.0.0**.


.. _gsgConfigWiFidevices:

Wi-Fi devices
`````````````

#. Click **Load default firmware** settings in the Radio Configuration toolbar
   to load the default values for the device firmware.
#. Ensure the API mode (API1 or API2) is enabled. To do so, the **AP**
   parameter value must be **1** (API mode without escapes) or **2** (API mode
   with escapes).
#. Connect to an access point:

   #. Click the **Active Scan** button.
   #. Select the desired access point from the list of the **Active Scan**
      result dialog.
   #. If the access point requires a password, type your password.
   #. Click the **Connect** button and wait for the module to connect to the
      access point.

#. Click **Write radio settings** in the Radio Configuration toolbar to apply
   the new values to the module.
#. Verify the module is correctly connected to the access point by checking
   the IP address assigned to the module by reading the **MY** parameter and
   verifying it has a value different than **0.0.0.0**.


.. _gsgRunApp:

Run your first XBee Python application
--------------------------------------

The XBee Python application demonstrated in the guide broadcasts the message
*Hello XBee World!* from one of the devices connected to your computer (the
sender) to all remote devices on the same network as the sender one. Once the
message is sent, the receiver XBee module must receive it. XCTU is used to
verify this.

Depending on the protocol of the XBee devices, the commands to be executed
differs from others. Follow the corresponding steps depending on the protocol
of your XBee devices.

* :ref:`gsgAppZBDMDP802`
* :ref:`gsgAppWiFi`
* :ref:`gsgAppCellular`


.. _gsgAppZBDMDP802:

ZigBee, DigiMesh, DigiPoint or 802.15.4 devices
```````````````````````````````````````````````

Follow these steps to send the broadcast message and verify that it is received
successfully:

#. The first step is to prepare the *receiver* XBee device in XCTU to verify
   that the broadcast message sent by the *sender* device is received
   successfully. Follow these steps to do so:

   #. Launch XCTU.
   #. Add the *receiver* module to XCTU.
   #. Click **Open the serial connection with the radio module** to switch to
      **Consoles working mode** and open the serial connection. This allows
      you to see the data when it is received.

#. Open the Python interpreter and write the application commands.

   #. Import the ``XBeeDevice`` class by executing the following command:

      .. code::

        > from src.devices import XBeeDevice

   #. Instantiate a generic XBee device:

      .. code::

        > device = XBeeDevice("COM1", 9600)

      .. note::
         Remember to replace the COM port by the one your *sender* XBee device
         is connected to.

   #. Initialize the XBee device:

      .. code::

        > device.init()

   #. Send the *Hello XBee World!* broadcast message.

      .. code::

        > device.send_data_broadcast("Hello XBee World!".encode("utf8"))

   #. Finalize the connection with the device:

      .. code::

        > device.finalize()

#. Verify that the message is received by the *receiver* XBee in XCTU. An
   **RX (Receive) frame** should be displayed in the **Console log** with the
   following information:

   +--------------------------+----------------------------------------------------+
   | Start delimiter          | 7E                                                 |
   +--------------------------+----------------------------------------------------+
   | Length                   | Depends on the XBee protocol                       |
   +--------------------------+----------------------------------------------------+
   | Frame type               | Depends on the XBee protocol                       |
   +--------------------------+----------------------------------------------------+
   | 16/64-bit source address | XBee sender's 16/64-bit address                    |
   +--------------------------+----------------------------------------------------+
   | Options                  | 02                                                 |
   +--------------------------+----------------------------------------------------+
   | RF data/Received data    | 48 65 6C 6C 6F 20 58 42 65 65 20 57 6F 72 6C 64 21 |
   +--------------------------+----------------------------------------------------+


.. _gsgAppWiFi:

Wi-Fi devices
`````````````

Wi-Fi devices send broadcast data using the ``send_ip_data_broadcast()``
command instead of the ``send_data_broadcast()`` one. For that reason, it is
necessary to instantiate a ``WiFiDevice`` instead of a generic ``XBeeDevice``
to execute the proper command.

Follow these steps to send the broadcast message and verify that it is received
successfully:

#. The first step is to prepare the *receiver* XBee device in XCTU to verify
   that the broadcast message sent by the *sender* device is received
   successfully by the *receiver* one.

   #. Launch XCTU.
   #. Add the *receiver* module to XCTU.
   #. Click **Open the serial connection with the radio module** to switch to
      **Consoles working mode** and open the serial connection. This allows
      you to see the data when it is received.

#. Open the Python interpreter and write the application commands.

   #. Import the ``WiFiDevice`` class by executing the following command:

      .. code::

        > from src.devices import WiFiDevice

   #. Instantiate a Wi-Fi XBee device:

      .. code::

        > device = WiFiDevice("COM1", 9600)

      .. note::
         Remember to replace the COM port by the one your *sender* XBee device
         is connected to.

   #. Initialize the Wi-Fi device:

      .. code::

        > device.init()

   #. Send the *Hello XBee World!* broadcast message.

      .. code::

        > device.send_ip_data_broadcast(9750, "Hello XBee World!".encode("utf8"))

   #. Finalize the connection with the device:

      .. code::

        > device.finalize()

#. Verify that the message is received by the *receiver* XBee in XCTU. An
   **RX IPv4 frame** should be displayed in the **Console log** with the
   following information:

   +---------------------+----------------------------------------------------+
   | Start delimiter     | 7E                                                 |
   +---------------------+----------------------------------------------------+
   | Length              | 00 1C                                              |
   +---------------------+----------------------------------------------------+
   | Frame type          | B0                                                 |
   +---------------------+----------------------------------------------------+
   | IPv4 source address | XBee Wi-Fi sender's IP address                     |
   +---------------------+----------------------------------------------------+
   | 16-bit dest port    | 26 16                                              |
   +---------------------+----------------------------------------------------+
   | 16-bit source port  | 26 16                                              |
   +---------------------+----------------------------------------------------+
   | Protocol            | 00                                                 |
   +---------------------+----------------------------------------------------+
   | Status              | 00                                                 |
   +---------------------+----------------------------------------------------+
   | RF data             | 48 65 6C 6C 6F 20 58 42 65 65 20 57 6F 72 6C 64 21 |
   +---------------------+----------------------------------------------------+


.. _gsgAppCellular:

Cellular devices
````````````````

Cellular devices are connected directly to the Internet, so there is no
network of remote devices to communicate with them. For the Cellular
protocol, the application demonstrated in this guide differs from other
protocols.

The application sends and reads data from an echo server. Follow these steps to
execute it:

#. Open the Python interpreter and write the application commands.

   #. Import the ``CellularDevice``, ``IPv4Address`` and ``IPPrototcol``
      classes:

      .. code::

        > from src.devices import CellularDevice
        > from ipaddress import IPv4Address
        > from src.models.xprot import IPProtocol

   #. Instantiate a Cellular XBee device:

      .. code::

        > device = CellularDevice("COM1", 9600)

      .. note::
         Remember to replace the COM port by the one your Cellular XBee device
         is connected to.

   #. Initialize the Cellular device:

      .. code::

        > device.init()

   #. Send the *Hello XBee World!* message to the echo server with IP
      *52.43.121.77* and port *11001* using the *TCP IP* protocol.

      .. code::

        > device.send_ip_data(IPv4Address("52.43.121.77"), 11001, IPProtocol.TCP, "Hello XBee World!".encode("utf8"))

   #. Read and print the response from the echo server. If response cannot be
      received, print *ERROR*.

      .. code::

        > ip_message = device.read_ip_data()
        > print(ip_message.data.decode("utf8")) if ip_message is not None else "ERROR"

   #. Finalize the connection with the device:

      .. code::

        > device.finalize()
