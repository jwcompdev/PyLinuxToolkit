# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# bash_commands.py
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

"""
Contains the BashOutput class, a cache of the most
recent command outputs.
"""
from pystdlib.bash.bash_command import BashCommand
from pystdlib.str_utils import build_repr


class BashCommands:
    """Contains a dictionary of all previously run commands."""

    def __init__(self, commands: dict[int, BashCommand] = None):
        """Initializes the BashCommands object."""
        self._current_cid: int = 1

        if commands is None:
            self._commands: dict[int, BashCommand] = {}
        else:
            self._commands: dict[int, BashCommand] = commands

            for command in commands.values():
                if command.cid > self._current_cid:
                    self._current_cid = command.cid + 1
                elif command.cid == self._current_cid:
                    self._current_cid += 1

    def __str__(self):
        return self._commands.__str__()

    def __repr__(self):
        return build_repr(self, self._commands)

    def get_commands(self) -> dict[int, BashCommand]:
        """
        Returns the dictionary of all commands.

        :return: the dictionary of all commands
        """
        return self._commands

    def get_command_by_id(self, cid: int):
        """
        Returns the command that matches the specified id.

        :param cid: the id to match
        :return: the matched command
        """
        return self._commands.get(cid)

    # NOTE: Do not change the name of this method or things will break.
    def add_command(self, command: BashCommand) -> int:
        """
        Adds the specified command, assigns it a new ID
        and returns that ID.

        :param command: the command
        :return: the new command ID
        """
        new_cid = self._current_cid
        self._current_cid += 1

        command.set_cid(new_cid)

        self._commands[new_cid] = command

        return new_cid

    def get_last(self) -> BashCommand:
        """
        Returns the most recently added command.

        :return: the most recently added command
        """
        return self._commands[self._current_cid - 1]
