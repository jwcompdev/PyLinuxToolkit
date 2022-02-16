# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# RegEx.py
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
This file contains the Patterns class that contains multiple RegEx
patters for use with re methods.
"""
import re


class Patterns:
    """
    Contains basic RegEx patterns to use for re methods.
    """

    ANSI_BASIC_ESCAPE = re.compile(r"(\x9b|\x1b\[)[0-?]*[ -/]*[@-~]")

    ALL_DIGITS = re.compile(r"\d")

    ALL_NON_DIGITS = re.compile(r"\D")

    ALL_WORDS = re.compile(r"\w")

    ALL_NEW_LINES = re.compile(r"\n")

    ALL_TABS = re.compile(r"\t")

    ALL_RETURNS = re.compile(r"\r")

    ALL_WHITESPACE = re.compile(r"\s")

    ALL_ALPHANUMERIC = re.compile(r"[a-zA-Z0-9]*")

    ALL_WHOLE_NUMBERS = re.compile(r"\d+")

    ALL_DECIMAL_NUMBERS = re.compile(r"\d*\.\d+")

    EMAIL_ADDRESS = re.compile(
        r"(([a-zA-Z0-9._%-]+)@(([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,6})))*"
    )

    URL = re.compile(
        r"(https?://)?(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#?&/=]*)"
    )

    URL_HTTPS = re.compile(
        r"https?://(www\.)?[-a-zA-Z0-9@:%._+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_+.~#()?&/=]*)"
    )

    IPV4 = re.compile(
        r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    )

    IPV6 = re.compile(
        r"(([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}"
        r"|([0-9a-fA-F]{1,4}:){1,7}:"
        r"|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}"
        r"|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}"
        r"|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}"
        r"|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}"
        r"|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}"
        r"|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})"
        r"|:((:[0-9a-fA-F]{1,4}){1,7}|:)"
        r"|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]+"
        r"|::(ffff(:0{1,4})?:)?((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]"
        r"|(2[0-4]|1?[0-9])?[0-9])"
        r"|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1?[0-9])?[0-9])\.){3}(25[0-5]"
        r"|(2[0-4]|1?[0-9])?[0-9]))"
    )

    IPV4AND6 = re.compile(
        r"((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}"
        r"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)"
        r"|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))"
        r"|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}"
        r"|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})"
        r"|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})"
        r"|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})"
        r"|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})"
        r"|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}"
        r"(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:"
        r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))"
        r"|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})"
        r"|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:)"
        r"(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:"
        r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))"
        r"|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:"
        r"((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)"
        r"(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))"
    )

    TIME12HR = re.compile(r"(0?[1-9]|1[0-2]):[0-5][0-9]")

    TIME12HR_AM_PM = re.compile(r"((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))")

    TIME24HR_W_SECONDS = re.compile(r"(?:[01]\d|2[0123]):[012345]\d:[012345]\d")

    TIME24HR_LEAD0 = re.compile(r"(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]")

    TIME24HR_LEAD0_OPT = re.compile(r"([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]")

    HTML_TAG = re.compile(r"</?[\w\s]*>|<.+[\W]>")

    ZIP_CODE_US = re.compile(r"\d{5}([ \-]\d{4})?")

    ZIP_CODE_CA = re.compile(
        r"[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d"
    )

    SS_NUMBER = re.compile(
        r"((?!219-09-9999|078-05-1120)"
        r"(?!666|000|9\d{2})\d{3}-(?!00)\d{2}-(?!0{4})\d{4})"
        r"|((?!219 09 9999|078 05 1120)"
        r"(?!666|000|9\d{2})\d{3} (?!00)\d{2} (?!0{4})\d{4})"
        r"|((?!219099999|078051120)"
        r"(?!666|000|9\d{2})\d{3}(?!00)\d{2}(?!0{4})\d{4})"
    )

    PASSPORT_NUMBER = re.compile(r"[A-PR-WY][1-9]\d\s?\d{4}[1-9]")
