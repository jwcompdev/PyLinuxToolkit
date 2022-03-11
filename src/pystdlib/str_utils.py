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
import uuid as uuid_native

from pystdlib.regex import Patterns
from pystdlib.types import NoneType
from pystdlib.utils import check_argument, InvalidInputError, check_argument_type


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
    if not isinstance(value, str):
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
    if isinstance(value, str):
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


def parse_int(value: str, default: int | float | None = None) -> int:
    """Attempts to parse a string to an int.
    If it fails, returns the default.
    If default is None then ValueError is raised.

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed int, or the default if parsing failed
    :raises ValueError: if parse failed and default is None
    """
    check_argument_type(default, "default", (int, float, NoneType))

    try:
        return int(value)
    except (TypeError, ValueError):
        if default is not None:
            if isinstance(default, int):
                return default
            elif isinstance(default, float):
                return int(default)

        raise


def parse_float(value: str, default: int | float | None = None) -> float:
    """Attempts to parse a string to a float.
    If it fails, returns the default.
    If default is None then ValueError is raised.

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed float, or the default if parsing failed
    :raises ValueError: if parse failed and default is None
    """
    check_argument_type(default, "default", (int, float, NoneType))

    try:
        return float(value)
    except (TypeError, ValueError):
        if default is not None:
            if isinstance(default, float):
                return default
            elif isinstance(default, int):
                return float(default)

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
    """Wraps a character or string around the given string.

    :param value: the string to be wrapped
    :param wrap_char: the character or string used to wrap
    :return: wrapped string or the original string
                if wrap_char is empty
    :raise IllegalArgumentError: if either parameter is not a string
    """
    check_argument_type(value, "value", str)

    check_argument_type(wrap_char, "wrap_char", str)

    return f"{wrap_char}{value}{wrap_char}"


def unwrap(value: str, wrap_char: str) -> str:
    """Unwraps a given string from a character or string.

    :param value: the string to be unwrapped
    :param wrap_char: the character or string used to unwrap
    :return: unwrapped string or the original string if it is not
                quoted properly with the wrap character or string
    :raise IllegalArgumentError: if either parameter is not a string
    """
    check_argument_type(value, "value", str)
    check_argument_type(wrap_char, "wrap_char", str)

    if is_not_blank(value) and is_not_blank(wrap_char):
        if value[0] == wrap_char \
                and value[-1] == wrap_char:
            return value[1:-1]
        elif value[0:len(wrap_char)] == wrap_char \
                and value[-len(wrap_char):] == wrap_char:
            return value[len(wrap_char): -len(wrap_char)]

    return value


def uuid(as_hex: bool = False, seed: int = None) -> str:
    """
    Generates a UUID string (using `uuid.uuid4()`).

    >>> uuid(seed=1234)
    1de9ea66-70d3-4a1f-8735-df5ef7697fb9
    >>> uuid(as_hex=True, seed=1234)
    1de9ea6670d34a1f8735df5ef7697fb9

    :param as_hex: True to return the hex value of the UUID,
    False to get its default representation (default)
    :param seed: an int to use as a seed for the randomness
    :return: an uuid string
    """
    rd = random.Random()

    if isinstance(seed, int):
        rd.seed(seed)

    uid = uuid_native.UUID(int=rd.getrandbits(128), version=4)

    if as_hex:
        return uid.hex

    return str(uid)


def random_string(size: int, seed: int = None) -> str:
    """
    Returns a string of the specified size containing random characters
    (uppercase/lowercase ascii letters and digits).

    >>> random_string(9, seed=1234)
    9XChaf688

    :param size: Desired string size
    :param seed: an int to use as a seed for the randomness
    :return: Random string
    """
    check_argument_type(size, "size", int)
    check_argument(size >= 1, 'size must be >= 1')

    rd = random.Random()

    if isinstance(seed, int):
        rd.seed(seed)

    chars = string.ascii_letters + string.digits
    buffer = [rd.choice(chars) for _ in range(size)]
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
    check_argument_type(byte_count, "byte_count", int)
    check_argument(byte_count >= 1, 'byte_count must be >= 1')

    random_bytes = os.urandom(byte_count)
    hex_bytes = binascii.hexlify(random_bytes)
    hex_string = hex_bytes.decode()

    return hex_string


def reverse(input_string: str) -> str:
    """
    Returns the string with its chars reversed.

    >>> reverse('hello')
    olleh

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
        return not "".__eq__(value.strip())
    except AttributeError:
        return value is not None


def build_repr(self, *args, _to_repr: bool = True, **kwargs) -> str:
    """
    Builds a clear repr string that can be used when overriding
    '__repr__' in classes.

    NOTE: all args and kwargs are by default converted
    to a string using 'str()' or if '_to_repr' is True are
    converted using 'repr()'. If the args or kwargs are already
    a string then no conversion is done.

    :param self: the instance of the class
    :param args: the args that can be used to recreate the instance
    :param _to_repr: if True uses 'repr()' on all args, otherwise
        uses 'str()' on all args
    :param kwargs: the keyword args that can be used to recreate
        the instance
    :return: a clear repr string
    """
    final_args_str = ""

    if len(args) == 1:
        if type(args[0]) is str:
            final_args_str = args[0]
        else:
            if _to_repr:
                final_args_str = repr(args[0])
            else:
                final_args_str = str(args[0])

    elif len(args) > 1:
        for item in args:
            if type(item) is str:
                final_args_str += item + ", "
            else:
                if _to_repr:
                    final_args_str += repr(item) + ", "
                else:
                    final_args_str += str(item) + ", "

    if len(kwargs) >= 1:
        for key, item in kwargs.items():
            if type(item) is str:
                final_args_str += f"{key}={item}, "
            else:
                if _to_repr:
                    final_args_str += f"{key}={repr(item)}, "
                else:
                    final_args_str += f"{key}={str(item)}, "

    final_args_str = final_args_str.rstrip(", ")

    return f"{type(self).__name__}({final_args_str})"
