# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# OutputWriter.py
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
This file contains the OutputWriter class, a handler for the printing
and filtering of all text to be printed to the output.
"""
from __future__ import annotations

from typing import NoReturn, Callable

from pylinuxtoolkit.bash.BashChecks import BashChecks
from pylinuxtoolkit.bash.BashData import BashData
from pylinuxtoolkit.bash.CustomQTWorker import CustomQTWorker
from pylinuxtoolkit.bash.Exceptions import BashPermissionError
from pylinuxtoolkit.bash.OutputData import OutputData
from pylinuxtoolkit.utils.Values import StringValue


class OutputWriter:
    """
    This object handles the printing and filtering of all text to be
    printed to the output. This class works just like stdout and can
    be used instead of it in other classes if desired.
    """

    def __init__(
        self,
        on_output: Callable[[OutputData], NoReturn],
        bash_data: BashData,
        on_setting: Callable[[OutputData], NoReturn] = None,
    ):
        self._on_output: Callable[[OutputData], NoReturn] = on_output
        self._on_setting: Callable[[OutputData], NoReturn] = on_setting
        self.data: BashData = bash_data
        self._last_line: StringValue = StringValue()
        self._qt_worker: CustomQTWorker = CustomQTWorker()
        self._qt_worker.set_on_output_function(self._on_output)

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

    # This method is just here to allow for operability
    # and doesn't need to do anything
    def flush(self):
        """
        Does nothing currently but is required to support being
        written to like stdout.
        """

        pass

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
            self._qt_worker.run_on_output_function(output_data)
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

        output_raw = (
            StringValue(self.data.current_line).strip_ansi_codes().split("\r\r")
        )
        output_modified = []
        for line in output_raw:
            line = line.rstrip("\n")
            line = line.rstrip("\r")
            line = line.rstrip()
            line = line.lstrip("\n")
            line = line.lstrip("\r")
            output2 = line.split("\r\n")
            output3 = []
            for line2 in output2:
                if "%" not in line2 and line2 != "":
                    output3.append(line2)

            # Checks if for some reason the last command prints on the same line as the prompt
            # Only seems to happen via local bash
            for line3 in output3:
                if self.data.prompt in line3:
                    remaining_text = line3.replace(self.data.prompt, "").strip()
                    if remaining_text != "":
                        output_modified.append(remaining_text)
                    output_modified.append(self.data.prompt)
                else:
                    output_modified.append(line3)

        for line in output_modified:
            current_line = line.strip("\n").strip("\r")
            if (
                current_line != ""
                and current_line != "\r\n"
                and "[PEXPECT]" not in current_line
                and "unset PROMPT_COMMAND" not in current_line
                and "'s password:" not in current_line
                and "exit" != current_line.strip()
            ):

                # noinspection PyUnresolvedReferences
                if not self.data.print_command and self.data.command == current_line:
                    continue
                elif current_line.strip().startswith(
                    self.data.current_user + "@"
                ) and current_line.strip().endswith("$"):
                    # print("*< " + self._last_line.strip())
                    # print(">* " + current_line.strip())
                    if self._last_line.strip() == current_line.strip():
                        continue
                    elif self._last_line.strip() == self.data.command:
                        continue
                    elif self.data.print_prompt:
                        self._emit_output(current_line.strip())
                    else:
                        continue
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
                elif BashChecks.is_apt_warning(current_line):
                    continue
                elif BashChecks.is_pydev_debugger(current_line):
                    continue
                elif BashChecks.is_debconf_error(current_line):
                    continue
                else:
                    if (
                        "Hit:" in current_line
                        and "http" in current_line
                        or "Get:" in current_line
                        and "http" in current_line
                        or "Ign:" in current_line
                        and "http" in current_line
                    ):
                        current_line = current_line.replace("\r", "").strip(" ")

                    self._emit_output(current_line)

    def _is_threaded_worker_enabled(self) -> bool:
        return self.data.threaded_worker_enabled
