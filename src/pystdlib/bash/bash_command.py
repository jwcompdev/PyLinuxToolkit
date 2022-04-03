# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# bash_command.py
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
Contains the BashCommand class, a data object that contains
info about the most recent run command.
"""
from __future__ import annotations

from typing import NoReturn

from pystdlib.bash import BashError
from pystdlib.bash.bash_checks import BashChecks
from pystdlib.introspection import Caller
from pystdlib.str_utils import build_repr
from pystdlib.values import StringValue, IntegerValue, FloatValue


class BashCommand:
    """
    A representation of a command run on the bash with its
    running directory, output command exit code.
    """

    def __init__(
        self,
        command: str | StringValue,
        directory: str | StringValue,
        output: str | StringValue,
        exit_code: int | str | IntegerValue | FloatValue | StringValue,
    ):
        """
        Initializes the command object.

        :param command: the command
        :param directory: the directory
        :param output: the output
        :param exit_code: the exit code
        """
        # noinspection PyTypeChecker
        self._cid: int = None
        self._command: str = str(command)
        self._directory: str = str(directory)
        self._sudo: bool = False

        if isinstance(exit_code, int):
            self._exit_code: int = exit_code
        elif isinstance(exit_code, str):
            self._exit_code: int = int(exit_code)
        elif isinstance(exit_code, (IntegerValue, FloatValue, StringValue)):
            self._exit_code: int = exit_code.to_int()
        else:
            self._exit_code = None

        if isinstance(output, StringValue):
            self._output: str = self._process_output(output.get()).get()
        else:
            self._output: str = self._process_output(output).get()

        if command.startswith("sudo "):
            self._sudo = True
            self._command = self._command.lstrip("sudo ")

    def __str__(self):
        return (
            f"(cid={self._cid}, command={self._command},"
            f' directory="{self._directory}", sudo={self._sudo},'
            f" exit_code={self._exit_code})"
        )

    def __repr__(self):
        return build_repr(
            self, self._command, self._directory, self._output, self._exit_code
        )

    @property
    def cid(self) -> int:
        """
        Returns the command ID.

        :return: the command ID
        """
        return self._cid

    @property
    def command(self) -> str:
        """
        Returns the command.

        :return: the command
        """
        return self._command

    @property
    def directory(self) -> str:
        """
        Returns the command directory.

        :return: the command directory
        """
        return self._directory

    @property
    def sudo(self) -> bool:
        """
        Returns True if the command was run as sudo.

        :return: True if the command was run as sudo
        """
        return self._sudo

    @property
    def output(self) -> str:
        """
        Returns the command output.

        :return: the command output
        """
        return self._output

    @property
    def exit_code(self) -> int:
        """
        Returns the command exit code.

        :return: the command exit code
        """
        return self._exit_code

    def set_cid(self, cid: int) -> NoReturn:
        """
        Sets the command ID.

        NOTE: This method is designed to only be run from the
        'add_command' method in the BashCommands class and will
        raise a BashError if run from anywhere else.

        :param cid: the id to set
        """
        if cid is not None and Caller().name_matches("add_command"):
            self._cid = cid
        else:
            raise BashError(
                "The cid attribute is read-only and can only be set internally!"
            )

    @staticmethod
    def _process_output(current_line) -> StringValue:
        """
        Processes the output line by line and reformats it then passes
        it to the QTWorker emit method that then passes it to the
        user-defined on_output function.
        """
        output_raw: list[StringValue] = (
            StringValue(current_line).strip_ansi_codes().split("\r\r")
        )
        output_modified: list[StringValue] = []
        output2: list[StringValue] = []

        for line in output_raw:
            line.rstrip("\n")
            line.rstrip("\r")
            line.rstrip()
            line.lstrip("\n")
            line.lstrip("\r")
            op1 = line.split("\r\n")
            for line2 in op1:
                op2 = line2.split("\r")
                for line3 in op2:
                    line3.rstrip("\n")
                    line3.rstrip("\r")
                    line3.rstrip()
                    line3.lstrip("\n")
                    line3.lstrip("\r")
                    output2.append(line3)

        for line2 in output2:
            if "%" not in line2 and line2 != "":
                output_modified.append(
                    line2.strip("\n").strip("\r").strip("\n").strip("\r")
                )

        final_output: list[StringValue] = []
        for line in output_modified:
            final_output.append(BashCommand._filter_line(line))

        full_output: StringValue = StringValue()
        for line in final_output:
            full_output += line + "\n"

        return full_output.rstrip("\n")

    @staticmethod
    def _filter_line(current_line) -> StringValue:
        if (
            current_line != ""
            and current_line != "\r\n"
            and not BashChecks.is_pexpect_garbage(current_line)
            and current_line.strip() != "exit"
            and not BashChecks.is_apt_warning(current_line)
            and not BashChecks.is_pydev_debugger(current_line)
            and not BashChecks.is_debconf_error(current_line)
        ):
            if BashChecks.is_apt_update(current_line):
                current_line = current_line.replace("\r", "").strip(" ")

            return current_line
        return StringValue()
