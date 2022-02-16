# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# Exceptions.py
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
This file contains exception classes for all bash objects.
"""


class BashError(Exception):
    """Base class for other exceptions"""
    pass

class BashConnectionError(BashError):
    """Raised when an ssh connection was unable to be opened or closed"""
    pass

class BashPermissionError(BashError):
    """Raised when user doesn't have permission to run the specified command"""
    pass

class BashValueError(BashError):
    """Raised when the incorrect value was supplied"""
    pass