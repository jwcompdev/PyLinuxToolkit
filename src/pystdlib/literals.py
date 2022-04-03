# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# literals.py
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

"""Contains string literals."""
import os
from typing import Union

NEW_LINE = os.linesep
FILE_SEPARATOR = os.extsep
PATH_SEPARATOR = os.sep

StrOrBytesPath = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]


# noinspection PyPep8Naming,PyPropertyDefinition,GrazieInspection
class Chars:
    """Contains some basic unicode characters."""

    @classmethod
    @property
    def ACCENT(cls):
        """
        The accent character (^).

        :return: the accent character (^)
        """
        return "^"

    @classmethod
    @property
    def AMPERSAND(cls):
        """
        The ampersand character (&).

        :return: the ampersand character (&)
        """
        return "&"

    @classmethod
    @property
    def ARROWS_LEFT(cls):
        """
        The left double arrow character («).

        :return: the left double arrow character («)
        """
        return "\u00AB"

    @classmethod
    @property
    def ARROWS_RIGHT(cls):
        """
        The right double arrow character (»).

        :return: the right double arrow character (»)
        """
        return "\u00BB"

    @classmethod
    @property
    def ASTERISK(cls):
        """
        The asterisk character (*).

        :return: the asterisk character (*)
        """
        return "*"

    # noinspection SpellCheckingInspection
    @classmethod
    @property
    def ATSIGN(cls):
        """
        The at sign character (@).

        :return: the at sign character (@)
        """
        return "@"

    @classmethod
    @property
    def BACKSLASH(cls):
        """
        The backslash character.

        :return: the backslash character
        """
        return "\\"

    @classmethod
    @property
    def BITCOIN(cls):
        """
        The bitcoin character (₿).

        :return: the bitcoin character (₿)
        """
        return "\u20BF"

    @classmethod
    @property
    def CENTS(cls):
        """
        The cent sign character (¢).

        :return: the cent sign character (¢)
        """
        return "\u00A2"

    @classmethod
    @property
    def COLON(cls):
        """
        The colon character (:).

        :return: the colon character (:)
        """
        return ":"

    @classmethod
    @property
    def COMMA(cls):
        """
        The comma character (,).

        :return: the comma character (,)
        """
        return ","

    @classmethod
    @property
    def COPYRIGHT(cls):
        """
        The copyright character (©).

        :return: the copyright character (©)
        """
        return "\u00A9"

    @classmethod
    @property
    def DOLLAR(cls):
        """
        The dollar currency character ($).

        :return: the dollar currency character ($)
        """
        return "$"

    @classmethod
    @property
    def DOT(cls):
        """
        The dot character (.).

        :return: the dot character (.)
        """
        return "."

    # noinspection SpellCheckingInspection
    @classmethod
    @property
    def DQUOTE(cls):
        """
        The double quote character (").

        :return: the double quote character (")
        """
        return '"'

    @classmethod
    @property
    def ELLIPSIS(cls):
        """
        The ellipsis character (…).

        :return: the ellipsis character (…)
        """
        return "\u2026"

    @classmethod
    @property
    def EMPTY_BRACES(cls):
        """
        An empty set of braces '{}'.

        :return: an empty set of braces '{}'
        """
        return "{}"

    @classmethod
    @property
    def EMPTY_BRACKETS(cls):
        """
        An empty set of brackets '[]'.

        :return: an empty set of brackets '[]'
        """
        return "[]"

    # noinspection SpellCheckingInspection
    @classmethod
    @property
    def EMPTY_DQUOTES(cls):
        """
        An empty set of double quotes ("").

        :return: an empty set of double quotes ("")
        """
        return '""'

    @classmethod
    @property
    def EMPTY_PARENS(cls):
        """
        An empty set of parenthesis. '()'

        :return: an empty set of parenthesis '()'
        """
        return "()"

    # noinspection SpellCheckingInspection
    @classmethod
    @property
    def EMPTY_SQUOTES(cls):
        """
        An empty set of double quotes ('').

        :return: an empty set of double quotes ('')
        """
        return "''"

    @classmethod
    @property
    def EQUALS(cls):
        """
        The equals character (=).

        :return: the equals character (=)
        """
        return "="

    @classmethod
    @property
    def EURO(cls):
        """
        The euro currency character (€).

        :return: the euro currency character (€)
        """
        return "\u20AC"

    @classmethod
    @property
    def EXCLAMATION(cls):
        """
        The exclamation mark character (!).

        :return: the exclamation mark character (!)
        """
        return "!"

    # noinspection SpellCheckingInspection
    @classmethod
    @property
    def FORWARDSLASH(cls):
        """
        The forward slash character (/).

        :return: the forward slash character (/)
        """
        return "/"

    @classmethod
    @property
    def FRAC_HLF(cls):
        """
        The 1/2 fraction character (½).

        :return: the 1/2 fraction character (½)
        """
        return "\u00BD"

    @classmethod
    @property
    def FRAC_QTR(cls):
        """
        The 1/4 fraction character (¼).

        :return: the 1/4 fraction character (¼)
        """
        return "\u00BC"

    @classmethod
    @property
    def FRAC_3QTR(cls):
        """
        The 3/4 fraction character (¾).

        :return: the 3/4 fraction character (¾)
        """
        return "\u00BE"

    @classmethod
    @property
    def GREATER_THAN(cls):
        """
        The greater than character (>).

        :return: the greater than character (>)
        """
        return ">"

    @classmethod
    @property
    def GREATER_THAN_EQUAL(cls):
        """
        The greater than equal character (≥).

        :return: the greater than equal character (≥)
        """
        return "\u2265"

    @classmethod
    @property
    def HASH(cls):
        """
        The hash character (#).

        :return: the hash character (#)
        """
        return "#"

    @classmethod
    @property
    def HYPHEN(cls):
        """
        The hyphen character (-).

        :return: the hyphen character (-)
        """
        return "-"

    @classmethod
    @property
    def LESS_THAN(cls):
        """
        The less than character (<).

        :return: the less than character (<)
        """
        return "<"

    @classmethod
    @property
    def LESS_THAN_EQUAL(cls):
        """
        The less than equal character (≤).

        :return: the less than equal character (≤)
        """
        return "\u2264"

    @classmethod
    @property
    def MICRO(cls):
        """
        The micro character (μ).

        :return: the micro character (μ)
        """
        return "\u03BC"

    @classmethod
    @property
    def MINUS(cls):
        """
        The minus character (-).

        :return: the minus character (-)
        """
        return Chars.HYPHEN

    @classmethod
    @property
    def NEGATIVE_ONE(cls):
        """
        The '-1' character.

        :return: the '-1' character
        """
        return "-1"

    @classmethod
    @property
    def NOT_EQUAL(cls):
        """
        The not equal character (≠).

        :return: the not equal character (≠)
        """
        return "\u2260"

    @classmethod
    @property
    def ONE(cls):
        """
        The '1' character.

        :return: the '1' character
        """
        return "1"

    @classmethod
    @property
    def PARAGRAPH(cls):
        """
        The paragraph symbol character (¶).

        :return: the paragraph symbol character (¶)
        """
        return "\u00B6"

    @classmethod
    @property
    def PERCENT(cls):
        """
        The percent character (%).

        :return: the percent character (%)
        """
        return "%"

    @classmethod
    @property
    def PLUS(cls):
        """
        The plus character (+).

        :return: the plus character (+)
        """
        return "+"

    @classmethod
    @property
    def PLUS_MINUS(cls):
        """
        The plus minus character (±).

        :return: the plus minus character (±)
        """
        return "\u00B1"

    @classmethod
    @property
    def POUND(cls):
        """
        The pound currency character (£).

        :return: the pound currency character (£)
        """
        return "\u00A3"

    @classmethod
    @property
    def POWER(cls):
        """
        The power character (⏻).

        :return: the power character (⏻)
        """
        return "\u23FB"

    @classmethod
    @property
    def QUESTION(cls):
        """
        The question mark character (?).

        :return: the question mark character (?)
        """
        return "?"

    @classmethod
    @property
    def REGISTERED(cls):
        """
        The registered character (®).

        :return: the registered character (®)
        """
        return "\u00AE"

    @classmethod
    @property
    def SEMICOLON(cls):
        """
        The semicolon character (;).

        :return: the semicolon character (;)
        """
        return ";"

    @classmethod
    @property
    def SPACE(cls):
        """
        The single space character ( ).

        :return: the single space character ( )
        """
        return " "

    @classmethod
    @property
    def SQUOTE(cls):
        """
        The single quote character (').

        :return: the single quote character (')
        """
        return "'"

    @classmethod
    @property
    def TAB(cls):
        """
        The tab character.

        :return: the tab character
        """
        return "\t"

    @classmethod
    @property
    def TILDE(cls):
        """
        The tilde character (~).

        :return: the tilde character (~)
        """
        return "~"

    @classmethod
    @property
    def TRADEMARK(cls):
        """
        The trademark character (™).

        :return: the trademark character (™)
        """
        return "\u2122"

    @classmethod
    @property
    def UNDERSCORE(cls):
        """
        The underscore character (_).

        :return: the underscore character (_)
        """
        return "_"

    @classmethod
    @property
    def VERTICAL(cls):
        """
        The vertical bar character (|).

        :return: the vertical bar character (|)
        """
        return "|"

    @classmethod
    @property
    def YEN(cls):
        """
        The yen currency character (¥).

        :return: the yen currency character (¥)
        """
        return "\u00A5"

    @classmethod
    @property
    def ZERO(cls):
        """
        The '0' character.

        :return: the '0' character
        """
        return "0"


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
    if field_name is None or field_name == "":
        raise ValueError("'field_name' cannot be None or empty!")

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
    if field_name is None or field_name == "":
        raise ValueError("'field_name' cannot be None or empty!")

    if field_name.lower() == "value":
        return VALUE_CANNOT_BE_NONE
    if field_name.lower() == "input":
        return INPUT_CANNOT_BE_NONE
    return field_name.title() + CANNOT_BE_NONE_OR_EMPTY
