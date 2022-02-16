# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# BaseConfig.py
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
This file contains the BaseConfig class.
"""
from abc import ABC

from attr import define

from pylinuxtoolkit.rpi import RaspberryPi


@define
class BaseConfig(ABC):
    _command_base: str = "sudo raspi-config nonint "

    def __init__(self, pi: RaspberryPi):
        self.__pi: RaspberryPi = pi

    def _run_str_command(self, command: str) -> str:
        if self.__pi.isLocal():
            pass
            #     return pi.getLocalBash()
            #             .runTerminalCommandString(command, pi.getLocalBash().getRoot());
            # } else {
            #     if(!pi.getSSHConfig().getClient().isConnected()) {
            #         if(!pi.connectSSH()) {
            #             throw new IllegalStateException("Unable to connect to pi!");
            #         }
            #     }
            #
            #     var result = pi.getSSHConfig().getClient().runCommand(command);
            #     if(result.getLeft().size() == 0) return "";
            #     return result.getLeft().get(0);
            # }

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
