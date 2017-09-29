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
from src.util import utils
from src.xexc import InvalidOperatingModeException, InvalidPacketException
from src.packets.aft import ApiFrameType
from src.models.mode import OperatingMode
from src.models.xstatus import DeviceCloudStatus, FrameError
from src.models.xopts import SendDataRequestOptions


class DeviceRequestPacket(XBeeAPIPacket):
    """
    This class represents a device request packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is sent out the serial port when the XBee module receives
    a valid device request from Device Cloud.

    | See:
    |     :class:`.DeviceResponsePacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 5

    def __init__(self, request_id, target=None, request_data=None):
        """
        Class constructor. Instantiates a new :class:`.DeviceRequestPacket` object with the provided parameters.

        Args:
            request_id (Integer): number that identifies the device request. (0 has no special meaning)
            target (String): device request target.
            request_data (Bytearray, optional): data of the request. Optional.

        | Raises:
        |     ValueError:
        |         1. If ``request_id`` is less than 0 or greater than 255.
        |         2. If length of ``target`` is greater than 255.

        | See:
        |     :class:`.XBeeAPIPacket`
        """
        if request_id < 0 or request_id > 255:
            raise ValueError("Device request ID must be between 0 and 255.")

        if target is not None and len(target) > 255:
            raise ValueError("Target length cannot exceed 255 bytes.")

        XBeeAPIPacket.__init__(self, ApiFrameType.DEVICE_REQUEST)
        self.__request_id = request_id
        self.__transport = 0x00  # Reserved.
        self.__flags = 0x00  # Reserved.
        self.__target = target
        self.__request_data = request_data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.DeviceRequestPacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 9. (start delim. + length (2 bytes) + frame type +
                     request id + transport + flags + target length + checksum = 9 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.DEVICE_REQUEST`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=DeviceRequestPacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.DEVICE_REQUEST.code:
            raise InvalidPacketException("This packet is not a device request packet.")

        target_length = raw[7]
        return DeviceRequestPacket(raw[4], str(raw[8:8 + target_length]), raw[8 + target_length:-1])

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return False

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        ret = utils.int_to_bytes(self.__request_id, num_bytes=1)
        ret += utils.int_to_bytes(self.__transport, num_bytes=1)
        ret += utils.int_to_bytes(self.__flags, num_bytes=1)
        if self.__target is not None:
            ret += utils.int_to_bytes(len(self.__target), num_bytes=1)
            ret += bytearray(self.__target, 'utf8')
        else:
            ret += utils.int_to_bytes(0x00, num_bytes=1)
        if self.__request_data is not None:
            ret += self.__request_data

        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.REQUEST_ID: self.__request_id,
                DictKeys.TRANSPORT:  self.__transport,
                DictKeys.FLAGS:      self.__flags,
                DictKeys.TARGET:     self.__target,
                DictKeys.RF_DATA:    list(self.__request_data) if self.__request_data is not None else None}

    def __get_request_id(self):
        """
        Returns the request ID of the packet.

        Returns:
            Integer: the request ID of the packet.
        """
        return self.__request_id

    def __set_request_id(self, request_id):
        """
        Sets the request ID of the packet.

        Args:
            request_id (Integer): the new request ID of the packet. Must be between 0 and 255.

        | Raises:
        |     ValueError: if ``request_id`` is less than 0 or greater than 255.
        """
        if request_id < 0 or request_id > 255:
            raise ValueError("Device request ID must be between 0 and 255.")
        self.__request_id = request_id

    def __get_transport(self):
        """
        Returns the transport of the packet.

        Returns:
            Integer: the transport of the packet.
        """
        return self.__transport

    def __get_flags(self):
        """
        Returns the flags of the packet.

        Returns:
            Integer: the flags of the packet.
        """
        return self.__flags

    def __get_target(self):
        """
        Returns the device request target of the packet.

        Returns:
            String: the device request target of the packet.
        """
        return self.__target

    def __set_target(self, target):
        """
        Sets the device request target of the packet.

        Args:
            target (String): the new device request target of the packet.

        | Raises:
        |     ValueError: if ``target`` length is greater than 255.
        """
        if target is not None and len(target) > 255:
            raise ValueError("Target length cannot exceed 255 bytes.")
        self.__target = target

    def __get_request_data(self):
        """
        Returns the data of the device request.

        Returns:
            Bytearray: the data of the device request.
        """
        if self.__request_data is None:
            return None
        return self.__request_data.copy()

    def __set_request_data(self, request_data):
        """
        Sets the data of the device request.

        Args:
            request_data (Bytearray): the new data of the device request.
        """
        if request_data is None:
            self.__request_data = None
        else:
            self.__request_data = request_data.copy()

    request_id = property(__get_request_id, __set_request_id)
    """Integer. Request ID of the packet."""

    transport = property(__get_transport)
    """Integer. Transport (reserved)."""

    flags = property(__get_flags)
    """Integer. Flags (reserved)."""

    target = property(__get_target, __set_target)
    """String. Request target of the packet."""

    request_data = property(__get_request_data, __set_request_data)
    """Bytearray. Data of the device request."""


class DeviceResponsePacket(XBeeAPIPacket):
    """
    This class represents a device response packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is sent to the serial port by the host in response to the
    :class:`.DeviceRequestPacket`. It should be sent within five seconds to avoid
    a timeout error.

    | See:
    |     :class:`.DeviceRequestPacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 8

    def __init__(self, frame_id, request_id, response_data=None):
        """
        Class constructor. Instantiates a new :class:`.DeviceResponsePacket` object with the provided parameters.

        | Args:
        |     frame_id (Integer): the frame ID of the packet.
        |     request_id (Integer): device Request ID. This number should match the device request ID in the
                                    device request. Otherwise, an error will occur. (0 has no special meaning)
        |     response_data (Bytearray, optional): data of the response. Optional.

        | Raises:
        |     ValueError:
        |         1. If ``frame_id`` is less than 0 or greater than 255.
        |         2. If ``request_id`` is less than 0 or greater than 255.

        | See:
        |     :class:`.XBeeAPIPacket`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255.")
        if request_id < 0 or request_id > 255:
            raise ValueError("Device request ID must be between 0 and 255.")

        XBeeAPIPacket.__init__(self, ApiFrameType.DEVICE_RESPONSE)
        self._frame_id = frame_id
        self.__request_id = request_id
        self.__response_data = response_data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.DeviceResponsePacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 8. (start delim. + length (2 bytes) + frame type +
                     frame id + request id + reserved + checksum = 8 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.DEVICE_RESPONSE`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=DeviceResponsePacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.DEVICE_RESPONSE.code:
            raise InvalidPacketException("This packet is not a device response packet.")

        return DeviceResponsePacket(raw[4], raw[5], raw[7:-1])

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        ret = utils.int_to_bytes(self.__request_id, num_bytes=1)
        ret += utils.int_to_bytes(0x00, num_bytes=1)
        if self.__response_data is not None:
            ret += self.__response_data

        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.REQUEST_ID: self.__request_id,
                DictKeys.RESERVED:   0x00,
                DictKeys.RF_DATA:    list(self.__response_data) if self.__response_data is not None else None}

    def __get_request_id(self):
        """
        Returns the request ID of the packet.

        Returns:
            Integer: the request ID of the packet.
        """
        return self.__request_id

    def __set_request_id(self, request_id):
        """
        Sets the request ID of the packet.

        Args:
            request_id (Integer): the new request ID of the packet. Must be between 0 and 255.

        | Raises:
        |     ValueError: if ``request_id`` is less than 0 or greater than 255.
        """
        if request_id < 0 or request_id > 255:
            raise ValueError("Device request ID must be between 0 and 255.")
        self.__request_id = request_id

    def __get_response_data(self):
        """
        Returns the data of the device response.

        Returns:
            Bytearray: the data of the device response.
        """
        if self.__response_data is None:
            return None
        return self.__response_data.copy()

    def __set_response_data(self, response_data):
        """
        Sets the data of the device response.

        Args:
            response_data (Bytearray): the new data of the device response.
        """
        if response_data is None:
            self.__response_data = None
        else:
            self.__response_data = response_data.copy()

    request_id = property(__get_request_id, __set_request_id)
    """Integer. Request ID of the packet."""

    request_data = property(__get_response_data, __set_response_data)
    """Bytearray. Data of the device response."""


