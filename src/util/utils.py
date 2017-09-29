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

import logging


# Number of bits to extract with the mask (__MASK)
__MASK_NUM_BITS = 8

# Bit mask to extract the less important __MAS_NUM_BITS bits of a number.
__MASK = 0xFF


def is_bit_enabled(number, position):
    """
    Returns whether the bit located at ``position`` within ``number`` is enabled or not.

    Args:
        number (Integer): the number to check if a bit is enabled.
        position (Integer): the position of the bit to check if is enabled in ``number``.

    Returns:
        Boolean: ``True`` if the bit located at ``position`` within ``number`` is enabled, ``False`` otherwise.
    """
    return ((number & 0xFFFFFFFF) >> position) & 0x01 == 0x01


def hex_string_to_bytes(hex_string):
    """
    Converts a String (composed by hex. digits) into a bytearray with same digits.
    
    Args:
        hex_string (String): String (made by hex. digits) with "0x" header or not.

    Returns:
        Bytearray: bytearray containing the numeric value of the hexadecimal digits.
        
    Raises:
        ValueError: if invalid literal for int() with base 16 is provided.
    
    Example:
        >>> a = "0xFFFE"
        >>> for i in hex_string_to_bytes(a): print(i)
        255
        254
        >>> print(type(hex_string_to_bytes(a)))
        <type 'bytearray'>
        
        >>> b = "FFFE"
        >>> for i in hex_string_to_bytes(b): print(i)
        255
        254
        >>> print(type(hex_string_to_bytes(b)))
        <type 'bytearray'>
        
    """
    aux = int(hex_string, 16)
    return int_to_bytes(aux)


def int_to_bytes(number, num_bytes=None):
    """
    Converts the provided integer into a bytearray.
    
    If ``number`` has less bytes than ``num_bytes``, the resultant bytearray
    is filled with zeros (0x00) starting at the beginning.
    
    If ``number`` has more bytes than ``num_bytes``, the resultant bytearray
    is returned without changes.
    
    Args:
        number (Integer): the number to convert to a bytearray.
        num_bytes (Integer): the number of bytes that the resultant bytearray will have.

    Returns:
        Bytearray: the bytearray corresponding to the provided number.

    Example:
        >>> a=0xFFFE
        >>> print([i for i in int_to_bytes(a)])
        [255,254]
        >>> print(type(int_to_bytes(a)))
        <type 'bytearray'>
        
    """
    byte_array = bytearray()
    byte_array.insert(0, number & __MASK)
    number >>= __MASK_NUM_BITS
    while number != 0:
        byte_array.insert(0, number & __MASK)
        number >>= __MASK_NUM_BITS

    if num_bytes is not None:
        while len(byte_array) < num_bytes:
            byte_array.insert(0, 0x00)

    return byte_array


def length_to_int(byte_array):
    """
    Calculates the length value for the given length field of a packet.
    Length field are bytes 1 and 2 of any packet.
    
    Args:
        byte_array (Bytearray): length field of a packet.
        
    Returns:
        Integer: the length value.
    
    Raises:
        ValueError: if ``byte_array`` is not a valid length field (it has length distinct than 0).
    
    Example:
        >>> b = bytearray([13,14])
        >>> c = length_to_int(b)
        >>> print("0x%02X" % c)
        0x1314
        >>> print(c)
        4884
    """
    if len(byte_array) != 2:
        raise ValueError("bArray must have length 2")
    return (byte_array[0] << 8) + byte_array[1]


def bytes_to_int(byte_array):
    """
    Converts the provided bytearray in an Integer.
    This integer is result of concatenate all components of ``byte_array``
    and convert that hex number to a decimal number.

    Args:
        byte_array (Bytearray): bytearray to convert in integer.

    Returns:
        Integer: the integer corresponding to the provided bytearray.

    Example:
        >>> x = bytearray([0xA,0x0A,0x0A]) #this is 0xA0A0A
        >>> print(bytes_to_int(x))
        657930
        >>> b = bytearray([0x0A,0xAA])    #this is 0xAAA
        >>> print(bytes_to_int(b))
        2730
    """
    if len(byte_array) == 0:
        return 0
    return int("".join(["%02X" % i for i in byte_array]), 16)


