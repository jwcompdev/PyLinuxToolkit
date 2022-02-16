# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# Locales.py
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
This file contains the Locales class, an enum of Locale values.
"""
from pylinuxtoolkit.utils.StrEnum import StrEnum


class Locales(StrEnum):
    """A list of all available locales"""
    NONE = ""
    Arabic_Egypt = "ar-EG.UTF-8"
    Bengali_India = "bn-IN.UTF-8"
    Chinese_Simplified = "zh_CN.UTF-8"
    Chinese_Traditional = "zh_TW.UTF-8"
    Danish_Denmark = "da-DK.UTF-8"
    English_CA = "en_CA.UTF-8"
    English_UK = "en_GB.UTF-8"
    English_US = "en_US.UTF-8"
    French = "fr_FR.UTF-8"
    German = "de_DE.UTF-8"
    Hebrew = "he_IL.UTF-8"
    Italian = "it_IT.UTF-8"
    Japanese = "ja_JP.UTF-8"
    Korean = "ko_KR.UTF-8"
    Portuguese_Brazilian = "pt_BR.UTF-8"
    Russian = "ru-RU.UTF-8"
    Spanish_Mexico = "es_MX.UTF-8"
    Spanish_Spain = "es_ES.UTF-8"
