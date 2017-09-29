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


class XBeeException(Exception):
    """
    Generic XBee API exception. This class and its subclasses indicate
    conditions that an application might want to catch.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    pass


class ComunicationException(XBeeException):
    """
    This exception will be thrown when any problem related to the communication 
    with the XBee device occurs.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    pass


class ATCommandException(ComunicationException):
    """
    This exception will be thrown when a response of a packet is not success or OK.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    pass


class ConnectionException(XBeeException):
    """
    This exception will be thrown when any problem related to the connection 
    with the XBee device occurs.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    pass


class XBeeDeviceException(XBeeException):
    """
    This exception will be thrown when any problem related to the XBee device 
    occurs.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    pass


class InvalidConfigurationException(ConnectionException):
    """
    This exception will be thrown when trying to open an interface with an 
    invalid configuration.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "The configuration used to open the interface is invalid."

    def __init__(self, message=__DEFAULT_MESSAGE):
        ConnectionException.__init__(self, msg=message)


class InvalidOperatingModeException(ConnectionException):
    """
    This exception will be thrown if the operating mode is different than 
    *OperatingMode.API_MODE* and *OperatingMode.API_MODE*

    This class have all functionality of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "The operating mode of the XBee device is not supported by the library."

    def __init__(self, message=__DEFAULT_MESSAGE):
        ConnectionException.__init__(self, message)

    @classmethod
    def from_operating_mode(cls, operating_mode):
        """
        Class constructor.

        Args:
            operating_mode (:class:`.OperatingMode`): the operating mode that generates the exceptions.
        """
        return cls("Unsupported operating mode: " + operating_mode.description)


class InvalidPacketException(ComunicationException):
    """
    This exception will be thrown when there is an error parsing an API packet 
    from the input stream.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "The XBee API packet is not properly formed."

    def __init__(self, message=__DEFAULT_MESSAGE):
        ComunicationException.__init__(self, message)


class OperationNotSupportedException(XBeeDeviceException):
    """
    This exception will be thrown when the operation performed is not supported 
    by the XBee device.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "The requested operation is not supported by either the connection interface or " \
                        "the XBee device."

    def __init__(self, message=__DEFAULT_MESSAGE):
        XBeeDeviceException.__init__(self, message)


class TimeoutException(ComunicationException):
    """
    This exception will be thrown when performing synchronous operations and 
    the configured time expires.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "There was a timeout while executing the requested operation."

    def __init__(self, _message=__DEFAULT_MESSAGE):
        ComunicationException.__init__(self)


class TransmitException(ComunicationException):
    """
    This exception will be thrown when receiving a transmit status different 
    than *TransmitStatus.SUCCESS* after sending an XBee API packet.

    All functionality of this class is the inherited of Exception.

    | _Exception: https://docs.python.org/2/library/exceptions.html?highlight=exceptions.exception#exceptions.Exception
    """
    __DEFAULT_MESSAGE = "There was a problem with a transmitted packet response (status not ok)"

    def __init__(self, _message=__DEFAULT_MESSAGE):
        ComunicationException.__init__(self, _message)
