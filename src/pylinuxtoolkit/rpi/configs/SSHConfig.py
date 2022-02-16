# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# SSHConfig.py
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
This file contains the SSHConfig class.
"""
from pylinuxtoolkit.rpi import RaspberryPi
from pylinuxtoolkit.rpi.configs import BaseConfig


class SSHConfig(BaseConfig):
    def __init__(self, pi: RaspberryPi):
        super().__init__(pi)
