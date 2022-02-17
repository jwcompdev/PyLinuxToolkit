# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# local_bash.py
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
Contains the LocalBash class, a bash terminal emulator that
allows running commands locally.
"""
from __future__ import annotations

import os
import pwd
import socket
from pathlib import Path
from typing import NoReturn, Callable

import pexpect
from pexpect import spawn

from pylinuxtoolkit.bash.bash_base import BashBase
from pylinuxtoolkit.bash.bash_exceptions import BashValueError
from pylinuxtoolkit.bash.output_data import OutputData
from pylinuxtoolkit.utils.lambdas import Lambdas
from pylinuxtoolkit.utils.task_pool import TaskPool
from pylinuxtoolkit.utils.values import StringValue


class LocalBash(BashBase):
    """A bash terminal emulator that allows running commands locally."""

    def __init__(
        self,
        directory="~",
        output_function: Callable[[OutputData], NoReturn] = Lambdas.one_arg_no_return,
        use_threaded_worker=False,
        wait_for_locks=True,
        timeout: int | None = 30,
        print_command: bool = False,
        print_prompt: bool = False,
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
        :param timeout: the timeout for all commands when they are run,
            can be set to None to disable the timeout
        :param print_command: prints the current command to the output
            before the command output actually prints
        :param print_prompt: prints the prompt after the command output
            prints
        """

        super().__init__(
            directory=directory,
            output_function=output_function,
            use_threaded_worker=use_threaded_worker,
            wait_for_locks=wait_for_locks,
            remote_ssh=False,
            timeout=timeout,
            print_command=print_command,
            print_prompt=print_prompt,
        )

        self._is_context_manager = False

        self.change_dir(directory)

        self._bash_data.prompt_func = self.get_prompt
        self._bash_data.current_user = self.current_user

    def __enter__(self) -> LocalBash:
        """Sets the _is_context_manager variable to True."""

        self._is_context_manager = True
        return self

    # noinspection SpellCheckingInspection
    def __exit__(self, etype, value, traceback) -> NoReturn:
        """Runs the close method."""

        self.close()

    def change_dir(self, directory: str) -> bool:
        """
        Changes the current working directory.

        :param directory: the directory to set
        :return: False if the directory doesn't exist
        """

        try:
            self._new_dir = directory.replace("~", str(Path.home()))

            os.chdir(self._new_dir)

            return True
        except FileNotFoundError:
            return False

    @property
    def current_dir(self) -> str:
        """
        Returns the current working directory

        :return: the current working directory
        """

        return str(Path.cwd())

    @property
    def home_dir(self) -> str:
        """
        Returns the current user's home directory.

        :return: the current user's home directory
        """

        return str(Path.home())

    @property
    def hostname(self) -> str:
        """
        Returns the current system hostname.

        :return: the current system hostname
        """

        return socket.gethostname()

    @property
    def current_user(self) -> str:
        """
        Returns the username of the current user.

        :return: the username of the current user
        """

        return pwd.getpwuid(os.getuid()).pw_name

    @staticmethod
    def _internal_run_local_command_string(command: str, client: spawn) -> str:
        client.sendline(command)
        client.expect("[$]")
        return client.before.replace(command, "").strip("\r\n")

    def close(self) -> NoReturn:
        """Currently does nothing."""

    def _handle_cd_command(
        self, command: str, print_command: bool = None, print_prompt: bool = None
    ) -> NoReturn:
        self._bash_data.command = command

        if print_command is not None:
            self._bash_data.print_command = print_command
        if print_prompt is not None:
            self._bash_data.print_prompt = print_prompt

        new_dir = command.replace("sudo", "").replace("cd ", "").strip()

        result = self.change_dir(new_dir)

        if print_command:
            self._output_writer.write_bypass(StringValue(command))

        if not result:
            self._output_writer.write_bypass(
                StringValue(f"bash: cd: {new_dir}: No such file or directory")
            )

        if print_prompt:
            self._output_writer.write_bypass(StringValue(self.get_prompt()))

    @TaskPool.decide_class_task(
        pool_name="_task_pool", threaded="is_threaded_worker_enabled"
    )
    def run_terminal_command(
        self,
        command: str,
        sudo: bool = False,
        timeout: int | None = 30,
        print_command: bool = None,
        print_prompt: bool = None,
        print_exit_code: bool = False,
    ) -> NoReturn:
        """
        Runs the specified terminal command and passes output to
        class init specified on_output function.

        :param command: the command to run as a string
        :param sudo: if true appends "sudo" to the beginning of
            the command
        :param timeout: the timeout to use for all commands
        :param print_command: if true prints the command to the output
        :param print_prompt: if true prints the prompt to the output
        :param print_exit_code: if true prints the exit code on a
            new line
        :return: the result of the command
        """

        if not command:
            raise BashValueError("Command must be specified!")
        if sudo:
            if not command.startswith("sudo "):
                command = "sudo " + command

        if command.replace("sudo", "").startswith("cd"):
            self._handle_cd_command(command, print_command, print_prompt)
        else:
            if timeout == 30:
                timeout = self._timeout

            with pexpect.spawn(
                command="bash", encoding="utf-8", timeout=timeout, echo=False
            ) as client:
                # Assign values to the BashData object
                # for access in on_output function
                self._bash_data.command = command
                self._bash_data.client = client

                if print_command is not None:
                    self._bash_data.print_command = print_command

                if print_prompt is not None:
                    self._bash_data.print_prompt = print_prompt

                if (
                    self._bash_data.print_prompt
                    and self._output_writer.get_last_line() == ""
                ):
                    self._output_writer.write_bypass(StringValue(self.get_prompt()))

                if self._bash_data.print_command:
                    self._output_writer.write_bypass(StringValue(command))

                # Starts command output
                client.logfile_read = self._output_writer

                client.setecho(False)
                client.waitnoecho()

                # This must be here to catch the first prompt
                client.expect("[$]")

                # Runs the requested command
                if print_exit_code:
                    client.sendline(command + " ; echo $?")
                else:
                    client.sendline(command)

                # This must be here to catch the prompt
                # after the command completes
                client.expect("[$]")

                # Exits the bash
                client.sendline("exit")
                client.expect(pexpect.EOF)
