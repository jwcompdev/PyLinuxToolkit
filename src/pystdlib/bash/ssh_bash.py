# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# ssh_bash.py
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
Contains the SSHBash class, a bash terminal emulator that
allows running commands over ssh.
"""
from __future__ import annotations

import logging
from typing import NoReturn, Optional, Callable

import pexpect
from pexpect import pxssh

from pystdlib.bash import BashValueError, BashConnectionError
from pystdlib.bash.bash_base import BashBase
from pystdlib.bash.bash_command import BashCommand
from pystdlib.bash.output import OutputData
from pystdlib.logged import Logged
from pystdlib.lambdas import Lambdas
from pystdlib.literals import StrOrBytesPath
from pystdlib.task_pool import TaskPool
from pystdlib.values import StringValue


class SSHBash(BashBase, Logged):
    """A bash terminal emulator that allows running commands over ssh."""

    def __init__(
        self,
        directory="~",
        output_function: Callable[[OutputData], NoReturn] = Lambdas.one_arg_no_return,
        use_threaded_worker=False,
        wait_for_locks=True,
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
        :param timeout: the timeout for all commands when they are run,
            can be set to None to disable the timeout
        :param ssh_login_timeout: the timeout for the ssh login,
            can be set to None to disable the timeout
        :param print_command: prints the current command to the output
            before the command output actually prints
        :param print_prompt: prints the prompt after the command output
            prints
        :param print_ssh_connection_msgs: if True prints all connecting
            and disconnected messages wait_for_locks the ssh connection
        :param print_ssh_login_success: if True prints success message
            on successful ssh login

        """
        super().__init__(
            directory=directory,
            output_function=output_function,
            use_threaded_worker=use_threaded_worker,
            wait_for_locks=wait_for_locks,
            remote_ssh=True,
            timeout=timeout,
            print_command=print_command,
            print_prompt=print_prompt,
        )

        self._is_context_manager = False
        self.set_log_level(logging.DEBUG)

        # SSH specific params
        self._ssh_hostname: Optional[str] = None
        self._ssh_internal_hostname: Optional[str] = None
        self._ssh_username: Optional[str] = None
        self._ssh_password: Optional[str] = None
        self._ssh_port: int = 22
        self._ssh_key: Optional[str] = None
        self._ssh_cwd: Optional[str] = None
        self._ssh_home: Optional[str] = None
        self._ssh_client = pxssh.pxssh(encoding="utf-8", timeout=timeout)
        self.ssh_login_timeout: int = ssh_login_timeout
        self.print_ssh_connection_msgs: bool = print_ssh_connection_msgs
        self.print_ssh_login_success: bool = print_ssh_login_success

        self._bash_data.current_user = self.current_user
        self._bash_data.client = self._ssh_client

    def __enter__(self) -> SSHBash:
        """Sets the _is_context_manager variable to True."""
        self._is_context_manager = True
        return self

    # noinspection SpellCheckingInspection
    def __exit__(self, etype, value, traceback) -> NoReturn:
        """Runs the close method."""
        self.close()

    def set_ssh_login_info(
        self,
        hostname: str,
        username: str,
        password: str = None,
        port: int = 22,
        ssh_key: StrOrBytesPath = None,
    ) -> NoReturn:
        """
        Sets the required login info for the ssh connection.

        :param hostname: the network hostname port ip address
            of the computer to connect to
        :param username: the username
        :param password: the password
        :param port: the port (Default is 22)
        :param ssh_key: the ssh auth key filename (Optional)
        """
        self._ssh_hostname = hostname
        self._ssh_username = username
        self._ssh_password = password
        self._ssh_port = port
        self._ssh_key = ssh_key

    def change_dir(self, directory: str) -> NoReturn:
        """
        Changes the current working directory.

        :param directory: the directory to set
        """
        self._internal_run_ssh_command_string("cd " + directory, self._ssh_client)
        self._ssh_cwd = self._internal_run_ssh_command_string("pwd", self._ssh_client)

    @property
    def current_dir(self) -> str:
        """
        Returns the current working directory.

        :return: the current working directory
        """
        return self._ssh_cwd

    @property
    def home_dir(self) -> str:
        """
        Returns the current user's home directory.

        :return: the current user's home directory
        """
        return self._ssh_home

    @property
    def hostname(self) -> str:
        """
        Returns the current system hostname.

        :return: the current system hostname
        """
        return self._ssh_internal_hostname

    @property
    def current_user(self) -> str:
        """
        Returns the username of the current user.

        :return: the username of the current user
        """
        return self._ssh_username

    def is_ssh_closed(self) -> bool:
        """
        Returns True if the ssh client is closed.

        :return: True if the ssh client is closed
        """
        return self._ssh_client.closed

    # noinspection PyTypeChecker
    @TaskPool.decide_class_task(
        pool_name="_task_pool", threaded="is_threaded_worker_enabled"
    )
    def ssh_connect_and_wait(
        self,
        ssh_login_timeout: int = 10,
        print_prompt: bool = None,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        print_ssh_mod: bool = False,
    ) -> NoReturn:
        """
        Connects to the ssh client and keeps the connection open.

        :param ssh_login_timeout: the timeout to use for ssh login
        :param print_prompt: if true prints the prompt to the output
        :param print_ssh_connection_msgs: if true prints a message on
            ssh connect and disconnect
        :param print_ssh_login_success: if true prints a message on
            ssh login success
        :param print_ssh_mod: if true prints the server's
            mod(Message of the Day) on login
        """
        self._ssh_connect_and_wait(
            ssh_login_timeout,
            print_prompt,
            print_ssh_connection_msgs,
            print_ssh_login_success,
            print_ssh_mod,
        )

    def _ssh_connect_and_wait(
        self,
        ssh_login_timeout: int = 10,
        print_prompt: bool = None,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        print_ssh_mod: bool = False,
    ) -> NoReturn:
        """
        Connects to the ssh client and keeps the connection open.

        NOTE: This method is never ran threaded.

        :param ssh_login_timeout: the timeout to use for ssh login
        :param print_prompt: if true prints the prompt to the output
        :param print_ssh_connection_msgs: if true prints a message on
            ssh connect and disconnect
        :param print_ssh_login_success: if true prints a message on
            ssh login success
        :param print_ssh_mod: if true prints the server's
            mod(Message of the Day) on login
        """
        if self._ssh_hostname is None or self._ssh_hostname == "":
            raise BashValueError("SSH Hostname was not provided and is required!")

        if self._ssh_username is None or self._ssh_username == "":
            raise BashValueError("SSH Username was not provided and is required!")

        try:
            self._debug("Starting class-wide connection...")
            if ssh_login_timeout == 10:
                ssh_login_timeout = self.ssh_login_timeout

            print_ssh_connection_msgs = (
                print_ssh_connection_msgs
                if print_ssh_connection_msgs
                else self.print_ssh_connection_msgs
            )
            print_ssh_login_success = (
                print_ssh_login_success
                if print_ssh_login_success
                else self.print_ssh_login_success
            )

            self._bash_data.command = ""
            self._bash_data.current_user = self._ssh_username
            self._bash_data.print_command = False

            self._internal_connect(
                self._ssh_client,
                ssh_login_timeout,
                print_prompt,
                print_ssh_connection_msgs,
                print_ssh_login_success,
                print_ssh_mod,
            )
        except pexpect.exceptions.EOF:
            # This should only happen when force quitting the program
            # while connected to the client
            pass

    def _internal_connect(
        self,
        client: pxssh,
        ssh_login_timeout: int = 10,
        print_prompt: bool = None,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        print_ssh_mod: bool = False,
    ):
        self._debug(f"Connecting to {self._ssh_username}@{self._ssh_hostname}...")
        if print_ssh_connection_msgs:
            self._output_writer.write(f"SSH Connecting to {self._ssh_hostname}!")

        if print_ssh_mod:
            client.logfile_read = self._output_writer
        else:
            client.logfile_read = None

        client.login(
            server=self._ssh_hostname,
            username=self._ssh_username,
            password=self._ssh_password,
            port=self._ssh_port,
            ssh_key=self._ssh_key,
            login_timeout=ssh_login_timeout,
        )

        self._debug(f"Login with {self._ssh_username}@{self._ssh_hostname} succeeded!")
        if print_ssh_login_success:
            self._output_writer.write(f"SSH Login with {self._ssh_username} succeeded!")

        client.logfile_read = None

        # Retrieves basic setting values
        self._debug("Requesting hostname, cwd and home dir...")
        self._ssh_internal_hostname = self._internal_run_ssh_command_string(
            "hostname", client
        )
        self._ssh_cwd = self._internal_run_ssh_command_string("pwd", client)
        self._ssh_home = self._internal_run_ssh_command_string("echo ~", client)

        if print_prompt is not None:
            self._bash_data.print_prompt = print_prompt

        # Assign values to the BashData object for access in on_output function
        self._bash_data.client = client

        # Starts command output
        client.logfile_read = self._output_writer

        # Print the prompt to the output
        if self._bash_data.print_prompt:
            self._output_writer.write(self.get_prompt())

        self._debug("Connection complete!")

    @TaskPool.decide_class_task(
        pool_name="_task_pool", threaded="is_threaded_worker_enabled"
    )
    def ssh_close(self, print_ssh_connection_msgs: bool = False):
        """
        Closes the ssh connection if still open.

        :param print_ssh_connection_msgs: if true prints a message on
            ssh disconnect
        """
        if not self._ssh_client.closed:
            print_ssh_connection_msgs = (
                print_ssh_connection_msgs
                if print_ssh_connection_msgs
                else self.print_ssh_connection_msgs
            )

            self._bash_data.command = ""

            self._internal_disconnect(print_ssh_connection_msgs)

    def _internal_disconnect(self, print_ssh_connection_msgs: bool = False):
        try:
            self._debug(
                f"Disconnecting from {self._ssh_username}@{self._ssh_hostname}..."
            )
            old_print_command = self._bash_data.print_command
            self._bash_data.print_command = False

            # Stops command output
            self._ssh_client.logfile_read = None

            # Logout of server and close client
            self._ssh_client.logout()

            # This should always be true but let's check just in case
            if self._ssh_client.closed:
                self._debug("Disconnected!")
                if print_ssh_connection_msgs:
                    self._output_writer.write("SSH Disconnected!")
            else:
                raise BashConnectionError("SSH connection failed to close!")

            self._bash_data.print_command = old_print_command
        except pexpect.exceptions.EOF:
            # This should only happen when force quitting the program
            # while connected to the client
            self._debug("SSH connection interrupted because of SIGINT!")

    def _internal_run_ssh_command_string(self, command: str, client: pxssh) -> str:
        client.sendline(command)
        client.prompt()
        before = client.before.replace(command, "").strip("\r\n")
        self._commands.add_command(BashCommand(command, self.current_dir, before, 0))
        self._debug(f"Created BashCommand: {str(self._commands.get_last())}")
        return before

    def _internal_run_command(
        self,
        client: pxssh,
        command: str,
        print_command: bool,
        print_exit_code: bool,
        refresh_working_dir: bool,
    ):
        # Assign values to the BashData object for access in on_output function
        self._bash_data.command = command

        if print_command is not None:
            self._bash_data.print_command = print_command

        # Starts command output
        client.logfile_read = self._output_writer

        self._debug(f"Running command '{command}'...")
        # Runs the requested command
        client.sendline(command)
        client.prompt()

        result = (
            StringValue(client.before)
            .strip_ansi_codes()
            .replace(command, "")
            .strip("\r\n")
        )

        # Stops command output
        client.logfile_read = None

        self._debug(f"Retrieving exit code from command '{command}'...")
        exit_code = self._internal_run_ssh_command_string("echo $?", client)

        self._debug(f"Saving output of '{command}' to BashCommands...")
        command_obj = BashCommand(command, self.current_dir, result, int(exit_code))
        self._commands.add_command(command_obj)
        self._debug(f"Created BashCommand: {str(self._commands.get_last())}")
        self._debug(f"Output was:\n{self._commands.get_last().output}")

        if print_exit_code:
            self._output_writer.write(exit_code)

        if refresh_working_dir:
            self._debug("Refreshing cwd...")
            self._ssh_cwd = self._internal_run_ssh_command_string("pwd", client)

        # Print the prompt to the output
        if self._bash_data.print_prompt:
            self._output_writer.write_bypass(self.get_prompt())

        self._debug(f"Running command '{command}' complete!")

    def close(self) -> NoReturn:
        """Closes the ssh connection if still open."""
        self.ssh_close()

    @TaskPool.decide_class_task(
        pool_name="_task_pool", threaded="is_threaded_worker_enabled"
    )
    def run_terminal_command(
        self,
        command: str,
        sudo: bool = False,
        timeout: int | None = 30,
        ssh_login_timeout: int = 10,
        print_command: bool = None,
        print_prompt: bool = None,
        print_exit_code: bool = False,
        print_ssh_connection_msgs: bool = False,
        print_ssh_login_success: bool = False,
        reconnect_ssh_if_closed: bool = True,
        create_temp_connection_if_closed: bool = False,
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
        if not command:
            raise BashValueError("Command must be specified!")

        if sudo and not command.startswith("sudo "):
            command = "sudo " + command

        if timeout == 30:
            timeout = self._timeout

        if ssh_login_timeout == 10:
            ssh_login_timeout = self.ssh_login_timeout

        print_ssh_connection_msgs = (
            print_ssh_connection_msgs
            if print_ssh_connection_msgs
            else self.print_ssh_connection_msgs
        )

        print_ssh_login_success = (
            print_ssh_login_success
            if print_ssh_login_success
            else self.print_ssh_login_success
        )

        bypass_connect = False

        try:
            if not self._ssh_client.closed:
                # If the connection is open then send the command
                self._ssh_client.timeout = timeout
                bypass_connect = True
            elif reconnect_ssh_if_closed:
                # If the connection is not open then reconnect and then send the command
                self._ssh_client = pxssh.pxssh(encoding="utf-8", timeout=timeout)
                self._ssh_connect_and_wait(
                    ssh_login_timeout=ssh_login_timeout,
                    print_prompt=print_prompt,
                    print_ssh_connection_msgs=print_ssh_connection_msgs,
                    print_ssh_login_success=print_ssh_login_success,
                    print_ssh_mod=False,
                )
                bypass_connect = True
            elif create_temp_connection_if_closed:
                # If the connection is not open then connect just for this command
                # and then send the command
                with pxssh.pxssh(encoding="utf-8", timeout=timeout) as client:
                    self._internal_connect(
                        client,
                        ssh_login_timeout,
                        print_prompt,
                        print_ssh_connection_msgs,
                        print_ssh_login_success,
                        False,
                    )

                    self._internal_run_command(
                        client, command, print_command, print_exit_code, False
                    )

                    self._internal_disconnect(print_ssh_connection_msgs)
            else:
                raise BashConnectionError("Connection closed!")

            if bypass_connect:
                if print_prompt is not None:
                    self._bash_data.print_prompt = print_prompt

                self._internal_run_command(
                    self._ssh_client, command, print_command, print_exit_code, True
                )
        except pexpect.exceptions.EOF:
            # This should only happen when force quitting the program
            # while connected to the client
            pass
