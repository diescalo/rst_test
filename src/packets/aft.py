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

from enum import Enum, unique
from src.util import utils


@unique
class ApiFrameType(Enum):
    """
    This enumeration lists all the available frame types used in any XBee protocol.
    
    | Inherited properties:
    |     **name** (String): the name (id) of this ApiFrameType.
    |     **value** (String): the value of this ApiFrameType.
    
    """
    TX_64 = (0x00, "TX (Transmit) Request 64-bit address")
    TX_16 = (0x01, "TX (Transmit) Request 16-bit address")
    REMOTE_AT_COMMAND_REQUEST_WIFI = (0x07, "Remote AT Command Request (Wi-Fi)")
    AT_COMMAND = (0x08, "AT Command")
    TRANSMIT_REQUEST = (0x10, "Transmit Request")
    EXPLICIT_ADDRESSING = (0x11, "Explicit Addressing Command Frame")
    REMOTE_AT_COMMAND_REQUEST = (0x17, "Remote AT Command Request")
    TX_SMS = (0x1F, "TX SMS")
    TX_IPV4 = (0x20, "TX IPv4")
    SEND_DATA_REQUEST = (0x28, "Send Data Request")
    DEVICE_RESPONSE = (0x2A, "Device Response")
    RX_64 = (0x80, "RX (Receive) Packet 64-bit Address")
    RX_16 = (0x81, "RX (Receive) Packet 16-bit Address")
    RX_IO_64 = (0x82, "IO Data Sample RX 64-bit Address Indicator")
    RX_IO_16 = (0x83, "IO Data Sample RX 16-bit Address Indicator")
    REMOTE_AT_COMMAND_RESPONSE_WIFI = (0x87, "Remote AT Command Response (Wi-Fi)")
    AT_COMMAND_RESPONSE = (0x88, "AT Command Response")
    TX_STATUS = (0x89, "TX (Transmit) Status")
    MODEM_STATUS = (0x8A, "Modem Status")
    TRANSMIT_STATUS = (0x8B, "Transmit Status")
    IO_DATA_SAMPLE_RX_INDICATOR_WIFI = (0x8F, "IO Data Sample RX Indicator (Wi-Fi)")
    RECEIVE_PACKET = (0x90, "Receive Packet")
    EXPLICIT_RX_INDICATOR = (0x91, "Explicit RX Indicator")
    IO_DATA_SAMPLE_RX_INDICATOR = (0x92, "IO Data Sample RX Indicator")
    REMOTE_AT_COMMAND_RESPONSE = (0x97, "Remote Command Response")
    RX_SMS = (0x9F, "RX SMS")
    RX_IPV4 = (0xB0, "RX IPv4")
    SEND_DATA_RESPONSE = (0xB8, "Send Data Response")
    DEVICE_REQUEST = (0xB9, "Device Request")
    DEVICE_RESPONSE_STATUS = (0xBA, "Device Response Status")
    FRAME_ERROR = (0xFE, "Frame Error")
    GENERIC = (0xFF, "Generic")

    def __init__(self, code, description):
        self.__code = code
        self.__description = description

    def __get_code(self):
        """
        Returns the code of the ApiFrameType element.

        Returns:
            Integer: the code of the ApiFrameType element.
        """
        return self.__code

    def __get_description(self):
        """
        Returns the description of the ApiFrameType element.

        Returns:
            Integer: the description of the ApiFrameType element.
        """
        return self.__description

    @classmethod
    def get(cls, code):
        """
        Retrieves the api frame type associated to the given ID.

        Args:
            code (Integer): the code of the API frame type to get.

        | Returns:
        |     :class:`.ApiFrameType`: the API frame type associated to the given code or ``None`` if
                                      the given code is not a valid ApiFrameType code.
        """
        try:
            return cls.lookupTable[code]
        except KeyError:
            return None

    code = property(__get_code)
    """Integer. The API frame type code."""

    description = property(__get_description)
    """String. The API frame type description."""


# Dictionary<Integer, ApiFrameType: Used to determine the ApiFrameType from Integer.
ApiFrameType.lookupTable = {x.code: x for x in ApiFrameType}
ApiFrameType.__doc__ += utils.doc_enum(ApiFrameType)