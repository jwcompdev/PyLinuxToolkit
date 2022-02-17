# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# raspberry_pi.py
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

"""Contains the RaspberryPi class."""
from __future__ import annotations

import os
import pwd
import socket
from abc import ABC
from typing import NoReturn

from pylinuxtoolkit.bash.linux_bash import LinuxBash


class RaspberryPi:
    """
    This is the main raspberry pi data class.
    """

    def __init__(self, remote: bool = False) -> NoReturn:
        self._remote: bool = remote
        self._bash: LinuxBash = LinuxBash()
        self._interface_config: InterfaceConfig = InterfaceConfig(self)
        self._localization_config: LocalizationConfig = LocalizationConfig(self)
        self._performance_config: PerformanceConfig = PerformanceConfig(self)
        self._ssh_config: SSHConfig = SSHConfig(self)
        self._system_config: SystemConfig = SystemConfig(self)

    # ssh_config: SSH_Config
    # interface_config: Interface_Config
    # system_config: System_Config
    # performance_config: Performance_Config
    # localization_config: Localization_Config

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

    @property
    def bash(self) -> LinuxBash:
        """
        Returns the linux bash instance.

        :return: the linux bash instance
        """

        return self._bash

    @property
    def interface(self) -> InterfaceConfig:
        """
        Returns the interface config instance.

        :return: the interface config instance
        """
        return self._interface_config

    @property
    def localization(self) -> LocalizationConfig:
        """
        Returns the localization config instance.

        :return: the localization config instance
        """
        return self._localization_config

    @property
    def performance(self) -> PerformanceConfig:
        """
        Returns the performance config instance.

        :return: the performance config instance
        """
        return self._performance_config

    @property
    def ssh(self) -> SSHConfig:
        """
        Returns the ssh config instance.

        :return: the ssh config instance
        """
        return self._ssh_config

    @property
    def system(self) -> SystemConfig:
        """
        Returns the system config instance.

        :return: the system config instance
        """
        return self._system_config


class BaseConfig(ABC):
    """
    This is the base class for all RPI Config objects
    """

    def __init__(self, rpi: RaspberryPi):
        """
        Initializes the base config.

        :param rpi: the root raspberry pi_obj object
        """

        self._command_base: str = "sudo raspi-config nonint "
        self.__pi: RaspberryPi = rpi

    def _run_str_command(self, command: str) -> str:
        # if self.__pi.isLocal():
        #     pass
        #         return pi.getLocalBash()
        #                 .runTerminalCommandString(command, pi.getLocalBash().getRoot());
        #     } else {
        #         if(!pi.getSSHConfig().getClient().isConnected()) {
        #             if(!pi.connectSSH()) {
        #                 throw new IllegalStateException("Unable to connect to pi!");
        #             }
        #         }
        #
        #         var result = pi.getSSHConfig().getClient().runCommand(command);
        #         if(result.getLeft().size() == 0) return "";
        #         return result.getLeft().get(0);
        #     }
        pass

    def _run_str_list_command(self, command: str) -> ():
        pass

    def _run_bool_command(self, command: str) -> bool:
        pass

    def _run_int_command(self, command: str) -> int:
        pass


# protected final RaspberryPi pi;
#     protected final String commandBase = "sudo raspi-config nonint ";
#
#     public ConfigBase(final RaspberryPi pi) {
#         this.pi = pi;
#     }
#
#     protected String runStringCommand(final String command) {
#         if(pi.isLocal()) {
#             return pi.getLocalBash()
#                     .runTerminalCommandString(command, pi.getLocalBash().getRoot());
#         } else {
#             if(!pi.getSSHConfig().getClient().isConnected()) {
#                 if(!pi.connectSSH()) {
#                     throw new IllegalStateException("Unable to connect to pi!");
#                 }
#             }
#
#             var result = pi.getSSHConfig().getClient().runCommand(command);
#             if(result.getLeft().size() == 0) return "";
#             return result.getLeft().get(0);
#         }
#     }
#
#     protected ArrayList<String> runStringListCommand(final String command) {
#         if(pi.isLocal()) {
#             return pi.getLocalBash()
#                     .runTerminalCommandStringList(command, pi.getLocalBash().getRoot());
#         } else {
#             if(!pi.getSSHConfig().getClient().isConnected()) {
#                 if(!pi.connectSSH()) {
#                     throw new IllegalStateException("Unable to connect to pi!");
#                 }
#             }
#
#             var result = pi.getSSHConfig().getClient().runCommand(command);
#             return result.getLeft();
#         }
#     }
#
#     protected boolean runBooleanCommand(final String command) {
#         if(pi.isLocal()) {
#             int result = pi.getLocalBash()
#                     .runTerminalCommand(command, pi.getLocalBash().getRoot());
#
#             return result == 0;
#         } else {
#             if(!pi.getSSHConfig().getClient().isConnected()) {
#                 if(!pi.connectSSH()) {
#                     throw new IllegalStateException("Unable to connect to pi!");
#                 }
#             }
#
#             var result = pi.getSSHConfig().getClient().runCommand(command);
#             if(result.getLeft().size() == 0) {
#                 var resultInt = result.getRight();
#                 return resultInt == 0;
#             }
#             var resultStr = result.getLeft().get(0);
#             var resultInt = Integer.parseInt(resultStr);
#             return resultInt == 0;
#         }
#     }
#
#     protected int runIntCommand(final String command) {
#         if(pi.isLocal()) {
#             return pi.getLocalBash()
#                     .runTerminalCommand(command, pi.getLocalBash().getRoot());
#         } else {
#             if(!pi.getSSHConfig().getClient().isConnected()) {
#                 if(!pi.connectSSH()) {
#                     throw new IllegalStateException("Unable to connect to pi!");
#                 }
#             }
#
#             var result = pi.getSSHConfig().getClient().runCommand(command);
#             return Integer.parseInt(result.getLeft().get(0));
#         }
#     }


class InterfaceConfig(BaseConfig):
    """
    This config object contains all the interface related settings.
    """


class LocalizationConfig(BaseConfig):
    """
    This config object contains all the localization related settings.
    """


class PerformanceConfig(BaseConfig):
    """
    This config object contains all the performance related settings.
    """


class SSHConfig(BaseConfig):
    """
    This config object contains all the ssh related settings.
    """


class SystemConfig(BaseConfig):
    """
    This config object contains all the system related settings.
    """


pi = RaspberryPi(False)
print(f"System Hostname: {pi.hostname}")
print(f"Current Username: {pi.current_user}")
