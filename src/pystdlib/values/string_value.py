from __future__ import annotations

import _collections_abc
import re
from typing import SupportsInt, SupportsFloat, Iterator, Sequence, SupportsIndex, Mapping, TYPE_CHECKING, Iterable

from pystdlib import Chars
from pystdlib.protocols import SupportsStringFull, SupportsIntFloatStr
from pystdlib.regex import Patterns
from pystdlib.str_utils import build_repr
from pystdlib.utils import check_argument_type
from pystdlib.values.value import Value

if TYPE_CHECKING:
    from pystdlib.values.boolean_value import BooleanValue
    from pystdlib.values.integer_value import IntegerValue
    from pystdlib.values.float_value import FloatValue


class StringValue(Value, _collections_abc.Sequence, SupportsInt, SupportsFloat):
    """Provides mutable access to a str"""

    def __init__(self, value: SupportsStringFull | StringValue = ""):
        """
        Initializes the StringValue object.

        NOTE: if the initial value is not a valid string or another
        StringValue object then the value is converted to a string
        and then stored.

        :param value: the initial string value.
            The default is an empty string.
        """
        self._value = StringValue._verify_string(value)

    @staticmethod
    def _verify_string(value: SupportsStringFull | StringValue = "") -> str:
        if isinstance(value, str):
            return value

        if isinstance(value, StringValue):
            return value._value

        return str(value)

    ########################################
    # Dunder Methods                       #
    ########################################

    # Must return a str
    def __str__(self) -> str:
        return self._value

    # Must return a str
    def __repr__(self) -> str:
        return build_repr(self, self._value)

    # Must return str
    def __format__(self, format_spec) -> str:
        return self._value.__format__(format_spec)

    # Must return int
    def __int__(self) -> int:
        return int(self._value)

    # Must return float
    def __float__(self) -> float:
        return float(self._value)

    # Must return complex
    def __complex__(self) -> complex:
        return complex(self._value)

    # Must return Iterator[str]
    def __iter__(self) -> Iterator[str]:
        """Implement iter(self)."""
        return iter(self._value)

    def __getnewargs__(self) -> tuple[str]:
        return self._value.__getnewargs__()

    def __eq__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        """
        Returns True if the value is equal to the specified value,
        False otherwise.

        :param other: the value to check
        :return: True if the value is equal to the specified value,
            False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(other, StringValue):
            return BooleanValue(self._value == other.get())

        return BooleanValue(self._value == other)

    def __ne__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        value, False otherwise.

        :param other: the value to check
        :return: True if the value is not equal to the specified value,
            False otherwise.
        """
        return self.__eq__(other).negate()

    def __lt__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(other, str):
            return BooleanValue(self._value < other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value < other.get())

        type_name = type(other).__name__
        raise TypeError("'<' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __le__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(other, str):
            return BooleanValue(self._value <= other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value <= other.get())

        type_name = type(other).__name__
        raise TypeError("'<=' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __gt__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(other, str):
            return BooleanValue(self._value > other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value > other.get())

        type_name = type(other).__name__
        raise TypeError("'>' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __ge__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(other, str):
            return BooleanValue(self._value >= other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value >= other.get())

        type_name = type(other).__name__
        raise TypeError("'>=' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    # Must return bool
    def __contains__(self, other: str | StringValue) -> bool:
        """Return key in self."""
        if isinstance(other, str):
            return other in self._value

        if isinstance(other, StringValue):
            return other.get() in self._value

        type_name = type(other).__name__
        raise TypeError("'in <StringValue>' requires string or "
                        "StringValue as left operand, not " + type_name)

    # Must return str
    def __getitem__(self, key: int | IntegerValue | slice) -> str:
        """Return self[key]."""
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(key, IntegerValue):
            return str(self._value[key.get()])

        return str(self._value[key])

    # Must return int
    def __len__(self) -> int:
        """Return len(self)."""
        return len(self._value)

    def __iadd__(self,
                 other: (SupportsIntFloatStr | IntegerValue
                         | FloatValue | StringValue)) \
            -> StringValue:
        from pystdlib.values.integer_value import IntegerValue
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float, IntegerValue, FloatValue)):
            self._value += str(other)
            return self

        if isinstance(other, str):
            self._value += other
            return self

        if isinstance(other, StringValue):
            self._value += other.get()
            return self

        type_name = type(other).__name__
        raise TypeError("'can only concatenate str or "
                        f"StringValue (not \"{type_name}\") to StringValue")

    def __add__(self,
                other: (SupportsIntFloatStr | IntegerValue
                        | FloatValue | StringValue)) \
            -> StringValue:
        from pystdlib.values.integer_value import IntegerValue
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float, IntegerValue, FloatValue)):
            return StringValue(self._value + str(other))

        if isinstance(other, str):
            return StringValue(self._value + other)

        if isinstance(other, StringValue):
            return StringValue(self._value + other.get())

        type_name = type(other).__name__
        raise TypeError("'can only concatenate str or "
                        f"StringValue (not \"{type_name}\") to StringValue")

    def __radd__(self,
                 other: (SupportsIntFloatStr | IntegerValue
                         | FloatValue | StringValue)) \
            -> StringValue:
        from pystdlib.values.integer_value import IntegerValue
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float, IntegerValue, FloatValue)):
            return StringValue(str(other) + self._value)

        if isinstance(other, str):
            return StringValue(other + self._value)

        if isinstance(other, StringValue):
            return StringValue(other.get() + self._value)

        type_name = type(other).__name__
        raise TypeError("'can only concatenate str or "
                        f"StringValue (not \"{type_name}\") to StringValue")

    def __isub__(self, other: int | str | IntegerValue | StringValue) \
            -> StringValue:
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(other, int):
            if other >= 0:
                self._value = self._value[other:]
            else:
                self._value = self._value[:other]
        elif isinstance(other, IntegerValue):
            if other >= 0:
                self._value = self._value[other.get():]
            else:
                self._value = self._value[:other.get()]
        elif isinstance(other, str):
            self._value = self._value.replace(other, "")
        elif isinstance(other, StringValue):
            self._value = self._value.replace(other.get(), "")
        else:
            return NotImplemented
        return self

    def __sub__(self,
                other: int | str | IntegerValue | StringValue | re.Pattern) \
            -> StringValue:
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(other, int):
            if other >= 0:
                return StringValue(self._value[other:])

            return StringValue(self._value[:other])

        if isinstance(other, IntegerValue):
            if other >= 0:
                return StringValue(self._value[other.get():])

            return StringValue(self._value[:other.get()])

        if isinstance(other, str):
            return StringValue(self._value.replace(other, ""))

        if isinstance(other, StringValue):
            return StringValue(self._value.replace(other.get(), ""))

        if isinstance(other, re.Pattern):
            return StringValue(other.sub("", self._value))

        return NotImplemented

    def __rsub__(self, other: str | StringValue) \
            -> StringValue:
        if isinstance(other, str):
            return StringValue(other.replace(self._value, ""))

        if isinstance(other, StringValue):
            return StringValue(other.get().replace(self._value, ""))

        return NotImplemented

    def __imul__(self, other: SupportsIndex) \
            -> StringValue:
        if isinstance(other, SupportsIndex):
            self._value *= other.__index__()
            return self

        type_name = type(other).__name__
        raise TypeError("can't multiply sequence by non-int "
                        f"of type '{type_name}'")

    def __mul__(self, other: SupportsIndex) \
            -> StringValue:
        if isinstance(other, SupportsIndex):
            return StringValue(self._value * other.__index__())

        type_name = type(other).__name__
        raise TypeError("can't multiply sequence by non-int "
                        f"of type '{type_name}'")

    def __rmul__(self, other: SupportsIndex) \
            -> StringValue:
        if isinstance(other, SupportsIndex):
            return StringValue(self._value * other.__index__())

        type_name = type(other).__name__
        raise TypeError("can't multiply sequence by non-int "
                        f"of type '{type_name}'")

    def __mod__(self, args) -> StringValue:
        return StringValue(self._value % args)

    def __rmod__(self, template) -> StringValue:
        return StringValue(str(template) % self._value)

    ########################################
    # Built-in Instance Methods            #
    ########################################

    # noinspection PyPropertyDefinition,PyPep8Naming
    @classmethod
    @property
    def EMPTY(cls) -> StringValue:
        """
        Returns an empty string as a StringValue.

        :return: an empty string as a StringValue
        """
        return StringValue("")

    @property
    def value(self):
        """
        Returns the value.

        :return: the value
        """
        return self._value

    def get(self) -> str:
        """
        Returns the value.

        :return: the value
        """
        return self._value

    def set(self, value: SupportsStringFull | StringValue) -> StringValue:
        """
        Sets the value.

        :param value: the value to set
        :return: this instance for use in method chaining
        """
        self._value = StringValue._verify_string(value)
        return self

    def is_equal_to(
            self, value: SupportsStringFull | StringValue) -> BooleanValue:
        """
        Returns True if the value is equal to the specified value,
        False otherwise.

        :param value: the value to check
        :return: True if the value is equal to the specified value,
            False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(value, StringValue):
            return BooleanValue(self._value == value._value)

        return BooleanValue(self._value == value)

    def is_not_equal_to(
            self, value: SupportsStringFull | StringValue) -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        value, False otherwise.

        :param value: the value to check
        :return: True if the value is not equal to the specified value,
            False otherwise.
        """
        return self.is_equal_to(value).negate()

    def append(self, text: SupportsStringFull | StringValue) -> StringValue:
        """
        Appends the specified string to the end of the value.

        :param text: the value to append
        :return: this instance for use in method chaining
        """
        self._value += text
        return self

    # noinspection SpellCheckingInspection
    def appendprefix(self, prefix: SupportsStringFull | StringValue) -> StringValue:
        """
        Appends the specified prefix to the beginning of the value.

        :param prefix: the value to append
        :return: this instance for use in method chaining
        """
        self._value += prefix
        return self

    # noinspection SpellCheckingInspection
    def appendsuffix(self, suffix: SupportsStringFull | StringValue) -> StringValue:
        """
        Appends the specified string to the end of the value.

        :param suffix: the value to append
        :return: this instance for use in method chaining
        """
        self._value += suffix
        return self

    def capitalize(self) -> StringValue:
        """
        Capitalize the value.

        More specifically, make the first character have uppercase and
        the rest lowercase.

        :return: this instance for use in method chaining
        """
        self._value = self._value.capitalize()
        return self

    # noinspection SpellCheckingInspection
    def casefold(self) -> StringValue:
        """
        Make the value a version suitable for case-less comparisons.

        :return: this instance for use in method chaining
        """
        self._value = self._value.casefold()
        return self

    def center(self, width: SupportsIndex,
               fill_char: str | StringValue = Chars.SPACE) -> StringValue:
        """
        Make the value a centered string of length width.

        Padding is done using the specified fill character
        (default is a space).

        :param width: the width of the new string
        :param fill_char: the character to pad the string with
        :return: this instance for use in method chaining
        """
        if isinstance(fill_char, StringValue):
            self._value = self._value.center(width, fill_char._value)
        else:
            self._value = self._value.center(width, fill_char)
        return self

    def count(self, sub: str | StringValue,
              start: SupportsIndex | None = None,
              end: SupportsIndex | None = None) -> IntegerValue:
        """
        Returns the number of non-overlapping occurrences of substring
        sub in string S[start:end].

        Optional arguments start and end are interpreted as in slice
        notation.

        :param sub: the substring to check for
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: the number of non-overlapping occurrences of substring
            sub in string S[start:end]
        """
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(sub, StringValue):
            return IntegerValue(self._value.count(sub._value, start, end))

        return IntegerValue(self._value.count(sub, start, end))

    def encode(self, encoding: str | StringValue = "utf-8", errors: str = "strict") \
            -> bytes:
        """
        Encode the string using the codec registered for encoding.

        :param encoding: The encoding in which to encode the string.
        :param errors:
            The error handling scheme to use for encoding errors.
            The default is 'strict' meaning that encoding errors raise
            a UnicodeEncodeError.  Other possible values are 'ignore',
            'replace' and 'xmlcharrefreplace' as well as any other name
            registered with codecs.register_error that can handle
            UnicodeEncodeErrors.
        :return: the encoded string in bytes
        """
        if isinstance(encoding, StringValue):
            return self._value.encode(encoding._value, errors)

        return self._value.encode(encoding, errors)

    def endswith(self, suffix: str | StringValue | tuple[str],
                 start: SupportsIndex | None = None,
                 end: SupportsIndex | None = None) -> BooleanValue:
        """
        Return True if the value ends with the specified suffix,
        False otherwise.
        With optional start, test the value beginning at that position.
        With optional end, stop comparing S at that position.
        Parameter 'suffix' can also be a tuple of strings to try.

        :param suffix: the suffix to check for
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: true if the value ends with the specified suffix,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(suffix, StringValue):
            return BooleanValue(self._value.endswith(suffix._value, start, end))

        return BooleanValue(self._value.endswith(suffix, start, end))

    def expandtabs(self, tabsize: (str | StringValue
                                   | SupportsIndex) = "8") \
            -> StringValue:
        """
        Make all tab characters annotations in value expanded using
        spaces.

        If tabsize is not given, a tab size of 8 characters is assumed.
        :param tabsize: the number of spaces to expand the tabs to
        :return: this instance for use in method chaining
        """
        if isinstance(tabsize, StringValue):
            self._value = self._value.expandtabs(tabsize._value)
        else:
            self._value = self._value.expandtabs(tabsize)
        return self

    def find(self, sub: str | StringValue,
             start: SupportsIndex | None = None,
             end: SupportsIndex | None = None) -> IntegerValue:
        """
        Return the lowest index in the value where substring sub is
        found, such that sub is contained within S[start:end].
        Optional arguments start and end are interpreted as in slice
        notation.

        Return -1 on failure.

        :param sub: the substring to check for
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: the lowest index in the value where the substring is
            found
        """
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(sub, StringValue):
            return IntegerValue(self._value.find(sub._value, start, end))

        return IntegerValue(self._value.find(sub, start, end))

    def format(self, *args, **kwargs) -> StringValue:
        """
        Return a formatted version of the value
        using substitutions from args and kwargs.
        The substitutions are identified by braces ('{' and '}').

        :param args: the args
        :param kwargs: the keyword args
        :return: this instance for use in method chaining
        """
        self._value = self._value.format(*args, **kwargs)
        return self

    def format_map(self, mapping) -> StringValue:
        """
        Return a formatted version of the value,
        using substitutions from mapping.
        The substitutions are identified by braces ('{' and '}').

        :param mapping: the mapping of substitutions
        :return: this instance for use in method chaining
        """
        self._value = self._value.format_map(mapping)
        return self

    def index(self, sub: str | StringValue,
              start: SupportsIndex | None = None,
              end: SupportsIndex | None = None) -> IntegerValue:
        """
        Return the lowest index in value where substring sub is found,
        such that sub is contained within value[start:end].  Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.

        :param sub: the substring to check
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: the lowest index in the value where the substring
            is found
        :raises ValueError: when the substring is not found
        """
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(sub, StringValue):
            return IntegerValue(self._value.index(sub._value, start, end))

        return IntegerValue(self._value.index(sub, start, end))

    def isalnum(self) -> BooleanValue:
        """
        Return True if the string is an alphanumeric string,
        False otherwise.

        A string is alphanumeric if all characters in the string are
        alphanumeric and there is at least one character in the string.

        :return: True if the string is an alphanumeric string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isalnum())

    def isalpha(self) -> BooleanValue:
        """
        Return True if the string is an alphabetic string,
        False otherwise.

        A string is alphabetic if all characters in the string are
        alphabetic and there is at least one character in the string.

        :return: True if the string is an alphabetic string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isalpha())

    def isascii(self) -> BooleanValue:
        """
        Return True if all characters in the string are ASCII,
        False otherwise.

        ASCII characters have code points in the range U+0000-U+007F.
        Empty string is ASCII too.

        :return: True if all characters in the string are ASCII,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isascii())

    def isdecimal(self) -> BooleanValue:
        """
        Return True if the string is a decimal string,
        False otherwise.

        A string is a decimal string if all characters in the string
        are decimal and there is at least one character in the string.

        :return: True if the string is a decimal string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isdecimal())

    def isdigit(self) -> BooleanValue:
        """
        Return True if the string is a digit string,
        False otherwise.

        A string is a digit string if all characters in the string are
        digits and there is at least one character in the string.

        :return: True if the string is a digit string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isdigit())

    # noinspection SpellCheckingInspection
    def isidentifier(self) -> BooleanValue:
        """
        Return True if the string is a valid Python identifier,
        False otherwise.

        Call keyword.iskeyword(s) to test whether string s is a
        reserved identifier, such as "def" or "class".

        :return: True if the string is a valid Python identifier,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isidentifier())

    def islower(self) -> BooleanValue:
        """
        Return True if the string is a lowercase string,
        False otherwise.

        A string is lowercase if all cased characters in the string
        are lowercase and there is at least one cased character in
        the string.

        :return: True if the string is a lowercase string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.islower())

    def isnumeric(self) -> BooleanValue:
        """
        Return True if the string is a numeric string,
        False otherwise.

        A string is numeric if all characters in the string are numeric
        and there is at least one character in the string.

        :return: True if the string is a numeric string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isnumeric())

    # noinspection SpellCheckingInspection
    def isprintable(self) -> BooleanValue:
        """
        Return True if the string is printable, False otherwise.

        A string is printable if all of its characters are considered
        printable in repr() or if it is empty.

        :return: True if the string is printable,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isprintable())

    def isspace(self) -> BooleanValue:
        """
        Return True if the string is a whitespace string,
        False otherwise.

        A string is whitespace if all characters in the string are
        whitespace and there is at least one character in the string.

        :return: True if the string is a whitespace string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isspace())

    def istitle(self) -> BooleanValue:
        """
        Return True if the string is a title-cased string,
        False otherwise.

        In a title-cased string, upper- and title-case characters may
        only follow uncased characters and lowercase characters only
        cased ones.

        :return: True if the string is a title-cased string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.istitle())

    def isupper(self) -> BooleanValue:
        """
        Return True if the string is an uppercase string,
        False otherwise.

        A string is uppercase if all cased characters in the string are
        uppercase and there is at least one cased character in the
        string.

        :return: True if the string is an uppercase string,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value.isupper())

    def join(self, *args: Iterable[str]) -> StringValue:
        """
        Concatenate the value with any number of strings.

        The value is inserted in between each given string.
        The result is returned as a new string.

        Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'

        :param args: the values to join
        :return: this instance for use in method chaining
        """
        self._value = self._value.join(*args)
        return self

    # noinspection SpellCheckingInspection
    def ljust(self, width: SupportsIndex,
              fill_char: str | StringValue = Chars.SPACE) -> StringValue:
        """
        Return a left-justified string of length width.

        Padding is done using the specified fill character
        (default is a space).

        :param width: the width of the new string
        :param fill_char: the character to pad the string with
        :return: this instance for use in method chaining
        """
        if isinstance(fill_char, StringValue):
            self._value = self._value.ljust(width, fill_char._value)
        else:
            self._value = self._value.ljust(width, fill_char)
        return self

    def lower(self) -> StringValue:
        """
        Return a copy of the string converted to lowercase.

        :return: this instance for use in method chaining
        """
        self._value = self._value.lower()
        return self

    # noinspection SpellCheckingInspection
    def lstrip(self, chars: str | StringValue | None = None) -> StringValue:
        """
        Return a copy of the string with leading whitespace removed.

        If chars is given and not None, remove characters in chars
        instead.

        :param chars: if not none, remove these characters instead
        :return: this instance for use in method chaining
        """
        if isinstance(chars, StringValue):
            self._value = self._value.lstrip(chars._value)
        else:
            self._value = self._value.lstrip(chars)
        return self

    maketrans = str.maketrans

    def partition(self, sep: str | StringValue) -> tuple[str, str, str]:
        """
        Partition the string into three parts using the given
        separator.

        This will search for the separator in the string.
        If the separator is found, returns a 3-tuple containing the
        part before the separator, the separator itself, and the part
        after it.

        If the separator is not found, returns a 3-tuple containing the
        original string and two empty strings.

        :param sep: the seperator to partition the string with
        :return: the partitioned string
        """
        if isinstance(sep, StringValue):
            return self._value.partition(sep._value)

        return self._value.partition(sep)

    # noinspection SpellCheckingInspection
    def removeprefix(self, prefix: str | StringValue) -> StringValue:
        """
        Return a str with the given prefix string removed if present.

        If the string starts with the prefix string, return
        string[len(prefix):].
        Otherwise, return a copy of the original string.

        :param prefix: the prefix to remove
        :return: this instance for use in method chaining
        """
        if isinstance(prefix, StringValue):
            self._value = self._value.removeprefix(prefix._value)
        else:
            self._value = self._value.removeprefix(prefix)
        return self

    # noinspection SpellCheckingInspection
    def removesuffix(self, suffix: str | StringValue) -> StringValue:
        """
        Return a str with the given suffix string removed if present.

        If the string ends with the suffix string and that suffix is
        not empty, return string[:-len(suffix)]. Otherwise, return a
        copy of the original string.

        :param suffix: the suffix to remove
        :return: this instance for use in method chaining
        """
        if isinstance(suffix, StringValue):
            self._value = self._value.removesuffix(suffix._value)
        else:
            self._value = self._value.removesuffix(suffix)
        return self

    def replace(self, old: str | StringValue,
                new: str | StringValue,
                count: SupportsIndex = -1) -> StringValue:
        """
        Return a copy with all occurrences of substring old replaced
        by new.

        If the optional argument count is given, only the first count
        occurrences are replaced.

        :param old: the string to replace
        :param new: the string to replace the old text with
        :param count: the maximum number of occurrences to replace.
            -1 (the default value) means replace all occurrences.
        :return: this instance for use in method chaining
        """
        if isinstance(old, StringValue):
            old = old.get()
        if isinstance(new, StringValue):
            new = new.get()
        self._value = self._value.replace(old, new, count)
        return self

    def rfind(self, sub: str | StringValue,
              start: SupportsIndex | None = None,
              end: SupportsIndex | None = None) -> IntegerValue:
        """
        Return the highest index in the value where substring sub is
        found, such that sub is contained within S[start:end]. Optional
        arguments start and end are interpreted as in slice notation.

        Return -1 on failure.

        :param sub: the substring to check
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: the highest index in the value where the substring is
            found
        """
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(sub, StringValue):
            return IntegerValue(self._value.rfind(sub._value, start, end))

        return IntegerValue(self._value.rfind(sub, start, end))

    # noinspection SpellCheckingInspection
    def rindex(self, sub: str | StringValue,
               start: SupportsIndex | None = None,
               end: SupportsIndex | None = None) -> IntegerValue:
        """
        Return the highest index in the value where substring sub is
        found, such that sub is contained within S[start:end]. Optional
        arguments start and end are interpreted as in slice notation.

        Raises ValueError when the substring is not found.

        :param sub: the substring to check
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: the highest index in the value where the substring is
            found
        :raises ValueError: when the substring is not found
        """
        from pystdlib.values.integer_value import IntegerValue
        if isinstance(sub, StringValue):
            return IntegerValue(self._value.rindex(sub._value, start, end))

        return IntegerValue(self._value.rindex(sub, start, end))

    # noinspection SpellCheckingInspection
    def rjust(self, width: SupportsIndex,
              fill_char: str | StringValue = Chars.SPACE) -> StringValue:
        """
        Return a right-justified string of length width.

        Padding is done using the specified fill character
        (default is a space).

        :param width: the width of the new string
        :param fill_char: the character to pad the string with
        :return: this instance for use in method chaining
        """
        if isinstance(fill_char, StringValue):
            self._value = self._value.rjust(width, fill_char._value)
        else:
            self._value = self._value.rjust(width, fill_char)
        return self

    # noinspection SpellCheckingInspection
    def rpartition(self, sep: str | StringValue) -> tuple[str, str, str]:
        """
        Partition the string into three parts using the given separator.

        This will search for the separator in the string, starting at
        the end. If the separator is found, returns a 3-tuple
        containing the part before the separator, the separator
        itself, and the part after it.

        If the separator is not found, returns a 3-tuple containing
        two empty strings and the original string.

        :param sep: the seperator to partition the string with
        :return: the partitioned string
        """
        if isinstance(sep, StringValue):
            return self._value.rpartition(sep._value)

        return self._value.rpartition(sep)

    def rsplit(self, sep: str | StringValue = None,
               max_split: int = -1) -> list[StringValue]:
        """
        Return a list of the words in the string, using sep as the
        delimiter string.

        Splits are done starting at the end of the string and working
        to the front.

        :param sep:
            The delimiter according which to split the string.
            None (the default value) means split according to any
            whitespace, and discard empty strings from the result.
        :param max_split:
            Maximum number of splits to do.
            -1 (the default value) means no limit.
        :return: a list of the words in the string, using sep as the
            delimiter string
        """
        if isinstance(sep, StringValue):
            words = self._value.rsplit(sep._value, max_split)
        else:
            words = self._value.rsplit(sep, max_split)

        new_words: list[StringValue] = []

        for word in words:
            new_words.append(StringValue(word))

        return new_words

    # noinspection SpellCheckingInspection
    def rstrip(self, chars: str | StringValue | None = None) -> StringValue:
        """
        Return a copy of the string with trailing whitespace removed.

        If chars is given and not None, remove characters in chars
        instead.

        :param chars: if not none, remove these characters instead
        :return: this instance for use in method chaining
        """
        if isinstance(chars, StringValue):
            self._value = self._value.rstrip(chars._value)
        else:
            self._value = self._value.rstrip(chars)
        return self

    def split(self, sep: str | StringValue = None,
              max_split: int = -1) -> list[StringValue]:
        """
        Return a list of the words in the string, using sep as the
        delimiter string.

        :param sep:
            The delimiter according which to split the string.
            None (the default value) means split according to any
            whitespace, and discard empty strings from the result.
        :param max_split:
            Maximum number of splits to do.
            -1 (the default value) means no limit.
        :return: a list of the words in the string, using sep as the
            delimiter string
        """
        if isinstance(sep, StringValue):
            words = self._value.split(sep._value, max_split)
        else:
            words = self._value.split(sep, max_split)

        new_words: list[StringValue] = []

        for word in words:
            new_words.append(StringValue(word))

        return new_words

    def splitlines(self, keep_ends: bool = False) -> list[str]:
        """
        Return a list of the lines in the string, breaking at line
        boundaries.

        Line breaks are not included in the resulting list unless
        keep_ends is given and true.

        :param keep_ends: if True includes linebreaks in the resulting
            list
        :return: a list of the lines in the string, breaking at line
            boundaries
        """
        return self._value.splitlines(keep_ends)

    def startswith(self, prefix: str | StringValue | tuple[str],
                   start: SupportsIndex | None = None,
                   end: SupportsIndex | None = None) \
            -> BooleanValue:
        """
        Return True if S starts with the specified prefix,
        False otherwise.
        With optional start, test S beginning at that position.
        With optional end, stop comparing S at that position.
        Parameter 'prefix' can also be a tuple of strings to try.

        :param prefix: the prefix to check for
        :param start: the beginning of the slice
        :param end: the end of the slice
        :return: true if the value begins with the specified prefix,
            False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        if isinstance(prefix, StringValue):
            return BooleanValue(self._value.startswith(prefix._value, start, end))

        return BooleanValue(self._value.startswith(prefix, start, end))

    def strip(self, chars: str | StringValue | None = None) -> StringValue:
        """
        Return a copy of the string with leading and trailing
        whitespace removed.

        If chars is given and not None, remove characters in chars
        instead.

        :param chars: if not none, remove these characters instead
        :return: this instance for use in method chaining
        """
        if isinstance(chars, StringValue):
            self._value = self._value.strip(chars._value)
        else:
            self._value = self._value.strip(chars)
        return self

    # noinspection SpellCheckingInspection
    def swapcase(self) -> StringValue:
        """
        Convert uppercase characters to lowercase and lowercase
        characters to uppercase.

        :return: this instance for use in method chaining
        """
        self._value = self._value.swapcase()
        return self

    def title(self) -> StringValue:
        """
        Return a version of the string where each word is title cased.

        More specifically, words start with upper-cased characters and
        all remaining cased characters have lower case.

        :return: this instance for use in method chaining
        """
        self._value = self._value.title()
        return self

    def translate(self, table: Mapping[int, int | str | None]) -> StringValue:
        """
        Replace each character in the string using the given
        translation table.

        The table must implement lookup/indexing via __getitem__, for
        instance a dictionary or list.  If this operation raises
        LookupError, the character is left untouched. Characters mapped
        to None are deleted.

        :param table:
            Translation table, which must be a mapping of Unicode
            ordinals to Unicode ordinals, strings, or None.
        :return: this instance for use in method chaining
        """
        self._value = self._value.translate(table)
        return self

    def upper(self) -> StringValue:
        """
        Return a copy of the string converted to uppercase.

        :return: this instance for use in method chaining
        """
        self._value = self._value.upper()
        return self

    def zfill(self, width: SupportsIndex) -> StringValue:
        """
        Pad the value with zeros on the left, to fill a 'field' of the
        given width.

        The string is never truncated.

        :param width: the with of the new string
        :return: this instance for use in method chaining
        """
        self._value = self._value.zfill(width)
        return self

    ########################################
    # Custom Instance Methods              #
    ########################################

    def strip_ansi_codes(self) -> StringValue:
        """
        Strips all ansi codes from the value.

        :return: this instance for use in method chaining
        """
        self._value = Patterns.ANSI_BASIC_ESCAPE.sub("", self._value) \
            .replace("\x1b7", "") \
            .replace("\x1b7r", "") \
            .replace("\x1b8", "") \
            .replace("\x1b8r", "")

        return self

    def wrap(self, wrap_char: str | StringValue) -> StringValue:
        """
        Wraps a character around the value.

        :param wrap_char: the character used to wrap
        :return: wrapped string or the original string
                    if wrap_char is empty
        """
        if wrap_char:
            if isinstance(wrap_char, StringValue):
                self._value = f"{wrap_char._value}{self._value}{wrap_char._value}"
            else:
                self._value = f"{wrap_char}{self._value}{wrap_char}"

        return self

    def unwrap(self, wrap_char: str | StringValue) -> StringValue:
        """
        Unwraps the value from a character.

        :param wrap_char: the character used to unwrap
        :return: unwrapped string or the original string if it is not
                    quoted properly with the wrap character
        """
        if isinstance(wrap_char, StringValue):
            wrap_char = wrap_char._value

        if wrap_char and self._value[0] == wrap_char \
                and self._value[-1] == wrap_char:
            self._value = self._value[1:-1]

        return self

    def is_boolean(self) -> BooleanValue:
        """
        Checks if the value can be converted to a Boolean.

        The following strings are considered true boolean values:
        "true", "t", "yes", "y", "1", "succeeded", "succeed", "enabled"
        The following strings are considered false boolean values:
        "false", "f", "no", "n", "0", "failed", "fail", "disabled"

        :return: true if string matches a boolean,
                    false if it does not match or is None or empty
        """
        from pystdlib.values.boolean_value import BooleanValue
        if not input or input is None:
            return BooleanValue(False)

        val = self._value.lower().strip()

        result = val in ("true", "t", "yes", "y", "1",
                         "succeeded", "succeed", "enabled",
                         "false", "f", "no", "n", "0",
                         "failed", "fail", "disabled")

        return BooleanValue(result)

    def to_boolean(self) -> BooleanValue | None:
        """
        Converts the value to a Boolean.

        The following strings are considered true boolean values:
        "true", "t", "yes", "y", "1", "succeeded", "succeed", "enabled"
        The following strings are considered false boolean values:
        "false", "f", "no", "n", "0", "failed", "fail", "disabled"

        None is returned if the string does not match a boolean value,
        an empty string or having the value None

        :return: the converted boolean,
                    None is returned if a match is not found
        """
        from pystdlib.values.boolean_value import BooleanValue
        if self._value and self._value is not None:
            val = str(self._value).lower().strip()

            is_true = val in ("true", "t", "yes", "y", "1",
                              "succeeded", "succeed", "enabled")

            is_false = val in ("false", "f", "no", "n", "0",
                               "failed", "fail", "disabled")

            if is_true:
                return BooleanValue(True)
            if is_false:
                return BooleanValue(False)

        return None

    def to_int(self) -> IntegerValue:
        """
        Converts the value to an IntegerValue and returns it.

        :return the value converted to an IntegerValue
        """
        from pystdlib.values.integer_value import IntegerValue
        return IntegerValue(self._value)

    def to_float(self) -> FloatValue:
        """
        Converts the value to a FloatValue and returns it.

        :return the value converted to a FloatValue
        """
        from pystdlib.values.float_value import FloatValue
        return FloatValue(self._value)

    def parse_int(self, default: int | IntegerValue = None) -> IntegerValue:
        """
        Attempts to parse the value to an int.
        If it fails, returns the default.
        If default is None then ValueError is raised.

        :param default: the value to return if parsing fails
        :return: the parsed int, or the default if parsing failed
        :raises ValueError: if parse failed and default is None
        """
        from pystdlib.values.integer_value import IntegerValue
        check_argument_type(default, "default", (int, IntegerValue))

        try:
            return IntegerValue(self._value)
        except ValueError:
            if default is not None:
                return IntegerValue(default)

            raise

    def parse_float(self, default: float | FloatValue = None) -> FloatValue:
        """
        Attempts to parse the value to a float.
        If it fails, returns the default.
        If default is None then ValueError is raised.

        :param default: the value to return if parsing fails
        :return: the parsed float, or the default if parsing failed
        :raises ValueError: if parse failed and default is None
        """
        from pystdlib.values.float_value import FloatValue
        check_argument_type(default, "default", (float, FloatValue))

        try:
            return FloatValue(self._value)
        except ValueError:
            if default is not None:
                return FloatValue(default)

            raise

    def is_empty(self) -> BooleanValue:
        """
        Returns True if the value is empty.

        :return: True if the value is empty
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue("".__eq__(self._value))

    def is_not_empty(self) -> BooleanValue:
        """
        Returns True if the value is not empty.

        :return: True if the value is not empty
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(not "".__eq__(self._value))

    def is_blank(self) -> BooleanValue:
        """
        Returns True if the value is whitespace or empty.

        :return: True if the value is whitespace or empty
        """
        from pystdlib.values.boolean_value import BooleanValue
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(False)

    def is_not_blank(self) -> BooleanValue:
        """
        Returns True if the value is not whitespace or empty.

        :return: True if the value is not whitespace or empty
        """
        from pystdlib.values.boolean_value import BooleanValue
        try:
            return BooleanValue(not "".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(True)

    def is_blank_or_none(self) -> BooleanValue:
        """
        Returns True if the value is whitespace, empty or None.

        :return: True if the value is whitespace, empty or None
        """
        from pystdlib.values.boolean_value import BooleanValue
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(self._value is None)

    def is_not_blank_or_none(self) -> BooleanValue:
        """
        Returns True if the value is not whitespace, empty or None.

        :return: True if the value is not whitespace, empty or None
        """
        from pystdlib.values.boolean_value import BooleanValue
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(self._value is not None)
