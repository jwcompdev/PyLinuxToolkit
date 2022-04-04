# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# output.py
# Copyright (C) 2022 JWCompDev <jwcompdev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by
# the Apache Software Foundation; either version 2.0 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License for more details.
#
# You should have received a copy of the Apache License
# along with this program.  If not, see <https://www.apache.org/licenses/>.

"""
Contains the OutputWriter class, a handler for the printing
and filtering of all text to be printed to the output.
"""
from __future__ import annotations

from typing import NoReturn, Callable

from PyQt5 import QtCore
from pexpect import spawn

from pystdlib.bash import BashPermissionError
from pystdlib.bash.bash_checks import BashChecks
from pystdlib.bash.bash_data import BashData
from pystdlib.str_utils import build_repr
from pystdlib.values import StringValue


class OutputData:
    """
    This is a data object that holds all the state and information
    for the most recent run command.
    """

    def __init__(self, is_remote: bool, client, line: str | StringValue, command: str):
        """
        Initializes the data object.

        :param is_remote: if True the client is running over ssh
        :param client: the bash client
        :param line: the current line of text to be output
        :param command: the last command run
        """
        self._is_remote: bool = is_remote
        self._client: spawn = client
        self._current_line: StringValue = StringValue(line)
        self._current_command: str = command

    def __str__(self):
        return (
            f'(is_remote={self._is_remote}, client="{str(self._client)}",'
            f' current_line="{str(self._current_line)}", '
            f'current_command="{str(self._current_command)}"'
        )

    def __repr__(self):
        return build_repr(self, self._is_remote, str(self._current_line))

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


class OutputWriter(QtCore.QObject):
    """
    This object handles the printing and filtering of all text to be
    printed to the output. This class works just like stdout and can
    be used instead of it in other classes if desired.
    """

    _on_output_signal = QtCore.pyqtSignal(OutputData, name="on_output")

    def __init__(
        self,
        on_output: Callable[[OutputData], NoReturn],
        bash_data: BashData,
        on_setting: Callable[[OutputData], NoReturn] = None,
    ):
        super().__init__()
        self._on_output: Callable[[OutputData], NoReturn] = on_output
        self._on_setting: Callable[[OutputData], NoReturn] = on_setting
        self.data: BashData = bash_data
        self._last_line: StringValue = StringValue()
        self._on_output_signal.connect(self._on_output)
        self._waiting_for_lock = False

    def write(self, text: str | StringValue):
        """
        Writes the specified text to the output with
        condition filtering.

        :param text: the text to write to the output
        """
        self.data.current_line = StringValue(text).strip_ansi_codes()
        self._process_output()

    def write_bypass(self, text: str | StringValue):
        """
        Writes the specified text to the output but bypasses the
        normal condition filtering.

        :param text: the text to write to the output
        """
        self.data.current_line = StringValue(text).strip_ansi_codes()
        self._emit_output(text)

    # This method is required to be considered a writer
    def flush(self):
        """
        Does nothing currently but is required to support being
        written to like stdout.
        """

    def get_last_line(self) -> StringValue:
        """
        Returns the last line printed to the output.

        :return: the last line printed to the output
        """
        return self._last_line

    def get_on_output(self) -> Callable[[OutputData], NoReturn]:
        """
        Returns the function that handles the output.

        :return: the function that handles the output
        """
        return self._on_output

    def set_on_output(self, func: Callable[[OutputData], NoReturn]):
        """
        Sets the function that the output of terminal
        commands is passed to.

        :param func: the function to set
        :return: this instance to allow for method chaining
        """
        self._on_output = func

    def _emit_output(self, current_line: StringValue) -> NoReturn:
        """
        If the command is being run with the QTWorker,
        then the line is passed through that then
        to the user defined on_output function.
        If QTWorker is not being used then the line is
        passed directly to the on_output function.

        :param current_line: the current line to emit
        """
        self._last_line.set(current_line)
        output_data = OutputData(
            self.data.is_remote, self.data.client, current_line, self.data.command
        )

        if self.data.threaded_worker_enabled:
            self._on_output_signal.emit(output_data)
        else:
            self._on_output(output_data)

    def _kill_raise(self, exception) -> NoReturn:
        """
        Halts the command execution then raises the
        specified exception.

        :param exception: the exception to be raised
        """
        if not self.data.is_remote:
            self.data.client.kill(1)

        self.data.client_close_func()
        raise exception

    def _process_output(self) -> NoReturn:
        """
        Processes the output line by line and reformats it then passes
        it to the QTWorker emit method that then passes it to the
        user-defined on_output function.
        """
        output_raw: list[StringValue] = (
            StringValue(self.data.current_line).strip_ansi_codes().split("\r\r")
        )
        output_modified: list[StringValue] = []
        for line in output_raw:
            line.rstrip("\n")
            line.rstrip("\r")
            line.rstrip()
            line.lstrip("\n")
            line.lstrip("\r")
            output2: list[StringValue] = line.split("\r\n")
            output3: list[StringValue] = []
            for line2 in output2:
                if "%" not in line2 and line2 != "":
                    output3.append(line2)

            # Checks if for some reason the last command prints on the
            # same line as the prompt. Only seems to happen via local
            # bash.
            for line3 in output3:
                if self.data.prompt in line3:
                    line3.replace(self.data.prompt, "").strip()
                    if line3 != "":
                        output_modified.append(line3)
                    output_modified.append(StringValue(self.data.prompt))
                else:
                    output_modified.append(line3)

        for line in output_modified:
            self._filter_line(line.strip("\n").strip("\r"))

    def _filter_line(self, current_line):
        # TODO: replace with less conditions
        if (
            current_line != ""
            and current_line != "\r\n"
            and not BashChecks.is_pexpect_garbage(current_line)
            and current_line.strip() != "exit"
            and (self.data.command != current_line or self.data.print_command)
            and not BashChecks.is_apt_warning(current_line)
            and not BashChecks.is_pydev_debugger(current_line)
            and not BashChecks.is_debconf_error(current_line)
        ):
            if BashChecks.is_apt_update(current_line):
                current_line = current_line.replace("\r", "").strip(" ")
                self._emit_output(current_line)
            elif BashChecks.is_prompt(current_line, self.data.current_user):
                if (
                    self._last_line.strip() != current_line.strip()
                    and self._last_line.strip() != self.data.command
                    and self.data.print_prompt
                ):
                    self._emit_output(current_line.strip())
            elif BashChecks.is_not_sudo(current_line):
                self._emit_output(current_line)
                self._kill_raise(
                    BashPermissionError(
                        "Command needs to be run as sudo - " + current_line
                    )
                )
            elif BashChecks.is_file_locked(current_line):
                if self.data.raise_error_on_lock_wait:
                    self._emit_output(current_line)
                    self._kill_raise(BashPermissionError(current_line))
                elif self.data.wait_for_locks and not self._waiting_for_lock:
                    self._waiting_for_lock = True
                    self._emit_output(current_line)
            else:
                self._emit_output(current_line)

    def _is_threaded_worker_enabled(self) -> bool:
        return self.data.threaded_worker_enabled
