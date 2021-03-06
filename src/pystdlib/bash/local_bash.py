# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# local_bash.py
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
Contains the LocalBash class, a bash terminal emulator that
allows running commands locally.
"""
from __future__ import annotations

import logging
import os
import pwd
import socket
from pathlib import Path
from typing import NoReturn, Callable

import pexpect
from pexpect import spawn

from pystdlib.bash import BashValueError
from pystdlib.bash.bash_base import BashBase
from pystdlib.bash.bash_command import BashCommand
from pystdlib.bash.output import OutputData
from pystdlib.logged import Logged
from pystdlib.lambdas import Lambdas
from pystdlib.task_pool import TaskPool
from pystdlib.values import StringValue


class LocalBash(BashBase, Logged):
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
        self.set_log_level(logging.DEBUG)

        self.change_dir(directory)

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

    def _internal_run_local_command_string(
        self, command: str, client: spawn
    ) -> StringValue:
        client.sendline(command)
        client.expect_exact(self.get_prompt())
        before = client.before.replace(command, "").strip("\r\n")
        self._commands.add_command(BashCommand(command, self.current_dir, before, 0))
        self._debug(f"Created BashCommand: {str(self._commands.get_last())}")
        return StringValue(before)

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

        result_msg = ""

        if not result:
            result_msg = f"bash: cd: {new_dir}: No such file or directory"
            self._output_writer.write_bypass(StringValue(result_msg))

        self._commands.add_command(
            BashCommand(command, self.current_dir, result_msg, 0)
        )
        self._debug(f"Created BashCommand: {str(self._commands.get_last())}")

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
        if sudo and not command.startswith("sudo "):
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
                client.expect_exact(self.get_prompt())

                # Runs the requested command
                self._debug(f"Running command '{command}'...")
                client.sendline(command)

                # This must be here to catch the prompt
                # after the command completes
                client.expect_exact(self.get_prompt())

                result = client.before

                client.logfile_read = None

                self._debug(f"Retrieving exit code from command '{command}'...")
                exit_code = self._internal_run_local_command_string("echo $?", client)

                exit_code = (
                    StringValue(exit_code).replace("\n", "").replace("\r", "").strip()
                )

                self._debug(f"Saving output of '{command}' to BashCommands...")
                command_obj = BashCommand(
                    command, self.current_dir, result, exit_code.to_int()
                )
                self._commands.add_command(command_obj)
                self._debug(f"Created BashCommand: {str(self._commands.get_last())}")
                self._debug(f"Output was:\n{self._commands.get_last().output}")

                if print_exit_code:
                    self._output_writer.write(exit_code)

                # Exits the bash
                client.sendline("exit")
                client.expect(pexpect.EOF)

                self._debug(f"Running command '{command}' complete!")
