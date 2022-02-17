# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# vnc_resolutions.py
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
Contains the VNCResolutions class,
an enum of VNC resolution sizes.
"""
from pylinuxtoolkit.utils.str_enum import StrEnum


class VNCResolutions(StrEnum):
    """A list of all available screen resolutions for the VNC connections"""
    NONE = ""
    SIZE_640_X_480 = "600x480"
    SIZE_720_X_480 = "720x480"
    SIZE_800_X_600 = "800x600"
    SIZE_1024_X_768 = "1024x768"
    SIZE_1280_X_720 = "1280x720"
    SIZE_1280_X_1024 = "1280x1024"
    SIZE_1600_X_1200 = "1600x1200"
    SIZE_1920_X_1080 = "1920x1080"


# print(VNC_Resolutions.Size_1600x1200)
# print(VNC_Resolutions.value_exists("1920x1080"))
# print(VNC_Resolutions.key_exists("Size_1920x1080"))
# print(VNC_Resolutions.Size_1920x1080 == "1920x1080")
# print(VNC_Resolutions.get_value(VNC_Resolutions.Size_1920x1080))