class DeviceResponseStatusPacket(XBeeAPIPacket):
    """
    This class represents a device response status packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is sent to the serial port after the serial port sends a
    :class:`.DeviceResponsePacket`.

    | See:
    |     :class:`.DeviceResponsePacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 7

    def __init__(self, frame_id, status):
        """
        Class constructor. Instantiates a new :class:`.DeviceResponseStatusPacket` object with the provided parameters.

        Args:
            frame_id (Integer): the frame ID of the packet.
            status (:class:`.DeviceCloudStatus`): device response status.

        | Raises:
        |     ValueError: if ``frame_id`` is less than 0 or greater than 255.

        | See:
        |     :class:`.DeviceCloudStatus`
        |     :class:`.XBeeAPIPacket`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255.")

        XBeeAPIPacket.__init__(self, ApiFrameType.DEVICE_RESPONSE_STATUS)
        self._frame_id = frame_id
        self.__status = status

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.DeviceResponseStatusPacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 7. (start delim. + length (2 bytes) + frame type +
                     frame id + device response status + checksum = 7 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.DEVICE_RESPONSE_STATUS`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=DeviceResponseStatusPacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.DEVICE_RESPONSE_STATUS.code:
            raise InvalidPacketException("This packet is not a device response status packet.")

        return DeviceResponseStatusPacket(raw[4], DeviceCloudStatus.get(raw[5]))

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        return utils.int_to_bytes(self.__status.code, num_bytes=1)

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.DC_STATUS: self.__status}

    def __get_status(self):
        """
        Returns the status of the device response packet.

        Returns:
            :class:`.DeviceCloudStatus`: the status of the device response packet.

        | See:
        |     :class:`.DeviceCloudStatus`
        """
        return self.__status

    def __set_status(self, status):
        """
        Sets the status of the device response packet.

        Args:
            status (:class:`.DeviceCloudStatus`): the new status of the device response packet.

        | See:
        |     :class:`.DeviceCloudStatus`
        """
        self.__status = status

    status = property(__get_status, __set_status)
    """:class:`.DeviceCloudStatus`. Status of the device response."""


class FrameErrorPacket(XBeeAPIPacket):
    """
    This class represents a frame error packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is sent to the serial port for any type of frame error.

    | See:
    |     :class:`.FrameError`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 6

    def __init__(self, frame_error):
        """
        Class constructor. Instantiates a new :class:`.FrameErrorPacket` object with the provided parameters.

        Args:
            frame_error (:class:`.FrameError`): the frame error.

        | See:
        |     :class:`.FrameError`
        |     :class:`.XBeeAPIPacket`
        """
        XBeeAPIPacket.__init__(self, ApiFrameType.FRAME_ERROR)
        self.__frame_error = frame_error

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.FrameErrorPacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 6. (start delim. + length (2 bytes) + frame type +
                     frame error + checksum = 6 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.FRAME_ERROR`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=FrameErrorPacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.FRAME_ERROR.code:
            raise InvalidPacketException("This packet is not a frame error packet.")

        return FrameErrorPacket(FrameError.get(raw[4]))

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return False

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        return utils.int_to_bytes(self.__frame_error.code, num_bytes=1)

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.FRAME_ERROR: self.__frame_error}

    def __get_error(self):
        """
        Returns the frame error of the packet.

        Returns:
            :class:`.FrameError`: the frame error of the packet.

        | See:
        |     :class:`.FrameError`
        """
        return self.__frame_error

    def __set_error(self, frame_error):
        """
        Sets the frame error of the packet.

        Args:
            frame_error (:class:`.FrameError`): the new frame error of the packet.

        | See:
        |     :class:`.FrameError`
        """
        self.__frame_error = frame_error

    error = property(__get_error, __set_error)
    """:class:`.FrameError`. Frame error of the packet."""


