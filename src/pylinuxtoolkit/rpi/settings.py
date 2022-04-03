# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# settings.py
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
Contains the Settings and SettingMonitor classes, that stores and
monitors new commands with a thread and updates the GUI or runs
other tasks.
"""
from typing import List, NoReturn

from pystdlib.bash.bash_commands import BashCommands
from pystdlib.logged import Logged
from pystdlib.task_pool import TaskPool
from pystdlib.values import StringValue


# class Setting:
#     def __init__(self, name, command):
#         self._name = name
#         self._command = command
#         self._value = ""
#
#     @property
#     def name(self):
#         return self._name
#
#     @property
#     def command(self):
#         return self._command
#
#     @property
#     def value(self):
#         return self._value
#
#     @value.setter
#     def value(self, value):
#         self._value = value
#
#
# class Settings:
#     def __init__(self):
#         self._settings: dict[str, Setting] = {}
#
#     @property
#     def settings(self) -> dict[str, Setting]:
#         return self._settings
#
#     def get(self, name: str) -> Setting:
#         return self._settings.get(name)
#
#     def add(self, name: str, setting: Setting) -> NoReturn:
#         self._settings[name] = setting


class SettingMonitor(Logged):
    """
    Contains a thread that monitors new commands
    and updates the GUI or runs other tasks
    """

    def __init__(self, commands: BashCommands):
        """
        Initializes the SettingMonitor.

        :param commands: the BashCommands instance
        """
        self._task_pool = TaskPool()
        self._commands: BashCommands = commands
        self._is_running = False
        self._print_requested = False
        self._should_terminate = False

        self.current_cid: int = 1
        self.processed_list: List[str] = []

    def start_monitoring(self) -> NoReturn:
        """Starts the monitor."""
        if not self._is_running:
            self._is_running = True

            self._start_monitoring()

    @TaskPool.threaded_class_task(pool_name="_task_pool")
    def _start_monitoring(self):
        """Starts the monitor."""
        self._debug("Starting Monitoring...")

        while not self._should_terminate:
            command = self._commands.get_command_by_id(self.current_cid)
            if command is not None:
                self._debug(
                    f"Loaded Command Output({self.current_cid}): "
                    f'"{command.command}" '
                    f"- [EC{command.exit_code}]"
                )
                self.processed_list.append(f"({self.current_cid} - {command.command})")
                self.current_cid += 1

            if self._print_requested:
                self._print_requested = False
                result: StringValue = StringValue()

                result.appendprefix("{")

                result.append(", ".join(x for x in self.processed_list))

                result.rstrip(",")
                result.appendsuffix("}")

                self._debug(result.get())

        self._should_terminate = False
        self._is_running = False

        self._debug("Monitoring terminated!!!")

    def request_processed_list(self) -> NoReturn:
        """
        Requests the monitor to print the current list
        to the logger.
        """
        self._print_requested = True

    def request_termination(self) -> NoReturn:
        """Requests the monitor to stop running."""
        self._should_terminate = True

    def is_running(self) -> bool:
        """
        Returns True if the monitor is running.

        :return: True if the monitor is running
        """
        return self._is_running
