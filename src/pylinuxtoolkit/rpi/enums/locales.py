# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# locales.py
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
Contains the Locales class, an enum of Locale values.
"""
from pylinuxtoolkit.utils.str_enum import StrEnum


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
