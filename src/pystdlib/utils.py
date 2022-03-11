# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# utils/__init__.py
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

"""Contains some basic utilities."""
from __future__ import annotations

import datetime
import json
import math
import pickle
import typing
from typing import NoReturn, Any


class IllegalArgumentError(Exception):
    """
    This exception is raised when a required argument was not found
    when a method was called.
    """


class InvalidInputError(TypeError):
    """
    Custom error raised when received object
    is not a string as expected.
    """

    def __init__(self, input_data: typing.Any):
        """
        Initializes the error.

        :param input_data: Any received object
        """
        type_name = type(input_data).__name__
        msg = f'Expected "str", received "{type_name}"'
        super().__init__(msg)


def check_argument(expression: bool,
                   error_message="Invalid argument specified!") -> NoReturn:
    """Ensures the truth of an expression involving one or
    more parameters to the calling method.

    :param expression: a boolean expression
    :param error_message: the exception message to use if the
                check fails; will be converted to a string
    :raises IllegalArgumentError: if expression is False
    """
    if not expression:
        raise IllegalArgumentError(str(error_message))


def check_argument_type(value,
                        value_name,
                        types: type | tuple[type, ...]) -> NoReturn:
    """Ensures the truth of an expression involving one or
    more parameters to the calling method.

    :param value: the value to check
    :param value_name: the name of the value
    :param types: a type or tuple of types to check
    :raises IllegalArgumentError: if expression is False
    """
    if not isinstance(value, types):
        raise IllegalArgumentError(f"\"{value_name}\" must be one "
                                   f"of the following types: {types}")


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


def convert_bytes_to_string(number: int) -> str:
    """Returns the conversion from bytes to the correct
    version (1024 bytes = 1 KB) as a string.

    :param number: number to convert to a readable string
    :return: the specified number converted to a readable string
    """
    num = number

    factor = 1024
    if num >= factor:
        num /= factor
        if num >= factor:
            num /= factor
            if num >= factor:
                num /= factor
                if num >= factor:
                    num /= factor
                    if num >= factor:
                        num /= factor
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
    rounded = math.floor(num * rounding_factor) / rounding_factor
    return f"{rounded:.2f}" + suffix


def timesince(d_t: datetime.datetime | datetime.timedelta,
              default: str = 'just now') -> str:
    """
    Returns string representing 'time since' e.g.
    3 days ago, 5 hours ago etc.

    >>> time_now = datetime.datetime.now()
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
    if isinstance(d_t, datetime.timedelta):
        diff = d_t
    else:
        now = datetime.datetime.now()
        diff = abs(now - d_t)

    periods = (
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
                output.append(f'{period} {singular}')
            else:
                output.append(f'{period} {plural}')

    if output:
        return f"{' and '.join(output[:2])} ago"

    return default


def kwa(**kwargs) -> dict:
    """
    Returns the specified kwargs as a dict.

    :param kwargs: the kwargs to convert
    :return: the specified kwargs as a dict
    """
    return kwargs


def save_pickle(file, data) -> NoReturn:
    """
    Pickles the specified data to the specified file.

    :param file: the file to save to
    :param data: the data to pickle
    """
    with open(file, 'wb') as open_file:
        pickle.dump(data, open_file)


def load_pickle(file):
    """
    Loads the pickled data from the specified file.

    :param file: the file to read
    :return: the pickled data
    """
    with open(file, 'rb') as open_file:
        data = pickle.load(open_file, encoding='bytes')
    return data


def save_json(file, data) -> NoReturn:
    """
    Converts the specified data to JSON
    and saves it in the specified file.

    :param file: the file to save to
    :param data: the data to convert
    """
    with open(file, 'w', encoding='utf-8') as open_file:
        json.dump(data, open_file, ensure_ascii=False)


def load_json(file):
    """
    Converts the JSON from the specified file to a python object.

    :param file: the file to read
    :return: the data object
    """
    with open(file, 'r') as open_file:
        return json.load(open_file)
