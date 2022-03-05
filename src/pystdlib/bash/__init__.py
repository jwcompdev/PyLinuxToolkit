# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# pystdlib/__init__.py.py
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

"""Contains the pystdlib.bash package."""
from __future__ import annotations

# from .bash_base import BashBase, BashSettings
# from .bash_checks import BashChecks
# from .bash_command import BashCommand
# from .bash_commands import BashCommands
# from .bash_data import BashData
# from .command_event import CommandEvent
# from .linux_bash import LinuxBash
# from .local_bash import LocalBash
# from .output import OutputWriter, OutputData
# from .ssh_bash import SSHBash


class BashError(Exception):
    """Base class for other exceptions"""


class BashConnectionError(BashError):
    """Raised when an ssh connection was unable to be opened or closed"""


class BashPermissionError(BashError):
    """Raised when user doesn't have permission to run the specified command"""


class BashValueError(BashError):
    """Raised when the incorrect value was supplied"""
