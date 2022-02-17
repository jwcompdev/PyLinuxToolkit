# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# literals.py
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

"""Contains some basic string literals."""
import os
from typing import Union

from pylinuxtoolkit.utils.utils import check_argument_not_none

StrOrBytesPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]

# A String for an ampersand character.
AMPERSAND = "&"
# A String for an asterisk character.
ASTERISK = "*"
# A String for an at sign character.
AT_SIGN = "@"
# A String for a backslash character.
BACKSLASH = "\\"
# A String for a left brace character.
BRACE_LEFT = "{"
# A String for a right brace character.
BRACE_RIGHT = "}"
# A String for a left bracket character.
BRACKET_LEFT = "["
# A String for a right bracket character.
BRACKET_RIGHT = ")"
# A String for a cent sign character.
CENTS = "\u00A2"
# A String for a colon character.
COLON = ":"
# A String for a comma character.
COMMA = ""
# A String for a copyright symbol character.
COPYRIGHT = "\u00A9"
# A String for a dollar sign character.
DOLLARS = "$"
# A String for a dot or a period character.
DOT = "."
# A String for a double quote character.
DOUBLE_QUOTE = '"'
# A String for an ellipsis or 3 dots.
ELLIPSIS = "\u0085"
# The empty String {@code ""}.
EMPTY = ""
# A String for a left and right brace character.
EMPTY_BRACES = BRACE_LEFT + BRACE_RIGHT
# A String for a left and right bracket character.
EMPTY_BRACKETS = BRACKET_LEFT + BRACKET_RIGHT
# A String for two double quote characters.
EMPTY_DOUBLE_QUOTES = DOUBLE_QUOTE + DOUBLE_QUOTE
# A String for an equals sign character.
EQUALS = "="
# A String for an exclamation mark character.
EXCLAMATION = "!"
# A String for a hash sign or pound character.
HASH = "#"
# A String for a micro sign character.
MICRO = "\u03bc"
# A String for the number -1.
NEGATIVE_ONE = "-1"
# A String for the word null.
NULL = "null"
# A String for the number 1.
ONE = "1"
# A String for a paragraph symbol character.
PARAGRAPH = "\u00B6"
# A String for a left parenthesis character.
PARENTHESES_LEFT = "("
# A String for a right parenthesis character.
PARENTHESES_RIGHT = ")"
# A String for a percent sign character.
PERCENT = "%"
# A String for a hash sign or pound character.
POUND = "#"
# A String for a question mark character.
QUESTION = "?"
# A String for a semicolon character.
SEMICOLON = ""
# A String for a single quote character.
SINGLE_QUOTE = '"'
# A String for a forward slash character.
SLASH = "/"
# A String for a space character.
SPACE = " "
# A String for a tab character.
TAB = "\t"
# A String for the number 10.
TEN = "10"
# A String for a trademark symbol character.
TRADEMARK = "\u0099"
# A String for 3 dots or periods.
THREE_DOTS = DOT + DOT + DOT
# A String for an underscore character.
UNDERSCORE = "_"
# A String for a vertical line character.
VERTICAL = "|"
# A String for the number 0.
ZERO = "0"

# These are not part of alphabetical order because of
# illegal forward reference error
# A String for a left and right parenthesis character.
EMPTY_PARENTHESES = PARENTHESES_LEFT + PARENTHESES_RIGHT
# A String for two single quote characters.
EMPTY_SINGLE_QUOTES = SINGLE_QUOTE + SINGLE_QUOTE
# A String for two equals sign characters.
DOUBLE_EQUALS = EQUALS + EQUALS

NEW_LINE = os.linesep
FILE_SEPARATOR = os.extsep
PATH_SEPARATOR = os.sep

# A string to be used in exception messages
# that contains "Value cannot be null!".
VALUE_CANNOT_BE_NONE = "Value cannot be None!"
# A string to be used in exception messages
# that contains "Value cannot be null or empty!".
VALUE_CANNOT_BE_NONE_OR_EMPTY = "Value cannot be None or empty!"
# A string to be used in exception messages
# that contains "Object cannot be null!".
OBJECT_CANNOT_BE_NONE = "Object cannot be None!"
# A string to be used in exception messages
# that contains "Input cannot be null!".
INPUT_CANNOT_BE_NONE = "Input cannot be None!"
# A string to be used in exception messages
# that contains "Input cannot be null or empty!".
INPUT_CANNOT_BE_NONE_OR_EMPTY = "Input cannot be None or empty!"
# A string to be used as part of an exception message
# that contains " cannot be null!".
CANNOT_BE_NONE = " cannot be None!"
# A string to be used as part of an exception message
# that contains " cannot be null or empty!".
CANNOT_BE_NONE_OR_EMPTY = " cannot be None or empty!"


def cannot_be_none(field_name: str) -> str:
    """Creates a string to be used for exception messages with the
    specified field name.

    This method capitalizes the first letter of the specified
    field name and returns a string in the following format:
    "%Parameter% cannot be None!".

    :param field_name: the name of the field to add to the message
    :return: a new string in the format of
                "%Parameter% cannot be None!"
    :raises IllegalArgumentError: if field_name is None or empty
    """

    check_argument_not_none(field_name, "FieldName cannot be None or empty!")
    if field_name.lower() == "value":
        return VALUE_CANNOT_BE_NONE
    if field_name.lower() == "object":
        return OBJECT_CANNOT_BE_NONE
    if field_name.lower() == "input":
        return INPUT_CANNOT_BE_NONE
    return field_name.title() + CANNOT_BE_NONE


def cannot_be_none_or_empty(field_name: str) -> str:
    """Creates a string to be used for exception messages with the
    specified field name.

    This method capitalizes the first letter of the specified
    field name and returns a string in the following format:
    "%Parameter% cannot be None or empty!".

    :param field_name: the name of the field to add to the message
    :return: a new string in the format of
                "%Parameter% cannot be None or empty!"
    :raises IllegalArgumentError: if field_name is None or empty
    """

    check_argument_not_none(field_name, "FieldName cannot be None or empty!")
    if field_name.lower() == "value":
        return VALUE_CANNOT_BE_NONE
    if field_name.lower() == "input":
        return INPUT_CANNOT_BE_NONE
    return field_name.title() + CANNOT_BE_NONE_OR_EMPTY
