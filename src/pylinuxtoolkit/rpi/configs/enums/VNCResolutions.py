# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# VNCResolutions.py
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
This file contains the VNCResolutions class,
an enum of VNC resolution sizes.
"""
from pylinuxtoolkit.utils.StrEnum import StrEnum


class VNCResolutions(StrEnum):
    """A list of all available screen resolutions for the VNC connections"""
    NONE = ""
    Size_640x480 = "600x480"
    Size_720x480 = "720x480"
    Size_800x600 = "800x600"
    Size_1024x768 = "1024x768"
    Size_1280x720 = "1280x720"
    Size_1280x1024 = "1280x1024"
    Size_1600x1200 = "1600x1200"
    Size_1920x1080 = "1920x1080"


# print(VNC_Resolutions.Size_1600x1200)
# print(VNC_Resolutions.value_exists("1920x1080"))
# print(VNC_Resolutions.key_exists("Size_1920x1080"))
# print(VNC_Resolutions.Size_1920x1080 == "1920x1080")
# print(VNC_Resolutions.get_value(VNC_Resolutions.Size_1920x1080))
