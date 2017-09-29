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

from src.packets.base import *
from src.packets.cellular import *
from src.packets.common import *
from src.packets.devicecloud import *
from src.packets.network import *
from src.packets.raw import *
from src.packets.wifi import *
from src.packets.aft import ApiFrameType
from src.models.mode import OperatingMode


"""
This module provides functionality to build XBee packets from
bytearray returning the appropriate XBeePacket subclass.

All the API and API2 logic is already included so all packet reads are
independent of the XBee operating mode.

Two API modes are supported and both can be enabled using the ``AP``
(API Enable) command::

    API1 - API Without Escapes
    The data frame structure is defined as follows:

      Start Delimiter          Length                   Frame Data                   Checksum
          (Byte 1)            (Bytes 2-3)               (Bytes 4-n)                (Byte n + 1)
    +----------------+  +-------------------+  +--------------------------- +  +----------------+
    |      0x7E      |  |   MSB   |   LSB   |  |   API-specific Structure   |  |     1 Byte     |
    +----------------+  +-------------------+  +----------------------------+  +----------------+
                   MSB = Most Significant Byte, LSB = Least Significant Byte


API2 - API With Escapes
The data frame structure is defined as follows::

      Start Delimiter          Length                   Frame Data                   Checksum
          (Byte 1)            (Bytes 2-3)               (Bytes 4-n)                (Byte n + 1)
    +----------------+  +-------------------+  +--------------------------- +  +----------------+
    |      0x7E      |  |   MSB   |   LSB   |  |   API-specific Structure   |  |     1 Byte     |
    +----------------+  +-------------------+  +----------------------------+  +----------------+
                        \___________________________________  _________________________________/
                                                            \/
                                                Characters Escaped If Needed

                   MSB = Most Significant Byte, LSB = Least Significant Byte


When sending or receiving an API2 frame, specific data values must be
escaped (flagged) so they do not interfere with the data frame sequencing.
To escape an interfering data byte, the byte 0x7D is inserted before
the byte to be escaped XOR'd with 0x20.

The data bytes that need to be escaped:

- ``0x7E`` - Frame Delimiter - :attr:`.SpecialByte.
- ``0x7D`` - Escape
- ``0x11`` - XON
- ``0x13`` - XOFF

The length field has a two-byte value that specifies the number of
bytes that will be contained in the frame data field. It does not include the
checksum field.

The frame data  forms an API-specific structure as follows::

      Start Delimiter          Length                   Frame Data                   Checksum
          (Byte 1)            (Bytes 2-3)               (Bytes 4-n)                (Byte n + 1)
    +----------------+  +-------------------+  +--------------------------- +  +----------------+
    |      0x7E      |  |   MSB   |   LSB   |  |   API-specific Structure   |  |     1 Byte     |
    +----------------+  +-------------------+  +----------------------------+  +----------------+
                                               /                                                 \\
                                              /  API Identifier        Identifier specific data   \\
                                              +------------------+  +------------------------------+
                                              |       cmdID      |  |           cmdData            |
                                              +------------------+  +------------------------------+


The cmdID frame (API-identifier) indicates which API messages
will be contained in the cmdData frame (Identifier-specific data).

To unit_test data integrity, a checksum is calculated and verified on
non-escaped data.

| See:
|     :class:`.XBeePacket`
|     :class:`.OperatingMode`
"""


def build_frame(packet_bytearray, operating_mode=OperatingMode.API_MODE):
    """
    Creates a packet from raw data.
    
    Args:
        packet_bytearray (Bytearray): the raw data of the packet to build.
        operating_mode (:class:`.OperatingMode`): the operating mode in which the raw data has been captured.
    
    | Raises:
    |     NotImplementedError: if the packet defined by the bytearray is not supported.

    | See:
    |     :class:`.OperatingMode`
    """
    frame_type = ApiFrameType.get(packet_bytearray[3])

    if frame_type == ApiFrameType.GENERIC:
        return GenericXBeePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.AT_COMMAND:
        return ATCommPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.AT_COMMAND_RESPONSE:
        return ATCommResponsePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RECEIVE_PACKET:
        return ReceivePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_64:
        return RX64Packet.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_16:
        return RX16Packet.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.REMOTE_AT_COMMAND_REQUEST:
        return RemoteATCommandPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.REMOTE_AT_COMMAND_RESPONSE:
        return RemoteATCommandResponsePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.TRANSMIT_REQUEST:
        return TransmitPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.TRANSMIT_STATUS:
        return TransmitStatusPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.MODEM_STATUS:
        return ModemStatusPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.TX_STATUS:
        return TXStatusPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_IO_16:
        return RX16IOPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_IO_64:
        return RX64IOPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.IO_DATA_SAMPLE_RX_INDICATOR:
        return IODataSampleRxIndicatorPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.EXPLICIT_ADDRESSING:
        return ExplicitAddressingPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.EXPLICIT_RX_INDICATOR:
        return ExplicitRXIndicatorPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.TX_SMS:
        return TXSMSPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.TX_IPV4:
        return TXIPv4Packet.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_SMS:
        return RXSMSPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.RX_IPV4:
        return RXIPv4Packet.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.REMOTE_AT_COMMAND_REQUEST_WIFI:
        return RemoteATCommandWifiPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.SEND_DATA_REQUEST:
        return SendDataRequestPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.DEVICE_RESPONSE:
        return DeviceResponsePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.REMOTE_AT_COMMAND_RESPONSE_WIFI:
        return RemoteATCommandResponseWifiPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.IO_DATA_SAMPLE_RX_INDICATOR_WIFI:
        return IODataSampleRxIndicatorWifiPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.SEND_DATA_RESPONSE:
        return SendDataResponsePacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.DEVICE_REQUEST:
        return DeviceRequestPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.DEVICE_RESPONSE_STATUS:
        return DeviceResponseStatusPacket.create_packet(packet_bytearray, operating_mode)

    elif frame_type == ApiFrameType.FRAME_ERROR:
        return FrameErrorPacket.create_packet(packet_bytearray, operating_mode)

    else:
        raise NotImplementedError("Frame type " + str(frame_type) + " is not supported.")
