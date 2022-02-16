# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# OutputData.py
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
This file contains the OutputData class, a data object that holds all
the state and information for the most recent run command.
"""
from __future__ import annotations

from pexpect import spawn

from pylinuxtoolkit.utils.Values import StringValue


class OutputData:
    """
    This is a data object that holds all the state and information
    for the most recent run command.
    """

    def __init__(self, is_remote: bool, process, line: str | StringValue, command: str):
        self._is_remote: bool = is_remote
        self._client: spawn = process
        self._current_line: StringValue = StringValue(line)
        self._current_command: str = command

    @property
    def is_remote(self) -> bool:
        """
        Returns True if the bash is set to run remotely.

        :return: True if the bash is set to run remotely
        """

        return self._is_remote

    @property
    def client(self) -> spawn:
        """
        Returns the internal bash client instance.
        :return: the internal bash client instance
        """
        return self._client

    @property
    def current_line(self) -> StringValue:
        """
        Returns the current line of text that was
        just sent from the bash.
        :return: the current line of text that was
        just sent from the bash
        """

        return self._current_line

    @property
    def current_command(self) -> str:
        """
        Returns the most recent command run typing the bash.
        :return: the most recent command run typing the bash
        """

        return self._current_command
