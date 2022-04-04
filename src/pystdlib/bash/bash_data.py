# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# bash_data.py
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
Contains the BashData class, a data object that stores all
state and settings for the current bash instance.
"""
from __future__ import annotations

from typing import Callable, NoReturn

from pexpect import spawn

from pystdlib.lambdas import Lambdas
from pystdlib.str_utils import build_repr
from pystdlib.values import StringValue


class BashData:
    """
    This is a data object that holds all the state and settings for the
    current bash instance.
    """

    def __init__(self, is_remote: bool):
        """
        Initializes the data object.

        :param is_remote: if True the bash is not being run remotely.
        """
        self._is_remote: bool = False
        # noinspection PyTypeChecker
        self.client: spawn = None
        self.current_user: str = ""
        self.current_line: StringValue = StringValue()
        self.command: str = ""
        self.prompt_func: Callable[[], str] = Lambdas.return_empty_str
        self.client_close_func: Callable[[], NoReturn] = Lambdas.no_return

        self._is_remote: bool = is_remote
        self.threaded_worker_enabled: bool = False
        self.print_command: bool = False
        self.print_prompt: bool = False
        self.wait_for_locks: bool = False
        self.raise_error_on_lock_wait: bool = False

    def __repr__(self):
        return build_repr(self, self._is_remote)

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
