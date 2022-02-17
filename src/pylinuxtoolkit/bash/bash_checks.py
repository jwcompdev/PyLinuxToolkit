# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# bash_checks.py
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
This file contains the BashChecks class, which contains functions that
check a line from the terminal for a conditional.
"""
from pylinuxtoolkit.utils.values import StringValue


class BashChecks:
    """
    Static functions that check a line from the terminal for a conditional.
    """

    @staticmethod
    def is_not_sudo(line: StringValue) -> bool:
        """
        Checks for an error that is caused by the sudo keyword not
        being used.

        :param line: the line to check
        :return: the result
        """

        return "E: Could not open lock file" in line \
               and "open (13: Permission denied)" in line

    @staticmethod
    def is_file_locked(line: StringValue) -> bool:
        """
        Checks for an error that is caused by a file being locked
        because another process is using it.

        :param line: the line to check
        :return: the result
        """

        return "Waiting for cache lock: Could not get lock" in line \
               and "It is held by process" in line

    @staticmethod
    def is_apt_warning(line: StringValue):
        """
        Checks for an error that shows when using the apt command.

        :param line: the line to check
        :return: the result
        """

        return "WARNING: apt does not have a stable CLI interface. " \
               "Use with caution in scripts." in line

    @staticmethod
    def is_pydev_debugger(line: StringValue):
        """
        Checks for an error that shows when using a debugger.

        :param line: the line to check
        :return: the result
        """

        return "bytes arguments were passed to a new process creation function. " \
               "Breakpoints may not work correctly." in line

    @staticmethod
    def is_debconf_error(line: StringValue):
        """
        Checks for an error that shows when an interactive program is
        run with progress bars.

        :param line: the line to check
        :return: the result
        """

        return "debconf: unable to initialize frontend: Dialog" in line \
               or "debconf: (Dialog frontend will not work on a dumb terminal" in line \
               or "debconf: falling back to frontend: Readline" in line

    @staticmethod
    def is_pexpect_garbage(line: StringValue):
        """
        Checks for garbage lines from pexpect.

        :param line: the line to check
        :return: the result
        """

        return "[PEXPECT]" in line \
               or "unset PROMPT_COMMAND" in line \
               or "'s password:" in line

    @staticmethod
    def is_apt_update(line: StringValue):
        """
        Checks for lines that are from apt update.

        :param line: the line to check
        :return: the result
        """

        return "Hit:" in line and "http" in line \
               or "Get:" in line and "http" in line \
               or "Ign:" in line and "http" in line

    @staticmethod
    def is_prompt(line: StringValue, current_user: str):
        """
        Checks for lines that are the current prompt.

        :param line: the line to check
        :param current_user: the current user to check for
        :return: the result
        """

        return line.strip().startswith(current_user + "@") \
               and line.strip().endswith("$")
