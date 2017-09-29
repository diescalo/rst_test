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


class ReceiveOptions(Enum):
    """
    This class lists all the possible options that have been set while
    receiving an XBee packet.

    The receive options are usually set as a bitfield meaning that the
    options can be combined using the '|' operand.
    """

    NONE = 0x00
    """
    No special receive options.
    """

    PACKET_ACKNOWLEDGED = 0x01
    """
    Packet was acknowledged.
    
    Not valid for WiFi protocol.
    """

    BROADCAST_PACKET = 0x02
    """
    Packet was a broadcast packet.
    
    Not valid for WiFi protocol.
    """

    APS_ENCRYPTED = 0x20
    """
    Packet encrypted with APS encryption.
    
    Only valid for ZigBee XBee protocol.
    """

    SENT_FROM_END_DEVICE = 0x40
    """
    Packet was sent from an end device (if known).
    
    Only valid for ZigBee XBee protocol.
    """

ReceiveOptions.__doc__ += utils.doc_enum(ReceiveOptions)


class TransmitOptions(Enum):
    """
    This class lists all the possible options that can be set while 
    transmitting an XBee packet.

    The transmit options are usually set as a bitfield meaning that the options 
    can be combined using the '|' operand.
    
    Not all options are available for all cases, that's why there are different 
    names with same values. In each moment, you must be sure that the option 
    your are going to use, is a valid option in your context.
    """

    NONE = 0x00
    """
    No special transmit options.
    """

    DISABLE_ACK = 0x01
    """
    Disables acknowledgments on all unicasts .

    Only valid for DigiMesh, 802.15.4 and Point-to-multipoint 
    protocols.
    """

    DISABLE_RETRIES_AND_REPAIR = 0x01
    """
    Disables the retries and router repair in the frame .

    Only valid for ZigBee protocol.
    """

    DONT_ATTEMPT_RD = 0x02
    """
    Doesn't attempt Route Discovery .

    Disables Route Discovery on all DigiMesh unicasts.

    Only valid for DigiMesh protocol.
    """

    USE_BROADCAST_PAN_ID = 0x04
    """
    Sends packet with broadcast {@code PAN ID}. Packet will be sent to all 
    devices in the same channel ignoring the {@code PAN ID}.

    It cannot be combined with other options.

    Only valid for 802.15.4 XBee protocol.
    """

    ENABLE_UNICAST_NACK = 0x04
    """
    Enables unicast NACK messages .

    NACK message is enabled on the packet.

    Only valid for DigiMesh 868/900 protocol.
    """

    ENABLE_UNICAST_TRACE_ROUTE = 0x04
    """
    Enables unicast trace route messages .

    Trace route is enabled on the packets.

    Only valid for DigiMesh 868/900 protocol.
    """

    ENABLE_MULTICAST = 0x08
    """
    Enables multicast transmission request.

    Only valid for ZigBee XBee protocol.
    """

    ENABLE_APS_ENCRYPTION = 0x20
    """
    Enables APS encryption, only if {@code EE=1} .

    Enabling APS encryption decreases the maximum number of RF payload 
    bytes by 4 (below the value reported by {@code NP}).

    Only valid for ZigBee XBee protocol.
    """

    USE_EXTENDED_TIMEOUT = 0x40
    """
    Uses the extended transmission timeout .

    Setting the extended timeout bit causes the stack to set the 
    extended transmission timeout for the destination address.

    Only valid for ZigBee XBee protocol.
    """

    POINT_MULTIPOINT_MODE = 0x40
    """
    Transmission is performed using point-to-Multipoint mode. 

    Only valid for DigiMesh 868/900 and Point-to-Multipoint 868/900 
    protocols.
    """

    REPEATER_MODE = 0x80
    """
    Transmission is performed using repeater mode .

    Only valid for DigiMesh 868/900 and Point-to-Multipoint 868/900 
    protocols.
    """

    DIGIMESH_MODE = 0xC0
    """
    Transmission is performed using DigiMesh mode .

    Only valid for DigiMesh 868/900 and Point-to-Multipoint 868/900 
    protocols.
    """

TransmitOptions.__doc__ += utils.doc_enum(TransmitOptions)


class RemoteATCmdOptions(Enum):
    """
    This class lists all the possible options that can be set while transmitting
    a remote AT Command.

    These options are usually set as a bitfield meaning that the options 
    can be combined using the '|' operand.
    """

    NONE = 0x00
    """
    No special transmit options
    """

    DISABLE_ACK = 0x01
    """
    Disables ACK
    """

    APPLY_CHANGES = 0x02
    """
    Applies changes in the remote device.

    If this option is not set, AC command must be sent before changes 
    will take effect.
    """

    EXTENDED_TIMEOUT = 0x40
    """
    Uses the extended transmission timeout

    Setting the extended timeout bit causes the stack to set the extended 
    transmission timeout for the destination address.

    Only valid for ZigBee XBee protocol.
    """

RemoteATCmdOptions.__doc__ += utils.doc_enum(RemoteATCmdOptions)


@unique
class SendDataRequestOptions(Enum):
    """
    Enumerates the different options for the :class:`.SendDataRequestPacket`.
    """
    OVERWRITE = (0, "Overwrite")
    ARCHIVE = (1, "Archive")
    APPEND = (2, "Append")
    TRANSIENT = (3, "Transient data (do not store)")

    def __init__(self, code, description):
        self.__code = code
        self.__description = description

    def __get_code(self):
        """
        Returns the code of the SendDataRequestOptions element.

        Returns:
            Integer: the code of the SendDataRequestOptions element.
        """
        return self.__code

    def __get_description(self):
        """
        Returns the description of the SendDataRequestOptions element.

        Returns:
            String: the description of the SendDataRequestOptions element.
        """
        return self.__description

    @classmethod
    def get(cls, code):
        """
        Returns the send data request option for the given code.

        Args:
            code (Integer): the code of the send data request option to get.

        | Returns:
        |     :class:`.FrameError`: the SendDataRequestOptions with the given code, ``None`` if there is not
                                    any send data request option with the provided code.
        """
        try:
            return cls.lookupTable[code]
        except KeyError:
            return None

    code = property(__get_code)
    """Integer. The send data request option code."""

    description = property(__get_description)
    """String. The send data request option description."""

SendDataRequestOptions.lookupTable = {x.code: x for x in SendDataRequestOptions}
SendDataRequestOptions.__doc__ += utils.doc_enum(SendDataRequestOptions)
