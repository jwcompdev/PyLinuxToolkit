# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# bash_base.py
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
This file contains the BashBase class, the base class for all bash
terminal emulator classes.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import NoReturn, Callable

from pylinuxtoolkit.bash.bash_data import BashData
from pylinuxtoolkit.bash.output_data import OutputData
from pylinuxtoolkit.bash.output_writer import OutputWriter
from pylinuxtoolkit.utils.lambdas import Lambdas
from pylinuxtoolkit.utils.protocols import SupportsWithClose
from pylinuxtoolkit.utils.task_pool import TaskPool


class BashBase(ABC, SupportsWithClose):
    """
    The base class for all bash terminal emulator classes.
    This could theoretically be subclassed, but It's not
    specifically built for that.
    """

    def __init__(self, directory=os.getcwd(),
                 output_function: Callable[[OutputData], NoReturn]
                 = Lambdas.one_arg_no_return,
                 use_threaded_worker=False, wait_for_locks=True, remote_ssh=False,
                 timeout: int | None = 30, print_command: bool = False,
                 print_prompt: bool = False,
                 ) -> NoReturn:
        """
        :param directory: the directory to use as the current working
            directory
        :param output_function: the output function to use, defaults
            to a NOOP function
        :param use_threaded_worker: if True the entire method is run
            in a separate thread
        :param wait_for_locks: if True the client will wait for a file
            lock to release before continuing without raising an
            exception
        :param remote_ssh: if True the client will connect to ssh,
            otherwise it will use the local context
        :param timeout: the timeout for all commands when they are run,
            can be set to None to disable the timeout
        :param print_command: prints the current command to the output
            before the command output actually prints
        :param print_prompt: prints the prompt after the command output
            prints

        """

        self._new_dir: str = directory
        self._running_dir = os.path.dirname(os.path.abspath(__file__))
        self._timeout: int = timeout
        self._task_pool: TaskPool = TaskPool()
        self._is_context_manager = False

        # Global Output params
        self._bash_data: BashData = BashData(remote_ssh)
        self._bash_data.threaded_worker_enabled = use_threaded_worker
        self._bash_data.print_command = print_command
        self._bash_data.print_prompt = print_prompt
        self._bash_data.wait_for_locks = wait_for_locks
        self._bash_data.raise_error_on_lock_wait = False

        self._bash_data.prompt_func = self.get_prompt
        self._bash_data.client_close_func = self.close
        self._output_writer: OutputWriter = OutputWriter(output_function, self._bash_data)

    # Do not ever make a setter for this as it will cause sync issues
    # and any open ssh connections may not be closed properly
    @property
    def is_remote(self):
        """
        Returns True if the bash is set to run remotely.

        :return: True if the bash is set to run remotely
        """

        return self._bash_data.is_remote

    def get_output_writer(self) -> OutputWriter:
        """
        Returns the current output writer instance.

        :return: the current output writer instance
        """

        return self._output_writer

    def get_on_output(self) -> Callable[[OutputData], NoReturn]:
        """
        Returns the function that handles the output.

        :return: the function that handles the output
        """

        return self._output_writer.get_on_output()

    def set_on_output(self, func: Callable[[OutputData], NoReturn]):
        """
        Sets the function that the output of terminal commands
        is passed to.

        :param func: the function to set
        :return: this instance to allow for method chaining
        """

        self._output_writer.set_on_output(func)
        return self

    def is_threaded_worker_enabled(self) -> bool:
        """
        Returns True if threaded worker is enabled.

        :return: True if threaded worker is enabled
        """

        return self._bash_data.threaded_worker_enabled

    def enable_threaded_worker(self):
        """
        Enables the threaded worker.

        :return: this instance to allow for method chaining
        """

        self._bash_data.threaded_worker_enabled = True
        return self

    def disable_threaded_worker(self):
        """
        Disables the threaded worker.

        :return: this instance to allow for method chaining
        """

        self._bash_data.threaded_worker_enabled = False
        return self

    def is_print_prompt_enabled(self) -> bool:
        """
        Returns True if print prompt is enabled.

        :return: True if print prompt is enabled
        """

        return self._bash_data.print_prompt

    def enable_print_prompt(self):
        """
        Enables print prompt.

        :return: this instance to allow for method chaining
        """

        self._bash_data.print_prompt = True
        return self

    def disable_print_prompt(self):
        """
        Disables print prompt.

        :return: this instance to allow for method chaining
        """

        self._bash_data.print_prompt = False
        return self

    def is_print_command_enabled(self) -> bool:
        """
        Returns True if print command is enabled.

        :return: True if print command is enabled
        """

        return self._bash_data.print_command

    def enable_print_command(self):
        """
        Enables print command.

        :return: this instance to allow for method chaining
        """

        self._bash_data.print_command = True
        return self

    def disable_print_command(self):
        """
        Disables print command.

        :return: this instance to allow for method chaining
        """

        self._bash_data.print_command = False
        return self

    def is_wait_for_locks_enabled(self) -> bool:
        """
        Returns True if wait for locks is enabled.

        :return: True if wait for locks is enabled
        """

        return self._bash_data.wait_for_locks

    def enable_wait_for_locks(self):
        """
        Enables wait for locks.

        :return: this instance to allow for method chaining
        """

        self._bash_data.wait_for_locks = True
        return self

    def disable_wait_for_locks(self):
        """
        Disables wait for locks.

        :return: this instance to allow for method chaining
        """

        self._bash_data.wait_for_locks = False
        return self

    def is_raise_error_on_lock_wait_enabled(self) -> bool:
        """
        Returns True if the program is set to raise an error if a
        command is waiting on a lock.

        :return: True if the program is set to raise an error if a
            command is waiting on a lock
        """

        return self._bash_data.raise_error_on_lock_wait

    def enable_raise_error_on_lock_wait(self):
        """
        Enables raising an error if a command is waiting on a lock.

        :return: this instance to allow for method chaining
        """

        self._bash_data.raise_error_on_lock_wait = True
        return self

    def disable_raise_error_on_lock_wait(self):
        """
        Disables raising an error if a command is waiting on a lock.

        :return: this instance to allow for method chaining
        """

        self._bash_data.raise_error_on_lock_wait = False
        return self

    def get_global_timeout(self) -> int:
        """
        Returns the global timeout.

        :return: the global timeout
        """

        return self._timeout

    def set_global_timeout(self, timeout: int):
        """
        Sets the global timeout.

        :param: timeout the timeout to set
        :return: this instance to allow for method chaining
        """

        self._timeout = timeout
        return self

    def set_global_timeout_default(self):
        """
        Sets the global timeout back to the default.

        :return: this instance to allow for method chaining
        """

        self._timeout = 30
        return self

    def running_dir(self) -> str:
        """
        Returns the directory of the current running program.

        :return: the directory of the current running program
        """

        return self._running_dir

    @abstractmethod
    def change_dir(self, directory: str) -> NoReturn:
        """
        Changes the current working directory.

        :param: directory the directory to set
        """

    @property
    @abstractmethod
    def current_dir(self) -> str:
        """
        Returns the current working directory.

        :return: the current working directory
        """

        pass

    @property
    @abstractmethod
    def home_dir(self) -> str:
        """
        Returns the current user's home directory.

        :return: the current user's home directory
        """

        pass

    @property
    @abstractmethod
    def hostname(self) -> str:
        """
        Returns the current system hostname.

        :return: the current system hostname
        """

        pass

    @property
    @abstractmethod
    def current_user(self) -> str:
        """
        Returns the username of the current user.

        :return: the username of the current user
        """

        pass

    def print_prompt(self):
        """
        Manually prints to the output a representation of what the
        terminal prompt would look like in the current working
        directory.

        This uses the current user, hostname, current working
        directory and if root, uses '#' instead of '$'.
        """

        self._output_writer.write_bypass(self.get_prompt())

    def get_prompt(self) -> str:
        """
        Returns a representation of what the terminal prompt would look
        like in the current working directory.

        This uses the current user, hostname, current working
        directory and if root, uses '#' instead of '$'.

        :return: a representation of what the terminal prompt would look
            like in the current working directory
        """
        current_dir = "~"
        sudo_char = '$'
        if self.current_user == "root":
            sudo_char = '#'
        if self.current_dir != self.home_dir:
            current_dir = self.current_dir

        return f"{self.current_user}@{self.hostname}:{current_dir}{sudo_char}"
