# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# RaspberryPi.py
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
This file contains the RaspberryPi class.
"""
import os
import pwd
import socket
from typing import NoReturn

from attr import validators, define
from attrs import field

from pylinuxtoolkit.bash.LinuxBash import LinuxBash


@define
class RaspberryPi:
    remote: bool = field(validator=validators.instance_of(bool))
    bash: LinuxBash = LinuxBash()

    # ssh_config: SSH_Config
    # interface_config: Interface_Config
    # system_config: System_Config
    # performance_config: Performance_Config
    # localization_config: Localization_Config

    @property
    def hostname(self) -> str:
        return socket.gethostname()

    @property
    def current_user(self) -> str:
        return pwd.getpwuid(os.getuid()).pw_name

    # def __enter__(self):
    #     pass
    #
    # def __exit__(self, _type, value, traceback):
    #     pass


pi = RaspberryPi(False)
print(pi.hostname)
print(pi.bash.current_user)


def on_output(value: str) -> NoReturn:
    pass


def on_error(value: str) -> NoReturn:
    pass

