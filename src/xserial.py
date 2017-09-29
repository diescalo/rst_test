# Copyright 2017 Digi International Inc., All Rights Reserved
#
# This software contains proprietary and confidential information of Digi
# International Inc.  By accepting transfer of this copy, Recipient agrees
# to retain this software in confidence, to prevent disclosure to others,
# and to make no use of this software other than that for which it was
# delivered.  This is an unpublished copyrighted work of Digi International
# Inc.  Except as permitted by federal law, 17 USC 117, copying is strictly
# prohibited.
#
# Restricted Rights Legend
#
# Use, duplication, or disclosure by the Government is subject to
# restrictions set forth in sub-paragraph (c)(1)(ii) of The Rights in
# Technical Data and Computer Software clause at DFARS 252.227-7031 or
# subparagraphs (c)(1) and (2) of the Commercial Computer Software -
# Restricted Rights at 48 CFR 52.227-19, as applicable.
#
# Digi International Inc., 11001 Bren Road East, Minnetonka, MN 55343

from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import enum
import src.xexc


class FlowControl(enum.Enum):
    """
    This class represents all available flow controls.
    """

    NONE = None
    SOFTWARE = 0
    HARDWARE_RTS_CTS = 1
    HARDWARE_DSR_DTR = 2
    UNKNOWN = 99


class XBeeSerialPort(Serial):
    """
    This class extends the functionality of Serial class (PySerial). 

    See:
        _PySerial: http://pyserial.sourceforge.net/
    """

    __DEFAULT_PORT_TIMEOUT = 0.1  # seconds
    __DEFAULT_DATA_BITS = EIGHTBITS
    __DEFAULT_STOP_BITS = STOPBITS_ONE
    __DEFAULT_PARITY = PARITY_NONE
    __DEFAULT_FLOW_CONTROL = FlowControl.SOFTWARE

    def __init__(self, baud_rate, port,
                 data_bits=__DEFAULT_DATA_BITS, stop_bits=__DEFAULT_STOP_BITS, parity=__DEFAULT_PARITY,
                 flow_control=__DEFAULT_FLOW_CONTROL, timeout=__DEFAULT_PORT_TIMEOUT):
        """
        Class constructor. Take the parameter and calls Serial class (PySerial) 
        constructor. The port is immediately opened on object creation, when a 
        port is given. It is not opened when port is ``None`` and a successive call
        to open() will be needed.

        The number of the ports starts at 0. In windows you must pass port 
        number 0 to refer port number 1.

        | See:
        |     _PySerial: http://pyserial.sourceforge.net/
        """
        if flow_control == FlowControl.SOFTWARE:
            Serial.__init__(self, port=port, baudrate=baud_rate,
                            bytesize=data_bits, stopbits=stop_bits, parity=parity, timeout=timeout, xonxoff=True)
        elif flow_control == FlowControl.HARDWARE_DSR_DTR:
            Serial.__init__(self, port=port, baudrate=baud_rate,
                            bytesize=data_bits, stopbits=stop_bits, parity=parity, timeout=timeout, dsrdtr=True)
        elif flow_control == FlowControl.HARDWARE_RTS_CTS:
            Serial.__init__(self, port=port, baudrate=baud_rate,
                            bytesize=data_bits, stopbits=stop_bits, parity=parity, timeout=timeout, rtscts=True)
        else:
            Serial.__init__(self, port=port, baudrate=baud_rate,
                            bytesize=data_bits, stopbits=stop_bits, parity=parity, timeout=timeout)
        self._isOpen = True if port is not None else False

    def read_byte(self):
        """
        Synchronous. Reads one byte from serial port.

        Returns:
            Integer: the read byte.

        | Raises:
        |     TimeoutException: if there is no bytes ins serial port buffer.
        """
        byte = bytearray(self.read(1))
        if len(byte) == 0:
            raise src.xexc.TimeoutException()
        else:
            return byte[0]

    def read_bytes(self, num_bytes):
        """
        Synchronous. Reads the specified number of bytes from the serial port.

        Args:
            num_bytes (Integer): the number of bytes to read.

        Returns:
            Bytearray: the read bytes.

        | Raises:
        |     TimeoutException: if the number of bytes read is less than ``num_bytes``.
        """
        read_bytes = bytearray(self.read(num_bytes))
        if len(read_bytes) != num_bytes:
            raise src.xexc.TimeoutException()
        return read_bytes

    def read_existing(self):
        """
        Asynchronous. Reads all bytes in the serial port buffer. May read 0 bytes.

        Returns:
            Bytearray: the bytes read.
        """
        return bytearray(self.read(self.inWaiting()))

    def get_read_timeout(self):
        """
        Returns the serial port read timeout.

        Returns:
            Integer: read timeout in seconds.
        """
        return self.timeout

    def set_read_timeout(self, read_timeout):
        """
        Sets the serial port read timeout in seconds.

        Args:
            read_timeout (Integer): the new serial port read timeout in seconds.
        """
        self.timeout = read_timeout
