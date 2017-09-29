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

from ipaddress import IPv4Address
from src.models.mode import OperatingMode
from src.models.xprot import IPProtocol
from src.packets.aft import ApiFrameType
from src.packets.base import XBeeAPIPacket, DictKeys
from src.util import utils
from src.xexc import InvalidOperatingModeException, InvalidPacketException


class RXIPv4Packet(XBeeAPIPacket):
    """
    This class represents an RX (Receive) IPv4 packet. Packet is built 
    using the parameters of the constructor or providing a valid byte array.
    
    | See:
    |     :class:`.TXIPv4Packet`
    |     :class:`.XBeeAPIPacket`
    """
    __MIN_PACKET_LENGTH = 15

    def __init__(self, source_address, dest_port, source_port, ip_protocol, data=None):
        """
        Class constructor. Instantiates a new :class:`.RXIPv4Packet` object with the provided parameters.

        Args:
            source_address (:class:`.IPv4Address`): IPv4 address of the source device.
            dest_port (Integer): destination port number.
            source_port (Integer): source port number.
            ip_protocol (:class:`.IPProtocol`): IP protocol used for transmitted data.
            data (Bytearray, optional): data that is sent to the destination device. Optional.

        | Raises:
        |     ValueError: if ``dest_port`` is less than 0 or greater than 65535 or
        |                 if ``source_port`` is less than 0 or greater than 65535.

        | See:
        |     :class:`.IPProtocol`
        """
        if dest_port < 0 or dest_port > 65535:
            raise ValueError("Destination port must be between 0 and 65535")
        if source_port < 0 or source_port > 65535:
            raise ValueError("Source port must be between 0 and 65535")

        XBeeAPIPacket.__init__(self, ApiFrameType.RX_IPV4)
        self.__source_address = source_address
        self.__dest_port = dest_port
        self.__source_port = source_port
        self.__ip_protocol = ip_protocol
        self.__status = 0  # Reserved
        self.__data = data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.
        
        Returns:
            RXIPv4Packet.

        | Raises:
        |     InvalidPacketException:
        |       1. If the bytearray length is less than 15. (start delim + length (2 bytes) + frame type +
                   source address (4 bytes) + dest port (2 bytes) + source port (2 bytes) + network protocol +
                    status + checksum = 15 bytes)
        |       2. If the length field of ``raw`` is different than its real length. (length field: bytes 2 and 3)
        |       3. If the first byte of ``raw`` is not the header byte. See :class:`.SPECIAL_BYTE`.
        |       4. If the calculated checksum is different than the checksum field value (last byte).
        |       5. If _OPERATING_MODE mode is not supported.
        |       6. If the frame type is not :attr:`ApiFrameType.RX_IPV4`.

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        _raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw

        XBeeAPIPacket._check_api_packet(_raw, min_length=RXIPv4Packet.__MIN_PACKET_LENGTH)

        if _raw[3] != ApiFrameType.RX_IPV4.code:
            raise InvalidPacketException("This packet is not an RXIPv4Packet.")

        return RXIPv4Packet(IPv4Address(bytes(raw[4:8])), utils.bytes_to_int(raw[8:10]),
                            utils.bytes_to_int(raw[10:12]), IPProtocol.get(raw[12]),
                            _raw[14:-1])

    def needs_id(self):
        """
        Override method.
        
        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def __get_source_address(self):
        """
        Returns the IPv4 address of the source device.

        Returns:
            :class:`ipaddress.IPv4Address`: the IPv4 address of the source device.
        """
        return self.__source_address

    def __set_source_address(self, source_address):
        """
        Sets the IPv4 source address.

        Args:
            source_address (:class:`.IPv4Address`): The new IPv4 source address.
        """
        if source_address is not None:
            self.__source_address = source_address

    def __get_dest_port(self):
        """
        Returns the destination port.

        Returns:
            Integer: the destination port.
        """
        return self.__dest_port

    def __set_dest_port(self, dest_port):
        """
        Sets the destination port.

        Args:
            dest_port (Integer): the new destination port.

        | Raises:
        |     ValueError: if ``dest_port`` is less than 0 or greater than 65535.
        """
        if dest_port < 0 or dest_port > 65535:
            raise ValueError("Destination port must be between 0 and 65535")
        self.__dest_port = dest_port

    def __get_source_port(self):
        """
        Returns the source port.

        Returns:
            Integer: the source port.
        """
        return self.__source_port

    def __set_source_port(self, source_port):
        """
        Sets the source port.

        Args:
            source_port (Integer): the new source port.

        | Raises:
        |     ValueError: if ``source_port`` is less than 0 or greater than 65535.
        """
        if source_port < 0 or source_port > 65535:
            raise ValueError("Source port must be between 0 and 65535")
        self.__source_port = source_port

    def __get_ip_protocol(self):
        """
        Returns the IP protocol used for transmitted data.

        Returns:
            :class:`.IPProtocol`: the IP protocol used for transmitted data.
        """
        return self.__ip_protocol

    def __set_ip_protocol(self, ip_protocol):
        """
        Sets the IP protocol used for transmitted data.

        Args:
            ip_protocol (:class:`.IPProtocol`): the new IP protocol.
        """
        self.__ip_protocol = ip_protocol

    def __get_data(self):
        """
        Returns the data of the packet.

        Returns:
            Bytearray: the data of the packet.
        """
        if self.__data is None:
            return self.__data
        return self.__data.copy()

    def __set_data(self, data):
        """
        Sets the data of the packet.

        Args:
            data (Bytearray): the new data of the packet.
        """
        if data is None:
            self.__data = None
        else:
            self.__data = data.copy()

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data`
        """
        ret = bytearray(self.__source_address.packed)
        ret += utils.int_to_bytes(self.__dest_port, num_bytes=2)
        ret += utils.int_to_bytes(self.__source_port, num_bytes=2)
        ret += utils.int_to_bytes(self.__ip_protocol.code, num_bytes=1)
        ret += utils.int_to_bytes(self.__status, num_bytes=1)
        if self.__data is not None:
            ret += self.__data
        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data_dict`
        """
        return {DictKeys.SRC_IPV4_ADDR: "%s (%s)" % (self.__source_address.packed, self.__source_address.exploded),
                DictKeys.DEST_PORT:     self.__dest_port,
                DictKeys.SRC_PORT:      self.__source_port,
                DictKeys.IP_PROTOCOL:   "%s (%s)" % (self.__ip_protocol.code, self.__ip_protocol.description),
                DictKeys.STATUS:        self.__status,
                DictKeys.DATA:          bytearray(self.__data)}

    source_address = property(__get_source_address, __set_source_address)
    """:class:`ipaddress.IPv4Address`. IPv4 address of the source device."""

    dest_port = property(__get_dest_port, __set_dest_port)
    """Integer. Destination port."""

    source_port = property(__get_source_port, __set_source_port)
    """Integer. Source port."""

    ip_protocol = property(__get_ip_protocol, __set_ip_protocol)
    """:class:`.IPProtocol`. IP protocol used in the transmission."""

    data = property(__get_data, __set_data)
    """Bytearray. Data of the packet."""


class TXIPv4Packet(XBeeAPIPacket):
    """
    This class represents an TX (Transmit) IPv4 packet. Packet is built
    using the parameters of the constructor or providing a valid byte array.

    | See:
    |     :class:`.RXIPv4Packet`
    |     :class:`.XBeeAPIPacket`
    """

    OPTIONS_CLOSE_SOCKET = 2
    """This option will close the socket after the transmission."""

    OPTIONS_LEAVE_SOCKET_OPEN = 0
    """This option will leave socket open after the transmission."""

    __MIN_PACKET_LENGTH = 16

    def __init__(self, frame_id, dest_address, dest_port, source_port, ip_protocol, transmit_options, data=None):
        """
        Class constructor. Instantiates a new :class:`.TXIPv4Packet` object with the provided parameters.

        Args:
            frame_id (Integer): the frame ID. Must be between 0 and 255.
            dest_address (:class:`.IPv4Address`): IPv4 address of the destination device.
            dest_port (Integer): destination port number.
            source_port (Integer): source port number.
            ip_protocol (:class:`.IPProtocol`): IP protocol used for transmitted data.
            transmit_options (Integer): the transmit options of the packet.
            data (Bytearray, optional): data that is sent to the destination device. Optional.

        | Raises:
        |     ValueError:
        |         1. If ``frame_id`` is less than 0 or greater than 255.
        |         2. If ``dest_port`` is less than 0 or greater than 65535.
        |         3. If ``source_port`` is less than 0 or greater than 65535.

        | See:
        |     :class:`.IPProtocol`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255")
        if dest_port < 0 or dest_port > 65535:
            raise ValueError("Destination port must be between 0 and 65535")
        if source_port < 0 or source_port > 65535:
            raise ValueError("Source port must be between 0 and 65535")

        XBeeAPIPacket.__init__(self, ApiFrameType.TX_IPV4)
        self._frame_id = frame_id
        self.__dest_address = dest_address
        self.__dest_port = dest_port
        self.__source_port = source_port
        self.__ip_protocol = ip_protocol
        self.__transmit_options = transmit_options
        self.__data = data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        Returns:
            TXIPv4Packet.

        | Raises:
        |     InvalidPacketException:
        |       1. If the bytearray length is less than 16. (start delim + length (2 bytes) + frame type +
                   frame id + dest address (4 bytes) + dest port (2 bytes) + source port (2 bytes) +
                   network protocol + transmit options + checksum = 16 bytes)
        |       2. If the length field of ``raw`` is different than its real length. (length field: bytes 2 and 3)
        |       3. If the first byte of ``raw`` is not the header byte. See :class:`.SPECIAL_BYTE`.
        |       4. If the calculated checksum is different than the checksum field value (last byte).
        |       5. If _OPERATING_MODE mode is not supported.
        |       6. If the frame type is not :attr:`ApiFrameType.TX_IPV4`.

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw

        XBeeAPIPacket._check_api_packet(raw, min_length=TXIPv4Packet.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.TX_IPV4.code:
            raise InvalidPacketException("This packet is not an TXIPv4Packet.")

        return TXIPv4Packet(raw[4], IPv4Address(bytes(raw[5:9])), utils.bytes_to_int(raw[9:11]),
                            utils.bytes_to_int(raw[11:13]), IPProtocol.get(raw[13]),
                            raw[14], raw[15:-1])

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def __get_dest_address(self):
        """
        Returns the IPv4 address of the destination device.

        Returns:
            :class:`ipaddress.IPv4Address`: the IPv4 address of the destination device.
        """
        return self.__dest_address

    def __set_dest_address(self, dest_address):
        """
        Sets the IPv4 destination address.

        Args:
            dest_address (:class:`ipaddress.IPv4Address`): The new IPv4 destination address.
        """
        if dest_address is not None:
            self.__dest_address = dest_address

    def __get_dest_port(self):
        """
        Returns the destination port.

        Returns:
            Integer: the destination port.
        """
        return self.__dest_port

    def __set_dest_port(self, dest_port):
        """
        Sets the destination port.

        Args:
            dest_port (Integer): the new destination port.

        | Raises:
        |     ValueError: if ``dest_port`` is less than 0 or greater than 65535.
        """
        if dest_port < 0 or dest_port > 65535:
            raise ValueError("Destination port must be between 0 and 65535")
        self.__dest_port = dest_port

    def __get_source_port(self):
        """
        Returns the source port.

        Returns:
            Integer: the source port.
        """
        return self.__source_port

    def __set_source_port(self, source_port):
        """
        Sets the source port.

        Args:
            source_port (Integer): the new source port.

        | Raises:
        |     ValueError: if ``source_port`` is less than 0 or greater than 65535.
        """
        if source_port < 0 or source_port > 65535:
            raise ValueError("Source port must be between 0 and 65535")

        self.__source_port = source_port

    def __get_ip_protocol(self):
        """
        Returns the IP protocol used for transmitted data.

        Returns:
            :class:`.IPProtocol`: the IP protocol used for transmitted data.
        """
        return self.__ip_protocol

    def __set_ip_protocol(self, ip_protocol):
        """
        Sets the network protocol used for transmitted data.

        Args:
            ip_protocol (:class:`.IPProtocol`): the new IP protocol.
        """
        self.__ip_protocol = ip_protocol

    def __get_transmit_options(self):
        """
        Returns the transmit options of the packet.

        Returns:
            Integer: the transmit options of the packet.
        """
        return self.__transmit_options

    def __set_transmit_options(self, transmit_options):
        """
        Sets the transmit options bitfield of the packet.

        | Args:
        |     transmit_options (Integer): the new transmit options. Can be
                                          :attr:`OPTIONS_CLOSE_SOCKET` or :attr:`OPTIONS_LEAVE_SOCKET_OPEN`.
        """
        self.__transmit_options = transmit_options

    def __get_data(self):
        """
        Returns the data of the packet.

        Returns:
            Bytearray: the data of the packet.
        """
        return self.__data if self.__data is None else self.__data.copy()

    def __set_data(self, data):
        """
        Sets the data of the packet.

        Args:
            data (Bytearray): the new data of the packet.
        """
        self.__data = None if data is None else data.copy()

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data`
        """
        ret = bytearray(self.__dest_address.packed)
        ret += utils.int_to_bytes(self.__dest_port, num_bytes=2)
        ret += utils.int_to_bytes(self.__source_port, num_bytes=2)
        ret += utils.int_to_bytes(self.__ip_protocol.code)
        ret += utils.int_to_bytes(self.__transmit_options)
        if self.__data is not None:
            ret += self.__data
        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data_dict`
        """
        return {DictKeys.DEST_IPV4_ADDR: "%s (%s)" % (self.__dest_address.packed, self.__dest_address.exploded),
                DictKeys.DEST_PORT:      self.dest_port,
                DictKeys.SRC_PORT:       self.source_port,
                DictKeys.IP_PROTOCOL:    "%s (%s)" % (self.__ip_protocol.code, self.__ip_protocol.description),
                DictKeys.OPTIONS:        self.__transmit_options,
                DictKeys.DATA:           bytearray(self.__data)}

    dest_address = property(__get_dest_address, __set_dest_address)
    """:class:`ipaddress.IPv4Address`. IPv4 address of the destination device."""

    dest_port = property(__get_dest_port, __set_dest_port)
    """Integer. Destination port."""

    source_port = property(__get_source_port, __set_source_port)
    """Integer. Source port."""

    ip_protocol = property(__get_ip_protocol, __set_ip_protocol)
    """:class:`.IPProtocol`. IP protocol."""

    transmit_options = property(__get_transmit_options, __set_transmit_options)
    """Integer. Transmit options."""

    data = property(__get_data, __set_data)
    """Bytearray. Data of the packet."""
