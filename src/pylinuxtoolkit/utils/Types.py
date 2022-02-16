# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# Types.py
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

    >> class newclass(metaclass=Final)
    """

    def __new__(mcs, name, bases, classdict):
        for b in bases:
            if isinstance(b, Final):
                raise TypeError(
                    "type '{0}' is not an acceptable base type".format(b.__name__)
                )
        return type.__new__(mcs, name, bases, dict(classdict))
