# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# linux_bash.py
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
This file contains the LinuxBash class, a bash terminal emulator that
allows running commands locally or over ssh.
"""
from __future__ import annotations

import os
from typing import NoReturn, Union, Callable

from pylinuxtoolkit.bash.local_bash import LocalBash
from pylinuxtoolkit.bash.output_data import OutputData
from pylinuxtoolkit.bash.output_writer import OutputWriter
from pylinuxtoolkit.bash.ssh_bash import SSHBash
from pylinuxtoolkit.utils.lambdas import Lambdas

StrOrBytesPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


class LinuxBash:
    """
    A bash terminal emulator that allows running commands locally or over ssh.
    """

    def __init__(
        self,
        directory="~",
        output_function: Callable[[OutputData], NoReturn] = Lambdas.one_arg_no_return,
        use_threaded_worker=False,
        wait_for_locks=True,
        remote_ssh=False,
        timeout: int | None = 30,
        ssh_login_timeout: int | None = 10,
        print_command: bool = False,
        print_prompt: bool = False,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
    ) -> NoReturn:
        """
        :param directory: the directory to use as the current working
            directory
        :param output_function: the output function to use, defaults
            to a NOOP function
        :param use_threaded_worker: if True the entire run command
            method is run in a separate thread
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

        self._is_context_manager: bool = False
        self._is_remote: bool = remote_ssh

        self._ssh_bash = SSHBash(
            directory=directory,
            output_function=output_function,
            use_threaded_worker=use_threaded_worker,
            wait_for_locks=wait_for_locks,
            timeout=timeout,
            ssh_login_timeout=ssh_login_timeout,
            print_command=print_command,
            print_prompt=print_prompt,
            print_ssh_connection_msgs=print_ssh_connection_msgs,
            print_ssh_login_success=print_ssh_login_success,
        )

        self._local_bash = LocalBash(
            directory=directory,
            output_function=output_function,
            use_threaded_worker=use_threaded_worker,
            wait_for_locks=wait_for_locks,
            timeout=timeout,
            print_command=print_command,
            print_prompt=print_prompt,
        )

        # Set the default bash based on if remote_ssh is True or not
        self._bash = self._ssh_bash if remote_ssh else self._local_bash

    # Do not ever make a setter for this as it will cause sync issues
    # and any open ssh connections may not be closed properly
    @property
    def is_remote(self):
        """
        Returns True if the bash is set to run remotely.

        :return: True if the bash is set to run remotely
        """

        return self._is_remote

    def __enter__(self):
        """
        Sets the _is_context_manager variable to True.
        """

        self._is_context_manager = True
        return self

    # noinspection SpellCheckingInspection
    def __exit__(self, etype, value, traceback) -> NoReturn:
        """
        Runs the close method.
        """

        self._bash.close()

    def get_output_writer(self) -> OutputWriter:
        """
        Returns the current output writer instance.

        :return: the current output writer instance
        """

        return self._bash.get_output_writer()

    def get_on_output(self):
        """
        Returns the function that handles the output.

        :return: the function that handles the output
        """

        return self._bash.get_on_output()

    def is_threaded_worker_enabled(self) -> bool:
        """
        Returns True if threaded worker is enabled.

        :return: True if threaded worker is enabled
        """

        return self._bash.is_threaded_worker_enabled()

    def enable_threaded_worker(self):
        """
        Enables the threaded worker.

        :return: this instance to allow for method chaining
        """

        self._bash.enable_threaded_worker()
        return self

    def disable_threaded_worker(self):
        """
        Disables the threaded worker.

        :return: this instance to allow for method chaining
        """

        self._bash.disable_threaded_worker()
        return self

    def is_print_prompt_enabled(self) -> bool:
        """
        Returns True if print prompt is enabled.

        :return: True if print prompt is enabled
        """

        return self._bash.is_print_prompt_enabled()

    def enable_print_prompt(self):
        """
        Enables print prompt.

        :return: this instance to allow for method chaining
        """

        self._bash.enable_print_prompt()
        return self

    def disable_print_prompt(self):
        """
        Disables print prompt.

        :return: this instance to allow for method chaining
        """

        self._bash.disable_print_prompt()
        return self

    def is_print_command_enabled(self) -> bool:
        """
        Returns True if print command is enabled.

        :return: True if print command is enabled
        """

        return self._bash.is_print_command_enabled()

    def enable_print_command(self):
        """
        Enables print command.

        :return: this instance to allow for method chaining
        """

        self._bash.enable_print_command()
        return self

    def disable_print_command(self):
        """
        Disables print command.

        :return: this instance to allow for method chaining
        """

        self._bash.disable_print_command()
        return self

    def is_wait_for_locks_enabled(self) -> bool:
        """
        Returns True if wait for locks is enabled.

        :return: True if wait for locks is enabled
        """

        return self._bash.is_wait_for_locks_enabled()

    def enable_wait_for_locks(self):
        """
        Enables wait for locks.

        :return: this instance to allow for method chaining
        """

        self._bash.enable_wait_for_locks()
        return self

    def disable_wait_for_locks(self):
        """
        Disables wait for locks.

        :return: this instance to allow for method chaining
        """

        self._bash.disable_wait_for_locks()
        return self

    def is_raise_error_on_lock_wait_enabled(self) -> bool:
        """
        Returns True if the program is set to raise an error if a
        command is waiting on a lock.

        :return: True if the program is set to raise an error if a
            command is waiting on a lock
        """

        return self._bash.is_raise_error_on_lock_wait_enabled()

    def enable_raise_error_on_lock_wait(self):
        """
        Enables raising an error if a command is waiting on a lock.

        :return: this instance to allow for method chaining
        """

        self._bash.enable_raise_error_on_lock_wait()
        return self

    def disable_raise_error_on_lock_wait(self):
        """
        Disables raising an error if a command is waiting on a lock.

        :return: this instance to allow for method chaining
        """

        self._bash.disable_raise_error_on_lock_wait()
        return self

    def set_on_output(self, func):
        """
        Sets the function that the output of terminal commands is passed to.

        :param func: the function to set
        :return: this instance to allow for method chaining
        """

        self._bash.set_on_output(func)
        return self

    def get_global_timeout(self) -> int:
        """
        Returns the global timeout.

        :return: the global timeout
        """

        return self._bash.get_global_timeout()

    def set_global_timeout(self, timeout: int):
        """
        Sets the global timeout.

        :param: timeout the timeout to set
        :return: this instance to allow for method chaining
        """

        self._bash.set_global_timeout(timeout)
        return self

    def set_global_timeout_default(self):
        """
        Sets the global timeout back to the default.

        :return: this instance to allow for method chaining
        """

        self._bash.set_global_timeout_default()
        return self

    @property
    def running_dir(self) -> str:
        """
        Returns the directory of the current running program.

        :return: the directory of the current running program
        """

        return self._bash.running_dir()

    def change_dir(self, directory: str) -> NoReturn:
        """
        Changes the current working directory.

        :param: directory the directory to set
        """

        self._bash.change_dir(directory)

    @property
    def current_dir(self) -> str:
        """
        Returns the current working directory.

        :return: the current working directory
        """

        return self._bash.current_dir

    @property
    def home_dir(self) -> str:
        """
        Returns the current user's home directory.

        :return: the current user's home directory
        """

        return self._bash.home_dir

    @property
    def hostname(self) -> str:
        """
        Returns the current system hostname.

        :return: the current system hostname
        """

        return self._bash.hostname

    @property
    def current_user(self) -> str:
        """
        Returns the username of the current user.

        :return: the username of the current user
        """

        return self._bash.current_user

    def print_prompt(self):
        """
        Manually prints to the output a representation of what the
        terminal prompt would look like in the current working
        directory.

        This uses the current user, hostname, current working
        directory and if root, uses '#' instead of '$'.
        """

        self._bash.print_prompt()

    def get_prompt(self) -> str:
        """
        Returns a representation of what the terminal prompt would look
        like in the current working directory.

        This uses the current user, hostname, current working
        directory and if root, uses '#' instead of '$'.

        :return: a representation of what the terminal prompt would look
            like in the current working directory
        """

        return self._bash.get_prompt()

    def set_ssh_login_info(
        self,
        hostname: str = None,
        username: str = None,
        password: str = None,
        port: int = 22,
        ssh_key: StrOrBytesPath = None,
    ):
        """
        Sets the required login info for the ssh connection.

        :param hostname: the network hostname port ip address
            of the computer to connect to
        :param username: the username
        :param password: the password
        :param port: the port (Default is 22)
        :param ssh_key: the ssh auth key filename (Optional)
        """

        if self.is_remote:
            self._ssh_bash.set_ssh_login_info(
                hostname, username, password, port, ssh_key
            )

    def ssh_connect(
        self,
        ssh_login_timeout: int = 10,
        print_prompt: bool = False,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        print_ssh_mod: bool = False,
    ):
        """
        Connects to the ssh client and keeps the connection open.

        :param ssh_login_timeout: the timeout to use for ssh login
        :param print_prompt: if true prints the prompt to the output
        :param print_ssh_connection_msgs: if true prints a message on ssh connect and disconnect
        :param print_ssh_login_success: if true prints a message on ssh login success
        :param print_ssh_mod: if true prints the server's mod(Message of the Day) on login
        """

        if self.is_remote:
            self._ssh_bash.ssh_connect_and_wait(
                ssh_login_timeout,
                print_prompt,
                print_ssh_connection_msgs,
                print_ssh_login_success,
                print_ssh_mod,
            )

    def ssh_close(self, print_ssh_connection_msgs: bool = False):
        """
        Closes the current connection if still open.

        :param print_ssh_connection_msgs: if true prints a message on
            ssh disconnect
        """

        if self.is_remote:
            self._ssh_bash.ssh_close(print_ssh_connection_msgs)

    def run_terminal_command(
        self,
        command: str,
        sudo: bool = False,
        timeout: int | None = 30,
        ssh_login_timeout: int = 10,
        print_command: bool = False,
        print_prompt: bool = False,
        print_exit_code: bool = False,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        reconnect_ssh_if_closed: bool = False,
        create_temp_connection_if_closed: bool = True,
    ):
        """
        Runs the specified terminal command and passes output to
        specified on_output function.

        :param timeout: the timeout to use for all commands
        :param ssh_login_timeout: the timeout to use for ssh login
        :param command: the command to run as a string
        :param sudo: if true appends "sudo" to the beginning of
            the command
        :param print_command: if true prints the command to the output
        :param print_prompt: if true prints the prompt to the output
        :param print_exit_code: if true prints the exit code on a
            new line
        :param print_ssh_connection_msgs: if true prints a message on
            ssh connect and disconnect
        :param print_ssh_login_success: if true prints a message on ssh
            login success
        :param reconnect_ssh_if_closed: if the client has been
            disconnected, reconnect the client and leave the connection
            open when method completes
        :param create_temp_connection_if_closed: if the client has been
            disconnected, reconnect command immediately close when
            method completes. NOTE: if "reconnect_ssh_if_closed" is
            True then this parameter is ignored.
        """

        if self.is_remote:
            self._ssh_bash.run_terminal_command(
                command,
                sudo,
                timeout,
                ssh_login_timeout,
                print_command,
                print_prompt,
                print_exit_code,
                print_ssh_connection_msgs,
                print_ssh_login_success,
                reconnect_ssh_if_closed,
                create_temp_connection_if_closed,
            )
        else:
            self._local_bash.run_terminal_command(
                command, sudo, timeout, print_command, print_prompt, print_exit_code
            )
