# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# log_manager.py
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
Contains the LogManager class, that contains basic tools for
logging related to the current project.
"""
from __future__ import annotations

import logging
import sys

from pystdlib.decorators import classproperty


class LogManager:
    """
    Contains basic tools for logging related to the current project.
    """

    c_handler: logging.Handler = logging.StreamHandler(sys.stdout)

    @classmethod
    def enable_logging(cls, level: int | str = logging.DEBUG):
        """
        Enables a logging handler that prints to the console and sets
        the logging level to the specified level.

        :param level: the logging level to set
        """
        # noinspection PyTypeChecker
        cls.c_handler.setFormatter(cls.default_formatter)
        cls.c_handler.setLevel(level)

        logging.getLogger().addHandler(LogManager.c_handler)
        logging.getLogger().setLevel(level)

    @classmethod
    def disable_logging(cls):
        """
        Disables the logging handler that prints to the console.
        """
        logging.getLogger().removeHandler(LogManager.c_handler)

    @classmethod
    def set_global_log_level(cls, level: int | str):
        """
        Sets the logging level to the specified level.

        :param level: the logging level to set
        """
        cls.c_handler.setLevel(level)
        logging.getLogger().setLevel(level)

    @classproperty
    def root_logger(self) -> logging.Logger:
        """
        Returns the root logger.

        :return: the root logger
        """
        return logging.getLogger()

    @classproperty
    def window_logger(self) -> logging.Logger:
        """
        Returns the logger for the Window class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.main.Window")

        :return: the "pylinuxtoolkit.main.Window" logger
        """
        return logging.getLogger("pylinuxtoolkit.main.Window")

    @classproperty
    def ssh_bash_logger(self) -> logging.Logger:
        """
        Returns the logger for the SSHBash class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.ssh_bash.SSHBash")

        :return: the "pylinuxtoolkit.bash.ssh_bash.SSHBash" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.ssh_bash.SSHBash")

    @classproperty
    def local_bash_logger(self) -> logging.Logger:
        """
        Returns the logger for the LocalBash class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.local_bash.LocalBash")

        :return: the "pylinuxtoolkit.bash.local_bash.LocalBash" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.local_bash.LocalBash")

    @classproperty
    def linux_bash_logger(self) -> logging.Logger:
        """
        Returns the logger for the LinuxBash class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.linux_bash.LinuxBash")

        :return: the "pylinuxtoolkit.bash.linux_bash.LinuxBash" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.linux_bash.LinuxBash")

    @classproperty
    def output_writer_logger(self) -> logging.Logger:
        """
        Returns the logger for the OutputWriter class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.output_writer.OutputWriter")

        :return: the "pylinuxtoolkit.bash.output_writer.OutputWriter" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.output_writer.OutputWriter")

    @classproperty
    def bash_command_logger(self) -> logging.Logger:
        """
        Returns the logger for the BashCommand class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.bash_command.BashCommand")

        :return: the "pylinuxtoolkit.bash.bash_command.BashCommand" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.bash_command.BashCommand")

    @classproperty
    def bash_commands_logger(self) -> logging.Logger:
        """
        Returns the logger for the BashCommands class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.bash.bash_commands.BashCommands")

        :return: the "pylinuxtoolkit.bash.bash_commands.BashCommands" logger
        """
        return logging.getLogger("pylinuxtoolkit.bash.bash_commands.BashCommands")

    @classproperty
    def raspberry_pi_logger(self) -> logging.Logger:
        """
        Returns the logger for the RaspberryPi class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.rpi.raspberry_pi.RaspberryPi")

        :return: the "pylinuxtoolkit.rpi.raspberry_pi.RaspberryPi" logger
        """
        return logging.getLogger("pylinuxtoolkit.rpi.raspberry_pi.RaspberryPi")

    @classproperty
    def task_pool_logger(self) -> logging.Logger:
        """
        Returns the logger for the TaskPool class.

        This is the same as calling:

        >>> logging.getLogger("pylinuxtoolkit.utils.task_pool.TaskPool")

        :return: the "pylinuxtoolkit.utils.task_pool.TaskPool" logger
        """
        return logging.getLogger("pylinuxtoolkit.utils.task_pool.TaskPool")

    # noinspection SpellCheckingInspection
    @classproperty
    def default_formatter(self) -> logging.Formatter:
        """
        Returns the default formatter for this project.

        This is the same as calling:

        >>> logging.Formatter('[%(levelname)-8s] %(name)s - %(message)s')

        :return: the default formatter for this project
        """
        return logging.Formatter('[%(levelname)-8s] %(name)s - %(message)s')

    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        """
        Return a logger with the specified name, creating it if necessary.

        If no name is specified, return the root logger.

        :param name: the name of the logger to lookup
        :return: the specified logger
        """
        return logging.getLogger(name)
