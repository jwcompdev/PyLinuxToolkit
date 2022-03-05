# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# str_utils.py
# Copyright (C) 2022 JWCompDev <jwcompdev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Contains some basic string utilities."""
from __future__ import annotations

import binascii
import os
import random
import string
from uuid import uuid4

from pystdlib.regex import Patterns
from pystdlib.utils import check_argument, InvalidInputError


def is_boolean(value: str) -> bool:
    """Checks if a string can be converted to a Boolean.

    The following strings are considered true boolean values:
    "true", "t", "yes", "y", "1", "succeeded", "succeed", "enabled".
    The following strings are considered false boolean values:
    "false", "f", "no", "n", "0", "-1", "failed", "fail", "disabled".

    :param value: string to check
    :return: true if string matches a boolean,
                false if it does not match or is None or empty
    """
    if not input or input is None:
        return False

    val = value.lower().strip()

    return val in ("true", "t", "yes", "y", "1",
                   "succeeded", "succeed", "enabled",
                   "false", "f", "no", "n", "0",
                   "failed", "fail", "disabled")


def to_boolean(value: str) -> bool | None:
    """Converts a string to a Boolean.

    The following strings are considered true boolean values:
    "true", "t", "yes", "y", "1", "succeeded", "succeed", "enabled".
    The following strings are considered false boolean values:
    "false", "f", "no", "n", "0", "-1", "failed", "fail", "disabled".

    None is returned if the string does not match a boolean value,
    an empty string or having the value None

    :param value: the string to convert
    :return: the converted boolean,
                None is returned if a match is not found
    """
    if value and value is not None:
        val = value.lower().strip()

        is_true = val in ("true", "t", "yes", "y", "1",
                          "succeeded", "succeed", "enabled")

        is_false = val in ("false", "f", "no", "n", "0",
                           "failed", "fail", "disabled")

        if is_true:
            return True
        if is_false:
            return False

    return None


def parse_int(value: str, default: int = None) -> int:
    """Attempts to parse a string to an int.
    If it fails, returns the default.
    If default is None then ValueError is raised.

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed int, or the default if parsing failed
    :raises ValueError: if parse failed and default is None
    """
    check_argument(isinstance(default, (int, type(None))),
                   "\"default\" must be a int or None!")

    try:
        return int(value)
    except ValueError:
        if default is not None:
            return default

        raise


def parse_float(value: str, default: float = None) -> float:
    """Attempts to parse a string to a float.
    If it fails, returns the default.
    If default is None then ValueError is raised.

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed float, or the default if parsing failed
    :raises ValueError: if parse failed and default is None
    """
    check_argument(isinstance(default, (float, type(None))),
                   "\"default\" must be a float or None!")

    try:
        return float(value)
    except ValueError:
        if default is not None:
            return default

        raise


def strip_ansi_codes(line) -> str:
    """Strips all ansi codes from the specified string.

    :param line: the line to strip_ansi_codes from
    :return: the modified line
    """
    return Patterns.ANSI_BASIC_ESCAPE.sub("", line) \
        .replace("\x1b7", "") \
        .replace("\x1b7r", "") \
        .replace("\x1b8", "") \
        .replace("\x1b8r", "")


def wrap(value: str, wrap_char: str) -> str:
    """Wraps a character around the given string .

    :param value: the string to be wrapped
    :param wrap_char: the character used to wrap
    :return: wrapped string or the original string
                if wrap_char is empty
    """
    if not wrap_char:
        return value

    return f"{wrap_char}{value}{wrap_char}"


def unwrap(value: str, wrap_char: str) -> str:
    """Unwraps a given string from a character.

    :param value: the string to be unwrapped
    :param wrap_char: the character used to unwrap
    :return: unwrapped string or the original string if it is not
                quoted properly with the wrap character
    """
    if str and wrap_char and \
            value[0] == wrap_char and \
            value[-1] == wrap_char:
        return value[1:-1]

    return value


def uuid(as_hex: bool = False) -> str:
    """
    Generated a UUID string (using `uuid.uuid4()`).
    *Examples:*

    >>> uuid() # possible output: '3917ea5e-86bd-430a-a1c8-54cd27085e01'
    >>> uuid(as_hex=True) # possible output: '3917ea5e86bd430aa1c854cd27085e01'

    :param as_hex: True to return the hex value of the UUID,
    False to get its default representation (default).
    :return: uuid string.
    """
    uid = uuid4()

    if as_hex:
        return uid.hex

    return str(uid)


def random_string(size: int) -> str:
    """
    Returns a string of the specified size containing random characters
    (uppercase/lowercase ascii letters and digits).

    >>> random_string(9) # possible output: "J1Mna4oY6"

    :param size: Desired string size
    :type size: int
    :return: Random string
    """
    if not isinstance(size, int) or size < 1:
        raise ValueError('size must be >= 1')

    chars = string.ascii_letters + string.digits
    buffer = [random.choice(chars) for _ in range(size)]
    out = ''.join(buffer)

    return out


def secure_random_hex(byte_count: int) -> str:
    """
    Generates a random string using secure low level random generator
    (os.urandom).

    **Bear in mind**: due to hex conversion, the returned string will
    have a size that is exactly the double of the given `byte_count`.

    >>> secure_random_hex(9) # possible output: 'aac4cf1d1d87bd5036'

    :param byte_count: Number of random bytes to generate
    :type byte_count: int
    :return: Hexadecimal string representation of generated random bytes
    """
    if not isinstance(byte_count, int) or byte_count < 1:
        raise ValueError('byte_count must be >= 1')

    random_bytes = os.urandom(byte_count)
    hex_bytes = binascii.hexlify(random_bytes)
    hex_string = hex_bytes.decode()

    return hex_string


def reverse(input_string: str) -> str:
    """
    Returns the string with its chars reversed.
    *Example:*
    >>> reverse('hello') # returns 'olleh'
    :param input_string: String to revert.
    :type input_string: str
    :return: Reversed string.
    """
    if not isinstance(input_string, str):
        raise InvalidInputError(input_string)

    return input_string[::-1]


def is_empty(value: str):
    """
    Returns True if the specified string is empty.

    :param value: the string to check
    :return: True if the specified string is empty
    """
    return "".__eq__(value)


def is_not_empty(value: str):
    """
    Returns True if the specified string is not empty.

    :param value: the string to check
    :return: True if the specified string is not empty
    """
    return not "".__eq__(value)


def is_blank(value: str):
    """
    Returns True if the specified string is whitespace or empty.

    :param value: the string to check
    :return: True if the specified string is whitespace or empty
    """
    try:
        return "".__eq__(value.strip())
    except AttributeError:
        return False


def is_not_blank(value: str):
    """
    Returns True if the specified string is not whitespace or empty.

    :param value: the string to check
    :return: True if the specified string is not whitespace or empty
    """
    try:
        return not "".__eq__(value.strip())
    except AttributeError:
        return True


def is_blank_or_none(value: str):
    """
    Returns True if the specified string is whitespace, empty or None.

    :param value: the string to check
    :return: True if the specified string is whitespace, empty or None
    """
    try:
        return "".__eq__(value.strip())
    except AttributeError:
        return value is None


def is_not_blank_or_none(value: str):
    """
    Returns True if the specified string is not whitespace, empty or None.

    :param value: the string to check
    :return: True if the specified string is not whitespace, empty or None
    """
    try:
        return "".__eq__(value.strip())
    except AttributeError:
        return value is not None
