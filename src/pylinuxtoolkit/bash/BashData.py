# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# BashData.py
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
This file contains the BashData class, a data object that stores all
state and settings for the current bash instance.
"""
from typing import Callable, NoReturn

from pexpect import spawn

from pylinuxtoolkit.utils import Lambdas
from pylinuxtoolkit.utils.Literals import EMPTY
from pylinuxtoolkit.utils.Values import StringValue


class BashData:
    """
    This is a data object that holds all the state and settings for the
    current bash instance.
    """

    def __init__(self, is_remote: bool):
        self._is_remote: bool = False
        # noinspection PyTypeChecker
        self.client: spawn = None
        self.current_user: str = EMPTY
        self.current_line: StringValue = StringValue(EMPTY)
        self.command: str = EMPTY
        self.prompt_func: Callable[[], str] = Lambdas.return_empty_str
        self.client_close_func: Callable[[], NoReturn] = Lambdas.no_return

        self._is_remote: bool = is_remote
        self.threaded_worker_enabled: bool = False
        self.print_command: bool = False
        self.print_prompt: bool = False
        self.wait_for_locks: bool = False
        self.raise_error_on_lock_wait: bool = False

    @property
    def is_remote(self):
        """
        Returns True if the bash is set to run remotely.

        :return: True if the bash is set to run remotely
        """

        return self._is_remote

    @property
    def prompt(self) -> str:
        """
        Returns the current prompt string.

        :return: the current prompt string
        """
        return self.prompt_func()
