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

from src.packets.base import XBeeAPIPacket, DictKeys
from src.xexc import InvalidOperatingModeException, InvalidPacketException
from src.packets.aft import ApiFrameType
from src.models.mode import OperatingMode
from src.models.xopts import TransmitOptions
from src.util import utils
import re


PATTERN_PHONE_NUMBER = "^\+?\d+$"
"""Pattern used to validate the phone number parameter of SMS packets."""


class RXSMSPacket(XBeeAPIPacket):
    """
    This class represents an RX (Receive) SMS packet. Packet is built 
    using the parameters of the constructor or providing a valid byte array.
    
    | See:
    |     :class:`.TXSMSPacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 25

    def __init__(self, phone_number, data):
        """
        Class constructor. Instantiates a new :class:`.RXSMSPacket` object withe the provided parameters.
        
        Args:
            phone_number (String): phone number of the device that sent the SMS.
            data (String): packet data (text of the SMS).
            
        | Raises:
        |     ValueError:
        |         1. If length of ``phone_number`` is greater than 20.
        |         2. If ``phone_number`` is not a valid phone number.
        """
        if len(phone_number) > 20:
            raise ValueError("Phone number length cannot be greater than 20 bytes")
        if not re.match(PATTERN_PHONE_NUMBER, phone_number):
            raise ValueError("Phone number invalid, only numbers and '+' prefix allowed.")
        XBeeAPIPacket.__init__(self, ApiFrameType.RX_SMS)

        self.__phone_number = bytearray(20)
        self.__phone_number[0:len(phone_number)] = phone_number.encode("utf8")
        self.__data = data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.
        
        Returns:
            :class:`.RXSMSPacket`
            
        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 25. (start delim + lenght (2 bytes) + frame type +
                     phone number (20 bytes) + checksum = 25 bytes)
        |         2. If the length field of ``raw`` is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of ``raw`` is not the header byte. See :class:`.SPECIAL_BYTE`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If _OPERATING_MODE mode is not supported.
        |         6. If the frame type is different than :py:attr:`.ApiFrameType.RX_SMS`
            
        | See:
        |     :meth:`.XBeePacket.create_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")
        
        _raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        
        XBeeAPIPacket._check_api_packet(_raw, min_length=RXSMSPacket.__MIN_PACKET_LENGTH)
        if _raw[3] != ApiFrameType.RX_SMS.code:
            raise InvalidPacketException("This packet is not an RXSMSPacket")

        return RXSMSPacket(_raw[4:23].decode("utf8").replace("\0", ""), _raw[24:-1].decode("utf8"))

    def needs_id(self):
        """
        Override method.
        
        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return False

    def get_phone_number_byte_array(self):
        """
        Returns the phone number byte array.

        Returns:
            Bytearray: phone number of the device that sent the SMS.
        """
        return self.__phone_number

    def __get_phone_number(self):
        """
        Returns the phone number of the device that sent the SMS.

        Returns:
            String: phone number of the device that sent the SMS.
        """
        return self.__phone_number.decode("utf8").replace("\0", "")

    def __set_phone_number(self, phone_number):
        """
        Sets the phone number of the device that sent the SMS.

        Args:
            phone_number (String): the new phone number.

        | Raises:
        |     ValueError:
        |         1. If length of ``phone_number`` is greater than 20.
        |         2. If ``phone_number`` is not a valid phone number.
        """
        if len(phone_number) > 20:
            raise ValueError("Phone number length cannot be greater than 20 bytes")
        if not re.match(PATTERN_PHONE_NUMBER, phone_number):
            raise ValueError("Phone number invalid, only numbers and '+' prefix allowed.")

        self.__phone_number = bytearray(20)
        self.__phone_number[0:len(phone_number)] = phone_number.encode("utf8")

    def __get_data(self):
        """
        Returns the data of the packet (SMS text).

        Returns:
            String: the data of the packet.
        """
        return self.__data

    def __set_data(self, data):
        """
        Sets the data of the packet.

        Args:
            data (String): the new data of the packet.
        """
        self.__data = data

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data`
        """
        ret = bytearray()
        ret += self.__phone_number
        if self.__data is not None:
            ret += self.__data.encode("utf8")
        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data_dict`
        """
        return {DictKeys.PHONE_NUMBER: self.__phone_number,
                DictKeys.RF_DATA:      self.__data}

    phone_number = property(__get_phone_number, __set_phone_number)
    """String. Phone number that sent the SMS."""

    data = property(__get_data, __set_data)
    """String. Data of the SMS."""


class TXSMSPacket(XBeeAPIPacket):
    """
    This class represents a TX (Transmit) SMS packet. Packet is built 
    using the parameters of the constructor or providing a valid byte array.
    
    | See:
    |     :class:`.RXSMSPacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 27

    def __init__(self, frame_id, phone_number, data):
        """
        Class constructor. Instantiates a new :class:`.TXSMSPacket` object with the provided parameters.

        Args:
            frame_id (Integer): the frame ID. Must be between 0 and 255.
            phone_number (String): the phone number.
            data (String): this packet's data.

        | Raises:
        |     ValueError:
        |         1. If ``frame_id`` is not between 0 and 255.
        |         2. If length of ``phone_number`` is greater than 20.
        |         3. If ``phone_number`` is not a valid phone number.

        | See:
        |     :class:`.XBeeAPIPacket`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255")
        if len(phone_number) > 20:
            raise ValueError("Phone number length cannot be greater than 20 bytes")
        if not re.match(PATTERN_PHONE_NUMBER, phone_number):
            raise ValueError("Phone number invalid, only numbers and '+' prefix allowed.")
        XBeeAPIPacket.__init__(self, ApiFrameType.TX_SMS)
        
        self._frame_id = frame_id
        self.__transmit_options = TransmitOptions.NONE.value
        self.__phone_number = bytearray(20)
        self.__phone_number[0:len(phone_number)] = phone_number.encode("utf8")
        self.__data = data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        Returns:
            :class:`.TXSMSPacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 27. (start delim, lenght (2 bytes), frame type, frame id,
                     transmit options, phone number (20 bytes), checksum)
        |         2. If the length field of ``raw`` is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of ``raw`` is not the header byte. See :class:`.SPECIAL_BYTE`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If _OPERATING_MODE mode is not supported.
        |         6. If the frame type is different than :py:attr:`.ApiFrameType.TX_SMS`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")
        
        _raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        
        XBeeAPIPacket._check_api_packet(raw, min_length=TXSMSPacket.__MIN_PACKET_LENGTH)
        if _raw[3] != ApiFrameType.TX_SMS.code:
            raise InvalidPacketException("This packet is not a TXSMSPacket")

        return TXSMSPacket(_raw[4], _raw[6:25].decode("utf8").replace("\0", ""), _raw[26:-1].decode("utf8"))

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def get_phone_number_byte_array(self):
        """
        Returns the phone number byte array.

        Returns:
            Bytearray: phone number of the device that sent the SMS.
        """
        return self.__phone_number

    def __get_phone_number(self):
        """
        Returns the phone number of the transmitter device.

        Returns:
            String: the phone number of the transmitter device.
        """
        return self.__phone_number.decode("utf8").replace("\0", "")

    def __set_phone_number(self, phone_number):
        """
        Sets the phone number of the transmitter device.

        Args:
            phone_number (String): the new phone number.

        | Raises:
        |     ValueError:
        |         1. If length of ``phone_number`` is greater than 20.
        |         2. If ``phone_number`` is not a valid phone number.
        """
        if len(phone_number) > 20:
            raise ValueError("Phone number length cannot be greater than 20 bytes")
        if not re.match(PATTERN_PHONE_NUMBER, phone_number):
            raise ValueError("Phone number invalid, only numbers and '+' prefix allowed.")

        self.__phone_number = bytearray(20)
        self.__phone_number[0:len(phone_number)] = phone_number.encode("utf8")

    def __get_data(self):
        """
        Returns the data of the packet (SMS text).

        Returns:
            Bytearray: packet's data.
        """
        return self.__data

    def __set_data(self, data):
        """
        Sets the data of the packet.

        Args:
            data (Bytearray): the new data of the packet.
        """
        self.__data = data

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data`
        """
        ret = utils.int_to_bytes(self.__transmit_options, num_bytes=1)
        ret += self.__phone_number
        if self.__data is not None:
            ret += self.__data.encode("utf8")
        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        |See:
        |     :meth:`.XBeeAPIPacket._get_API_packet_spec_data_dict`
        """
        return {DictKeys.OPTIONS:      self.__transmit_options,
                DictKeys.PHONE_NUMBER: self.__phone_number,
                DictKeys.RF_DATA:      self.__data}

    phone_number = property(__get_phone_number, __set_phone_number)
    """String. Phone number that sent the SMS."""

    data = property(__get_data, __set_data)
    """String. Data of the SMS."""
