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
class OperatingMode(Enum):
    """
    This class represents all operating modes available.

    | Inherited properties:
    |     **name** (String): the name (id) of this OperatingMode.
    |     **value** (String): the value of this OperatingMode.
    """

    AT_MODE = (0, "AT mode")
    API_MODE = (1, "API mode")
    ESCAPED_API_MODE = (2, "API mode with escaped characters")
    UNKNOWN = (99, "Unknown")

    def __init__(self, code, description):
        self.__code = code
        self.__description = description

    def __get_code(self):
        """
        Returns the code of the OperatingMode element.

        Returns:
            String: the code of the OperatingMode element.
        """
        return self.__code

    def __get_description(self):
        """
        Returns the description of the OperatingMode element.

        Returns:
            String: the description of the OperatingMode element.
        """
        return self.__description

    @classmethod
    def get(cls, code):
        """
        Returns the OperatingMode for the given code.

        Args:
            code (Integer): the code corresponding to the operating mode to get.

        Returns:
            :class:`.OperatingMode`: the OperatingMode with the given code.
        """
        try:
            return cls.lookupTable[code]
        except KeyError:
            return OperatingMode.UNKNOWN

    code = property(__get_code)
    """Integer. The operating mode code."""

    description = property(__get_description)
    """String: The operating mode description."""

OperatingMode.lookupTable = {x.code: x for x in OperatingMode}
OperatingMode.__doc__ += utils.doc_enum(OperatingMode)


@unique
class APIOutputMode(Enum):
    """
    Enumerates the different API output modes. The API output mode establishes
    the way data will be output through the serial interface of an XBee device.

    | Inherited properties:
    |     **name** (String): the name (id) of this OperatingMode.
    |     **value** (String): the value of this OperatingMode.
    """

    NATIVE = (0x00, "Native")
    EXPLICIT = (0x01, "Explicit")
    EXPLICIT_ZDO_PASSTHRU = (0x03, "Explicit with ZDO Passthru")

    def __init__(self, code, description):
        self.__code = code
        self.__description = description

    def __get_code(self):
        """
        Returns the code of the APIOutputMode element.

        Returns:
            String: the code of the APIOutputMode element.
        """
        return self.__code

    def __get_description(self):
        """
        Returns the description of the APIOutputMode element.

        Returns:
            String: the description of the APIOutputMode element.
        """
        return self.__description

    @classmethod
    def get(cls, code):
        """
        Returns the APIOutputMode for the given code.

        Args:
            code (Integer): the code corresponding to the API output mode to get.

        | Returns:
        |     :class:`.OperatingMode`: the APIOutputMode with the given code, ``None`` if there is not an
                                       APIOutputMode with that code.
        """
        try:
            return cls.lookupTable[code]
        except KeyError:
            return None

    code = property(__get_code)
    """Integer. The API output mode code."""

    description = property(__get_description)
    """String: The API output mode description."""

APIOutputMode.lookupTable = {x.code: x for x in APIOutputMode}
APIOutputMode.__doc__ += utils.doc_enum(APIOutputMode)


@unique
class IPAddressingMode(Enum):
    """
    Enumerates the different IP addressing modes.
    """

    DHCP = (0x00, "DHCP")
    STATIC = (0x01, "Static")

    def __init__(self, code, description):
        self.__code = code
        self.__description = description

    def __get_code(self):
        """
        Returns the code of the IPAddressingMode element.

        Returns:
            String: the code of the IPAddressingMode element.
        """
        return self.__code

    def __get_description(self):
        """
        Returns the description of the IPAddressingMode element.

        Returns:
            String: the description of the IPAddressingMode element.
        """
        return self.__description

    @classmethod
    def get(cls, code):
        """
        Returns the IPAddressingMode for the given code.

        Args:
            code (Integer): the code corresponding to the IP addressing mode to get.

        | Returns:
        |     :class:`.IPAddressingMode`: the IPAddressingMode with the given code, ``None`` if there is not an
                                          IPAddressingMode with that code.
        """
        try:
            return cls.lookupTable[code]
        except KeyError:
            return None

    code = property(__get_code)
    """Integer. The IP addressing mode code."""

    description = property(__get_description)
    """String. The IP addressing mode description."""

IPAddressingMode.lookupTable = {x.code: x for x in IPAddressingMode}
IPAddressingMode.__doc__ += utils.doc_enum(IPAddressingMode)
