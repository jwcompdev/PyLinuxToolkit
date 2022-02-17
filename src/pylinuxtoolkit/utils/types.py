# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# types.py
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
This file contains some general type classes that can be inherited from.
"""


class Final(type):
    """
    A metaclass that can be assigned to a class to completely prevent
    that class from being subclassed.

    >>> class newclass(metaclass=Final)
    """

    # noinspection PyMethodParameters
    def __new__(cls, name, bases, classdict):
        for base in bases:
            if isinstance(base, Final):
                raise TypeError(
                    f"type '{base.__name__}' is not an acceptable base type"
                )
        return type.__new__(cls, name, bases, dict(classdict))
