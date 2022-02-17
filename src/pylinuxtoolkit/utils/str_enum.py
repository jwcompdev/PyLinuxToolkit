# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# str_enum.py
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
Contains the StrEnum class, a subclass of Enum that allows
strings as values.
"""

from enum import Enum, auto


class StrEnum(str, Enum):
    """This is a subclass of Enum that allows strings as values."""

    def __new__(cls, *args):
        """Verifies that all values are of type string."""

        for arg in args:
            if not isinstance(arg, (str, auto)):
                raise TypeError(
                    "Values must be strings: "
                    f"{repr(arg)} is a {type(arg)}"
                )
        return super().__new__(cls, *args)

    def __str__(self) -> str:
        """
        Returns the string as the value so the enum can be used like
        an immutable string.

        :return: the string as the value
        """

        return self.value

    @classmethod
    def value_exists(cls, value: str) -> bool:
        """
        Checks if the specified string matches a value in the class and
        if so returns True.

        :return: True if the value is found
        """

        return any(val.lower() == value.lower()
                   for _, val in cls.__members__.items())

    @classmethod
    def key_exists(cls, key: str) -> bool:
        """
        Checks if the specified string matches a key
        in the class and if so returns True.

        :return: True if the key is found
        """

        return any(_key.lower() == key.lower()
                   for _key, _ in cls.__members__.items())

    @classmethod
    def size(cls) -> int:
        """
        Returns the amount of items int the enum.

        :return: the amount of items in the enum
        """

        num = 0
        for _, _ in cls.__members__.items():
            num += 1

        return num

    @classmethod
    def __len__(cls) -> int:
        """
        Returns the amount of items int the enum.

        :return: the amount of items in the enum
        """

        return cls.size()