class SendDataRequestPacket(XBeeAPIPacket):
    """
    This class represents a send data request packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is used to send a file of the given name and type to
    Device Cloud.

    If the frame ID is non-zero, a :class:`.SendDataResponsePacket` will be
    received.

    | See:
    |     :class:`.SendDataResponsePacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 10

    def __init__(self, frame_id, path, content_type, options, file_data=None):
        """
        Class constructor. Instantiates a new :class:`.SendDataRequestPacket` object with the provided parameters.

        Args:
            frame_id (Integer): the frame ID of the packet.
            path (String): path of the file to upload to Device Cloud.
            content_type (String): content type of the file to upload.
            options (:class:`.SendDataRequestOptions`): the action when uploading a file.
            file_data (Bytearray, optional): data of the file to upload. Optional.

        | Raises:
        |     ValueError: if ``frame_id`` is less than 0 or greater than 255.

        | See:
        |     :class:`.XBeeAPIPacket`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255.")

        XBeeAPIPacket.__init__(self, ApiFrameType.SEND_DATA_REQUEST)
        self._frame_id = frame_id
        self.__path = path
        self.__content_type = content_type
        self.__transport = 0x00  # Always TCP.
        self.__options = options
        self.__file_data = file_data

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.SendDataRequestPacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 10. (start delim. + length (2 bytes) + frame type +
                     frame id + path length + content type length + transport + options + checksum = 10 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.SEND_DATA_REQUEST`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=SendDataRequestPacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.SEND_DATA_REQUEST.code:
            raise InvalidPacketException("This packet is not a send data request packet.")

        path_length = raw[5]
        content_type_length = raw[6 + path_length]
        return SendDataRequestPacket(raw[4],
                                     str(raw[6:6 + path_length]),
                                     str(raw[6 + path_length + 1:6 + path_length + 1 + content_type_length]),
                                     SendDataRequestOptions.get(raw[6 + path_length + 2 + content_type_length]),
                                     raw[6 + path_length + 3 + content_type_length:-1])

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        if self.__path is not None:
            ret = utils.int_to_bytes(len(self.__path), num_bytes=1)
            ret += bytearray(self.__path, "utf8")
        else:
            ret = utils.int_to_bytes(0x00, num_bytes=1)
        if self.__content_type is not None:
            ret += utils.int_to_bytes(len(self.__content_type), num_bytes=1)
            ret += bytearray(self.__content_type, "utf8")
        else:
            ret += utils.int_to_bytes(0x00, num_bytes=1)
        ret += utils.int_to_bytes(0x00, num_bytes=1)  # Transport is always TCP
        ret += utils.int_to_bytes(self.__options.code, num_bytes=1)
        if self.__file_data is not None:
            ret += self.__file_data

        return ret

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.PATH_LENGTH:         len(self.__path) if self.__path is not None else 0x00,
                DictKeys.PATH:                self.__path if self.__path is not None else None,
                DictKeys.CONTENT_TYPE_LENGTH: len(self.__content_type) if self.__content_type is not None else 0x00,
                DictKeys.CONTENT_TYPE:        self.__content_type if self.__content_type is not None else None,
                DictKeys.TRANSPORT:           0x00,
                DictKeys.TRANSMIT_OPTIONS:    self.__options,
                DictKeys.RF_DATA:             list(self.__file_data) if self.__file_data is not None else None}

    def __get_path(self):
        """
        Returns the path of the file to upload to Device Cloud.

        Returns:
            String: the path of the file to upload to Device Cloud.
        """
        return self.__path

    def __set_path(self, path):
        """
        Sets the path of the file to upload to Device Cloud.

        Args:
            path (String): the new path of the file to upload to Device Cloud.
        """
        self.__path = path

    def __get_content_type(self):
        """
        Returns the content type of the file to upload.

        Returns:
            String: the content type of the file to upload.
        """
        return self.__content_type

    def __set_content_type(self, content_type):
        """
        Sets the content type of the file to upload.

        Args:
            content_type (String): the new content type of the file to upload.
        """
        self.__content_type = content_type

    def __get_options(self):
        """
        Returns the file upload operation options.

        Returns:
            :class:`.SendDataRequestOptions`: the file upload operation options.

        | See:
        |     :class:`.SendDataRequestOptions`
        """
        return self.__options

    def __set_options(self, options):
        """
        Sets the file upload operation options.

        Args:
            options (:class:`.SendDataRequestOptions`): the new file upload operation options

        | See:
        |     :class:`.SendDataRequestOptions`
        """
        self.__options = options

    def __get_file_data(self):
        """
        Returns the data of the file to upload.

        Returns:
            Bytearray: the data of the file to upload.
        """
        if self.__file_data is None:
            return None
        return self.__file_data.copy()

    def __set_file_data(self, file_data):
        """
        Sets the data of the file to upload.

        Args:
            file_data (Bytearray): the new data of the file to upload.
        """
        if file_data is None:
            self.__file_data = None
        else:
            self.__file_data = file_data.copy()

    path = property(__get_path, __set_path)
    """String. Path of the file to upload to Device Cloud."""

    content_type = property(__get_content_type, __set_content_type)
    """String. The content type of the file to upload."""

    options = property(__get_options, __set_options)
    """:class:`.SendDataRequestOptions`. File upload operation options."""

    file_data = property(__get_file_data, __set_file_data)
    """Bytearray. Data of the file to upload."""


class SendDataResponsePacket(XBeeAPIPacket):
    """
    This class represents a send data response packet. Packet is built
    using the parameters of the constructor or providing a valid API payload.

    This frame type is sent out the serial port in response to the
    :class:`.SendDataRequestPacket`, providing its frame ID is non-zero.

    | See:
    |     :class:`.SendDataRequestPacket`
    |     :class:`.XBeeAPIPacket`
    """

    __MIN_PACKET_LENGTH = 7

    def __init__(self, frame_id, status):
        """
        Class constructor. Instantiates a new :class:`.SendDataResponsePacket` object with the provided parameters.

        Args:
            frame_id (Integer): the frame ID of the packet.
            status (:class:`.DeviceCloudStatus`): the file upload status.

        | Raises:
        |     ValueError: if ``frame_id`` is less than 0 or greater than 255.

        | See:
        |     :class:`.DeviceCloudStatus`
        |     :class:`.XBeeAPIPacket`
        """
        if frame_id < 0 or frame_id > 255:
            raise ValueError("Frame id must be between 0 and 255.")

        XBeeAPIPacket.__init__(self, ApiFrameType.SEND_DATA_RESPONSE)
        self._frame_id = frame_id
        self.__status = status

    @staticmethod
    def create_packet(raw, operating_mode):
        """
        Override method.

        | Returns:
        |     :class:`.SendDataResponsePacket`

        | Raises:
        |     InvalidPacketException:
        |         1. If the bytearray length is less than 10. (start delim. + length (2 bytes) + frame type +
                     frame id + status + checksum = 7 bytes).
        |         2. If the length field of 'raw' is different than its real length. (length field: bytes 2 and 3)
        |         3. If the first byte of 'raw' is not the header byte. See :class:`.SpecialByte`.
        |         4. If the calculated checksum is different than the checksum field value (last byte).
        |         5. If operating_mode mode is not supported.
        |         6. If the frame type is different than :attr:`.ApiFrameType.SEND_DATA_RESPONSE`

        | See:
        |     :meth:`.XBeePacket.create_packet`
        |     :meth:`.XBeeAPIPacket._check_api_packet`
        """
        if operating_mode != OperatingMode.ESCAPED_API_MODE and operating_mode != OperatingMode.API_MODE:
            raise InvalidOperatingModeException(operating_mode.name + " is not supported.")

        raw = XBeeAPIPacket._unescape_data(raw) if operating_mode == OperatingMode.ESCAPED_API_MODE else raw
        XBeeAPIPacket._check_api_packet(raw, min_length=SendDataResponsePacket.__MIN_PACKET_LENGTH)

        if raw[3] != ApiFrameType.SEND_DATA_RESPONSE.code:
            raise InvalidPacketException("This packet is not a send data response packet.")

        return SendDataResponsePacket(raw[4], DeviceCloudStatus.get(raw[5]))

    def needs_id(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket.needs_id`
        """
        return True

    def _get_api_packet_spec_data(self):
        """
        Override method.

        | See:
        |     :meth:`.XBeeAPIPacket._get_api_packet_spec_data`
        """
        return utils.int_to_bytes(self.__status.code, num_bytes=1)

    def _get_api_packet_spec_data_dict(self):
        """
        Override method.

        See:
            :meth:`.XBeeAPIPacket._get_api_packet_spec_data_dict`
        """
        return {DictKeys.DC_STATUS: self.__status}

    def __get_status(self):
        """
        Returns the file upload status.

        Returns:
            :class:`.DeviceCloudStatus`: the file upload status.

        | See:
        |     :class:`.DeviceCloudStatus`
        """
        return self.__status

    def __set_status(self, status):
        """
        Sets the file upload status.

        Args:
            status (:class:`.DeviceCloudStatus`): the new file upload status.

        | See:
        |     :class:`.DeviceCloudStatus`
        """
        self.__status = status

    status = property(__get_status, __set_status)
    """:class:`.DeviceCloudStatus`. The file upload status."""