def ascii_to_int(ni):
    """
    Converts a bytearray containing the ASCII code of each number digit in an Integer.
    This integer is result of the number formed by all ASCII codes of the bytearray.
    
    Example:
        >>> x = bytearray( [0x31,0x30,0x30] )   #0x31 => ASCII code for number 1.
                                                #0x31,0x30,0x30 <==> 1,0,0
        >>> print(ascii_to_int(x))
        100
    """
    return int("".join([str(i - 0x30) for i in ni]))


def int_to_ascii(number):
    """
    Converts an integer number to a bytearray. Each element of the bytearray is the ASCII
    code that corresponds to the digit of its position.

    Args:
        number (Integer): the number to convert to an ASCII bytearray.

    Returns:
        Bytearray: the bytearray containing the ASCII value of each digit of the number.

    Example:
        >>> x = int_to_ascii(100)
        >>> print(x)
        100
        >>> print([i for i in x])
        [49, 48, 48]
    """
    return bytearray([ord(i) for i in str(number)])


def int_to_length(number):
    """
    Converts am integer into a bytearray of 2 bytes corresponding to the length field of a
    packet. If this bytearray has length 1, a byte with value 0 is added at the beginning.

    Args:
        number (Integer): the number to convert to a length field.

    Returns:


    Raises:
        ValueError: if ``number`` is less than 0 or greater than 0xFFFF.
        
    Example:
        >>> a = 0
        >>> print(hex_to_string(int_to_length(a)))
        00 00
        
        >>> a = 8
        >>> print(hex_to_string(int_to_length(a)))
        00 08
        
        >>> a = 200
        >>> print(hex_to_string(int_to_length(a)))
        00 C8
        
        >>> a = 0xFF00
        >>> print(hex_to_string(int_to_length(a)))
        FF 00
        
        >>> a = 0xFF
        >>> print(hex_to_string(int_to_length(a)))
        00 FF
    """
    if number < 0 or number > 0xFFFF:
        raise ValueError("The number must be between 0 and 0xFFFF.")
    length = int_to_bytes(number)
    if len(length) < 2:
        length.insert(0, 0)
    return length


def hex_to_string(byte_array):
    """
    Returns the provided bytearray in a pretty string format. All bytes are separated by blank spaces and
    printed in hex format.

    Args:
        byte_array (Byteawway): the bytearray to print in pretty string.

    Returns:
        String: the bytearray formatted in a pretty string.
    """
    return " ".join(["%02X" % i for i in byte_array])


def doc_enum(enum_class, descriptions=None):
    """
    Returns a string with the description of each value of an enumeration.
    
    | Args:
    |     enum_class (Enumeration): the Enumeration to get its values documentation.
    |     descriptions (dictionary): each enumeration's item description. The key is the enumeration element name
                                     and the value is the description.
            
    Returns:
        String: the string listing all the enumeration values and their descriptions.
    """
    tab = " "*4
    data = "\n%s| Values:\n" % tab
    for x in enum_class:
        data += """{:s}| {:s}**{:s}**{:s} {:s}\n""".format(tab, tab, x,
                                                           ":" if descriptions is not None else " =",
                                                           str(x.value) if descriptions is None else descriptions[x])
    return data + "\n"


def enable_logger(name, level=logging.DEBUG):
    """
    Enables a logger with the given name and level.

    Args:
        name (String): name of the logger to enable.
        level (Integer): logging level value.
    
    Assigns a default formatter and a default handler (for console).
    """
    log = logging.getLogger(name)
    log.disabled = False
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-7s - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.setLevel(level)


def disable_logger(name):
    """
    Disables the logger with the give name.

    Args:
        name (String): the name of the logger to disable.
    """
    log = logging.getLogger(name)
    log.disabled = True
