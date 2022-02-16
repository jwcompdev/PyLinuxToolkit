# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# Utils.py
# Copyright (C) 2022 JWCompDev <jwcompdev@outlook.com>
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
"""
This file contains some basic utilities.
"""
from __future__ import annotations

import datetime
import math
from typing import Any, NoReturn

from pylinuxtoolkit.utils.Exceptions import IllegalArgumentError
from pylinuxtoolkit.utils.RegEx import Patterns


########################################
# Check Value Utils                    #
########################################

def check_argument(expression: bool, error_message="Invalid argument specified!") -> NoReturn:
    """Ensures the truth of an expression involving one or
    more parameters to the calling method.

    :param expression: a boolean expression
    :param error_message: the exception message to use if the
                check fails; will be converted to a string
    :raises IllegalArgumentError: if expression is False
    """

    if not expression:
        raise IllegalArgumentError(str(error_message))


def check_argument_not_none(reference, error_message) -> Any:
    """Ensures that reference is not None, raising an
    IllegalArgumentError with a custom message otherwise.

    :param reference: the object to verify
    :param error_message: the exception message to use if the check
                            fails; will be converted to a string
    :return: reference, guaranteed to be not None, for convenience
    :raises IllegalArgumentError: if reference is None
    """

    check_argument(reference is not None, error_message)
    return reference


def check_argument_not_none_or_empty(reference, error_message) -> Any:
    """Ensures that reference is not None and non-empty,
    throwing an IllegalArgumentError with a custom message otherwise.

    :param reference: the object to verify
    :param error_message: the exception message to use if the
                            check fails; will be converted to a string
    :return: reference, guaranteed to be not None and non-empty, for convenience
    """

    check_argument(reference is not None and len(reference) != 0, error_message)
    return reference


########################################
# String Utils                         #
########################################

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

    if val == "true" \
            or val == "t" \
            or val == "yes" \
            or val == "y" \
            or val == "1" \
            or val == "succeeded" \
            or val == "succeed" \
            or val == "enabled" \
            or val == "false" \
            or val == "f" \
            or val == "no" \
            or val == "n" \
            or val == "0" \
            or val == "-1" \
            or val == "failed" \
            or val == "fail" \
            or val == "disabled":
        return True
    else:
        return False


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

    if not value or value is None:
        return None

    val = value.lower().strip()

    if val == "true" \
            or val == "t" \
            or val == "yes" \
            or val == "y" \
            or val == "1" \
            or val == "succeeded" \
            or val == "succeed" \
            or val == "enabled":
        return True
    elif val == "false" \
            or val == "f" \
            or val == "no" \
            or val == "n" \
            or val == "0" \
            or val == "-1" \
            or val == "failed" \
            or val == "fail" \
            or val == "disabled":
        return False
    else:
        return None


def parse_int_or_default(value: str, default: int) -> int:
    """Attempts to parse a string to an int.
    If it fails, returns the default

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed int, or the default if parsing failed
    """

    check_argument(isinstance(default, int), "\"default\" must be a int!")

    try:
        return int(value)
    except ValueError:
        return default


def parse_float_or_default(value: str, default: float) -> float:
    """Attempts to parse a string to a float.
    If it fails, returns the default

    :param value: the string to parse
    :param default: the value to return if parsing fails
    :return: the parsed float, or the default if parsing failed
    """

    check_argument(isinstance(default, float), "\"default\" must be a float!")

    try:
        return float(value)
    except ValueError:
        return default


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

    if not str or not wrap_char:
        return value
    elif value[0] == wrap_char and value[-1] == wrap_char:
        return value[1:-1]


########################################
# Integer Utils                        #
########################################

def convert_bytes_to_string(number: int) -> str:
    """Returns the conversion from bytes to the correct
    version (1024 bytes = 1 KB) as a string.

    :param number: number to convert to a readable string
    :return: the specified number converted to a readable string
    """
    factor = 1024
    if number >= factor:
        number /= factor
        if number >= factor:
            number /= factor
            if number >= factor:
                number /= factor
                if number >= factor:
                    number /= factor
                    if number >= factor:
                        number /= factor
                        suffix = " PB"
                    else:
                        suffix = " TB"
                else:
                    suffix = " GB"
            else:
                suffix = " MB"
        else:
            suffix = " KB"
    else:
        suffix = " Bytes"

    rounding_factor = 10 ** 2
    rounded = math.floor(number * rounding_factor) / rounding_factor
    return f"{rounded:.2f}" + suffix


########################################
# Other Utils                          #
########################################

def timesince(dt: datetime.datetime | datetime.timedelta,
              default: str = 'just now') -> str:
    """
    Returns string representing 'time since' e.g.
    3 days ago, 5 hours ago etc.

    >>> now = datetime.datetime.now()
    >>> timesince(now)
    'just now'
    >>> timesince(now - datetime.timedelta(seconds=1))
    '1 second ago'
    >>> timesince(now - datetime.timedelta(seconds=2))
    '2 seconds ago'
    >>> timesince(now - datetime.timedelta(seconds=60))
    '1 minute ago'
    >>> timesince(now - datetime.timedelta(seconds=61))
    '1 minute and 1 second ago'
    >>> timesince(now - datetime.timedelta(seconds=62))
    '1 minute and 2 seconds ago'
    >>> timesince(now - datetime.timedelta(seconds=120))
    '2 minutes ago'
    >>> timesince(now - datetime.timedelta(seconds=121))
    '2 minutes and 1 second ago'
    >>> timesince(now - datetime.timedelta(seconds=122))
    '2 minutes and 2 seconds ago'
    >>> timesince(now - datetime.timedelta(seconds=3599))
    '59 minutes and 59 seconds ago'
    >>> timesince(now - datetime.timedelta(seconds=3600))
    '1 hour ago'
    >>> timesince(now - datetime.timedelta(seconds=3601))
    '1 hour and 1 second ago'
    >>> timesince(now - datetime.timedelta(seconds=3602))
    '1 hour and 2 seconds ago'
    >>> timesince(now - datetime.timedelta(seconds=3660))
    '1 hour and 1 minute ago'
    >>> timesince(now - datetime.timedelta(seconds=3661))
    '1 hour and 1 minute ago'
    >>> timesince(now - datetime.timedelta(seconds=3720))
    '1 hour and 2 minutes ago'
    >>> timesince(now - datetime.timedelta(seconds=3721))
    '1 hour and 2 minutes ago'
    >>> timesince(datetime.timedelta(seconds=3721))
    '1 hour and 2 minutes ago'
    """
    if isinstance(dt, datetime.timedelta):
        diff = dt
    else:
        now = datetime.datetime.now()
        diff = abs(now - dt)

    periods = (
        (diff.days / 365, 'year', 'years'),
        (diff.days % 365 / 30, 'month', 'months'),
        (diff.days % 30 / 7, 'week', 'weeks'),
        (diff.days % 7, 'day', 'days'),
        (diff.seconds / 3600, 'hour', 'hours'),
        (diff.seconds % 3600 / 60, 'minute', 'minutes'),
        (diff.seconds % 60, 'second', 'seconds'),
    )

    output = []
    for period, singular, plural in periods:
        if int(period):
            if int(period) == 1:
                output.append('%d %s' % (period, singular))
            else:
                output.append('%d %s' % (period, plural))

    if output:
        return '%s ago' % ' and '.join(output[:2])

    return default
