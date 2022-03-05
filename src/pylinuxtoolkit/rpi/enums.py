# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# locales.py
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

"""Contains the enums required for the RaspberryPi object."""
from pystdlib.str_enum import StrEnum


class Locales(StrEnum):
    """A list of all available locales"""

    NONE = ""
    ARABIC_EGYPT = "ar-EG.UTF-8"
    BENGALI_INDIA = "bn-IN.UTF-8"
    CHINESE_SIMPLIFIED = "zh_CN.UTF-8"
    CHINESE_TRADITIONAL = "zh_TW.UTF-8"
    DANISH_DENMARK = "da-DK.UTF-8"
    ENGLISH_CA = "en_CA.UTF-8"
    ENGLISH_UK = "en_GB.UTF-8"
    ENGLISH_US = "en_US.UTF-8"
    FRENCH = "fr_FR.UTF-8"
    GERMAN = "de_DE.UTF-8"
    HEBREW = "he_IL.UTF-8"
    ITALIAN = "it_IT.UTF-8"
    JAPANESE = "ja_JP.UTF-8"
    KOREAN = "ko_KR.UTF-8"
    PORTUGUESE_BRAZILIAN = "pt_BR.UTF-8"
    RUSSIAN = "ru-RU.UTF-8"
    SPANISH_MEXICO = "es_MX.UTF-8"
    SPANISH_SPAIN = "es_ES.UTF-8"


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


if __name__ == "__main__":
    print(VNCResolutions.SIZE_1600_X_1200)
    print(VNCResolutions.value_exists("1920x1080"))
    print(VNCResolutions.key_exists("Size_1920x1080"))
    print(VNCResolutions.SIZE_1920_X_1080 == "1920x1080")
