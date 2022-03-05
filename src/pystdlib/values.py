# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# values.py
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

"""Contains some mutable classes that mimic the built-in types."""
from __future__ import annotations

import _collections_abc
import math
import re
from abc import abstractmethod, ABC
from numbers import Number
from typing import Optional, Iterator, Tuple, SupportsInt, SupportsIndex, \
    SupportsFloat, Literal, Iterable, \
    SupportsBytes, Mapping, Sequence, Union, Any

from pystdlib import Chars
from pystdlib.regex import Patterns
from pystdlib.utils import check_argument

SupportsIntegerFull = Union[str, bytes, bytearray, SupportsInt, SupportsIndex]
SupportsFloatFull = Union[SupportsIntegerFull, SupportsFloat]
SupportsStringFull = Union[str, Sequence[str]]
SupportsIntFloatStr = Union[int, float, str]


class Value(ABC):
    """Provides mutable access to a value."""

    @abstractmethod
    def get(self):
        """
        Returns the value.

        :return the value
        """

    @abstractmethod
    def set(self, value) -> Value:
        """
        Sets the value.

        :param value: the value to set
        :return this instance for use in method chaining
        """


class NumberValue(Value, Number, SupportsInt, SupportsFloat):
    """Provides mutable access to a number"""

    def __eq__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_equal_to(other)

    def __ne__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_not_equal_to(other)

    @abstractmethod
    def __bool__(self):
        pass

    @abstractmethod
    def __int__(self) -> int:
        pass

    @abstractmethod
    def __float__(self) -> float:
        pass

    @abstractmethod
    def __pos__(self) -> NumberValue:
        pass

    @abstractmethod
    def __neg__(self) -> NumberValue:
        pass

    @abstractmethod
    def __abs__(self) -> NumberValue:
        pass

    # noinspection SpellCheckingInspection
    # Has to return int to satisfy SupportsRound
    @abstractmethod
    def __round__(self, ndigits: SupportsIndex = None) -> int:
        pass

    # Has to return int to satisfy SupportsTrunc
    @abstractmethod
    def __trunc__(self) -> int:
        pass

    @abstractmethod
    def __floor__(self) -> NumberValue:
        pass

    @abstractmethod
    def __ceil__(self) -> NumberValue:
        pass

    @abstractmethod
    def __iadd__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __add__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __radd__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __isub__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __sub__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __rsub__(self,
                 other: SupportsIntFloatStr | IntegerValue | FloatValue | StringValue) \
            -> IntegerValue | FloatValue | StringValue:
        pass

    @abstractmethod
    def __imul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __mul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __rmul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    # noinspection SpellCheckingInspection
    @abstractmethod
    def __itruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    @abstractmethod
    def __truediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    @abstractmethod
    def __rtruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    # noinspection SpellCheckingInspection
    @abstractmethod
    def __ifloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    @abstractmethod
    def __floordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    @abstractmethod
    def __rfloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        pass

    # noinspection SpellCheckingInspection
    @abstractmethod
    def __ipow__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __pow__(self, other: int | float | IntegerValue | FloatValue,
                modulo: Optional[int | IntegerValue] = None) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __rpow__(self, other: int | float | IntegerValue | FloatValue,
                 modulo: Optional[int | IntegerValue] = None) \
            -> IntegerValue | FloatValue:
        pass

    @abstractmethod
    def __imod__(self, other) -> IntegerValue:
        pass

    @abstractmethod
    def __mod__(self, other: int | IntegerValue) -> IntegerValue:
        pass

    @abstractmethod
    def __rmod__(self, other: int | IntegerValue) -> IntegerValue:
        pass

    # noinspection SpellCheckingInspection
    @abstractmethod
    def __divmod__(self, other: SupportsIndex) \
            -> Tuple[IntegerValue, IntegerValue]:
        pass

    @abstractmethod
    def __rdivmod__(self, other: SupportsIndex) \
            -> Tuple[IntegerValue, IntegerValue]:
        pass

    def __lt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than(other)

    def __le__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than_or_equal_to(other)

    def __gt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than(other)

    def __ge__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than_or_equal_to(other)

    @abstractmethod
    def get(self) -> int | float:
        """
        Returns the value.

        :return the value
        """

    @abstractmethod
    def set(self, value: int | float) -> NumberValue:
        """
        Sets the value.

        :param value: the value to set
        :return this instance for use in method chaining
        """

    @abstractmethod
    def to_int(self) -> int:
        """
        Converts the value to an int and returns it.

        :return the value converted to an int
        """

    @abstractmethod
    def to_float(self) -> float:
        """
        Converts the value to a float and returns it.

        :return the value converted to a float
        """

    @abstractmethod
    def increment(self) -> NumberValue:
        """
        Increments the value.

        :return: this instance for use in method chaining
        """

    @abstractmethod
    def increment_and_get(self) -> int | float:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance after it was
            incremented
        """

    @abstractmethod
    def get_and_increment(self) -> int | float:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance before it was
            incremented
        """

    @abstractmethod
    def decrement(self) -> NumberValue:
        """
        Decrements the value.

        :return: this instance for use in method chaining
        """

    @abstractmethod
    def decrement_and_get(self) -> int | float:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance after it was
            decremented
        """

    @abstractmethod
    def get_and_decrement(self) -> int | float:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance before it was
            decremented
        """

    @abstractmethod
    def add(self, other: int | float) -> NumberValue:
        """
        Adds a value to the value of this instance.

        :param other: the value to add
        :return: this instance for use in method chaining
        """

    @abstractmethod
    def add_and_get(self, other: int | float) -> int | float:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance after
            adding the other
        """

    @abstractmethod
    def get_and_add(self, other: int | float) -> int | float:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance before
            adding the other
        """

    @abstractmethod
    def subtract(self, other: int | float) -> NumberValue:
        """
        Subtracts a value to the value of this instance.

        :param other: the value to subtract
        :return: this instance for use in method chaining
        """

    @abstractmethod
    def subtract_and_get(self, other: int | float) -> int | float:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance after
            subtracting the other
        """

    @abstractmethod
    def get_and_subtract(self, other: int | float) -> int | float:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance before
            subtracting the other
        """

    @abstractmethod
    def is_positive(self) -> BooleanValue:
        """
        Returns True if the value is positive,
        False otherwise.

        :return: True if the value is positive,
        False otherwise
        """

    @abstractmethod
    def is_negative(self) -> BooleanValue:
        """
        Returns True if the value is negative,
        False otherwise.

        :return: True if the value is negative,
            False otherwise
        """

    @abstractmethod
    def is_zero(self) -> BooleanValue:
        """
        Returns True if the value is zero,
        False otherwise.

        :return: True if the value is zero,
            False otherwise
        """

    @abstractmethod
    def is_not_zero(self) -> BooleanValue:
        """
        Returns True if the value is not zero,
        False otherwise.

        :return: True if the value is annotations zero,
            False otherwise
        """

    @abstractmethod
    def is_equal_to(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is equal to the specified number,
        False otherwise.

        :param number: the number to check
        :return: True if the value is equal to the specified number,
            False otherwise.
        """

    @abstractmethod
    def is_not_equal_to(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        number, False otherwise.

        :param number: the number to check
        :return: True if the value is not equal to the specified number,
            False otherwise.
        """

    @abstractmethod
    def is_less_than_or_equal_to(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is less than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than or equal to the
            specified number, False otherwise.
        """

    @abstractmethod
    def is_greater_than_or_equal_to(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is greater than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than or equal to the
            specified number, False otherwise.
        """

    @abstractmethod
    def is_less_than(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is less than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than the
            specified number, False otherwise.
        """

    @abstractmethod
    def is_greater_than(self, number: int | float) -> BooleanValue:
        """
        Returns True if the value is greater than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than the
            specified number, False otherwise.
        """


class IntegerValue(NumberValue):
    """Provides mutable access to a int"""

    def __init__(self, number: SupportsIntegerFull | StringValue = 0):
        self._value: int = self._verify_int(number)

    @staticmethod
    def _verify_int(number: SupportsIntegerFull | StringValue = 0) \
            -> int:
        if number is None:
            raise TypeError("IntegerValue() argument must be a string, "
                            "a bytes-like object or a number, not 'NoneType'")

        if isinstance(number, (str, bytes, bytearray)):
            try:
                value: int = int(number)
            except ValueError as ex:
                if "invalid literal for int() with base 10:" in str(ex):
                    raise TypeError(str(ex).replace("int()", "IntegerValue()"))

                raise

        elif isinstance(number, StringValue):
            try:
                value: int = int(number.get())
            except ValueError as ex:
                if "invalid literal for int() with base 10:" in str(ex):
                    raise TypeError(str(ex).replace("int()", "IntegerValue()"))

                raise
        elif isinstance(number, (int, float)):
            value: int = int(number)
        elif isinstance(number, SupportsInt):
            return IntegerValue._verify_int(number.__int__())
        elif isinstance(number, SupportsIndex):
            return IntegerValue._verify_int(number.__index__())
        else:
            raise TypeError("IntegerValue() argument must be a string, "
                            "a bytes-like object or a number,"
                            f" not '{type(number).__name__}'")
        return value

    ########################################
    # Dunder Methods                       #
    ########################################

    # Must return str
    def __str__(self) -> str:
        return str(self._value)

    # Must return str
    def __repr__(self) -> str:
        return repr(self._value)

    # Must return str
    def __format__(self, format_spec) -> str:
        return self._value.__format__(format_spec)

    # Must return bool
    def __bool__(self) -> bool:
        return self._value != 0

    def __getnewargs__(self) -> tuple[int]:
        return self._value.__getnewargs__()

    def __eq__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        """
        Returns True if the value is equal to the specified number,
        False otherwise.

        :param other: the number to check
        :return: True if the value is equal to the specified number,
            False otherwise.
        """
        if isinstance(other, (IntegerValue, FloatValue)):
            return BooleanValue(self._value == other.get())

        return BooleanValue(self._value == other)

    def __ne__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        number, False otherwise.

        :param other: the number to check
        :return: True if the value is not equal to the specified number,
            False otherwise.
        """
        return self.__eq__(other).negate()

    __hash__ = None

    # Must return int
    def __int__(self) -> int:
        return int(self._value)

    # Must return float
    def __float__(self) -> float:
        return float(self._value)

    # Must return complex
    def __complex__(self) -> complex:
        return complex(self._value)

    def __pos__(self) -> IntegerValue:
        return IntegerValue(self._value.__pos__())

    def __neg__(self) -> IntegerValue:
        return IntegerValue(self._value.__neg__())

    def __abs__(self) -> IntegerValue:
        return IntegerValue(abs(self._value))

    # noinspection SpellCheckingInspection
    # Has to return int to satisfy SupportsRound
    def __round__(self, ndigits: SupportsIndex = None) -> int:
        return round(self._value)

    # Has to return int to satisfy SupportsTrunc
    def __trunc__(self) -> int:
        return self._value.__trunc__()

    def __floor__(self) -> IntegerValue:
        return IntegerValue(self._value.__floor__())

    def __ceil__(self) -> IntegerValue:
        return IntegerValue(self._value.__ceil__())

    def __iadd__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            self._value += other
            return self

        if isinstance(other, float):
            return FloatValue(self._value + other)

        if isinstance(other, IntegerValue):
            self._value += other.get()
            return self

        if isinstance(other, FloatValue):
            return FloatValue(self._value + other.get())

        return NotImplemented

    def __add__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            return IntegerValue(self._value + other)

        if isinstance(other, float):
            return FloatValue(self._value + other)

        if isinstance(other, IntegerValue):
            return IntegerValue(self._value + other.get())

        if isinstance(other, FloatValue):
            return FloatValue(self._value + other.get())

        return NotImplemented

    def __radd__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            return FloatValue(other + self._value)

        if isinstance(other, float):
            return FloatValue(other + self._value)

        if isinstance(other, IntegerValue):
            return FloatValue(other.get() + self._value)

        if isinstance(other, FloatValue):
            return FloatValue(other.get() + self._value)

        return NotImplemented

    def __isub__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            self._value -= other
            return self

        if isinstance(other, float):
            return FloatValue(self._value - other)

        if isinstance(other, IntegerValue):
            self._value -= other.get()
            return self

        if isinstance(other, FloatValue):
            return FloatValue(self._value - other.get())

        return NotImplemented

    def __sub__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            return IntegerValue(self._value - other)

        if isinstance(other, float):
            return FloatValue(self._value - other)

        if isinstance(other, IntegerValue):
            return IntegerValue(self._value - other.get())

        if isinstance(other, FloatValue):
            return FloatValue(self._value - other.get())

        return NotImplemented

    def __rsub__(self,
                 other: SupportsIntFloatStr | IntegerValue | FloatValue | StringValue) \
            -> IntegerValue | FloatValue | StringValue:
        if isinstance(other, int):
            return IntegerValue(other - self._value)

        if isinstance(other, float):
            return FloatValue(other - self._value)

        if isinstance(other, IntegerValue):
            return IntegerValue(other.get() - self._value)

        if isinstance(other, FloatValue):
            return FloatValue(other.get() - self._value)

        if isinstance(other, str):
            if self._value >= 0:
                return StringValue(other[self._value:])

            return StringValue(other[:self._value])

        if isinstance(other, IntegerValue):
            if self._value >= 0:
                return StringValue(other.get()[self._value:])

            return StringValue(other.get()[:self._value])

        return NotImplemented

    def __imul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            self._value *= other
            return self

        if isinstance(other, float):
            return FloatValue(self._value * other)

        if isinstance(other, IntegerValue):
            self._value *= other.get()
            return self

        if isinstance(other, FloatValue):
            return FloatValue(self._value * other.get())

        return NotImplemented

    def __mul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            return IntegerValue(self._value * other)

        if isinstance(other, float):
            return FloatValue(self._value * other)

        if isinstance(other, IntegerValue):
            return IntegerValue(self._value * other.get())

        if isinstance(other, FloatValue):
            return FloatValue(self._value * other.get())

        return NotImplemented

    def __rmul__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            return IntegerValue(other * self._value)

        if isinstance(other, float):
            return FloatValue(other * self._value)

        if isinstance(other, IntegerValue):
            return IntegerValue(other.get() * self._value)

        if isinstance(other, FloatValue):
            return FloatValue(other.get() * self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __itruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __truediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __rtruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other / self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() / self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ifloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __floordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __rfloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ipow__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, int):
            self._value **= other
            return self

        if isinstance(other, float):
            return FloatValue(self._value ** other)

        if isinstance(other, IntegerValue):
            self._value **= other.get()
            return self

        if isinstance(other, FloatValue):
            return FloatValue(self._value ** other.get())

        return NotImplemented

    def __pow__(self, other: int | float | IntegerValue | FloatValue,
                modulo: Optional[int | IntegerValue] = None) \
            -> IntegerValue | FloatValue:
        if modulo is None:
            if isinstance(other, int):
                return IntegerValue(self._value ** other)

            if isinstance(other, float):
                return FloatValue(self._value ** other)

            if isinstance(other, IntegerValue):
                return IntegerValue(self._value ** other.get())

            if isinstance(other, FloatValue):
                return FloatValue(self._value ** other.get())

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        if is_mod_int and is_other_int:
            if isinstance(other, int) and isinstance(modulo, int):
                return IntegerValue((self._value ** other) % modulo)

            if isinstance(other, IntegerValue) and isinstance(modulo, int):
                return IntegerValue((self._value ** other.get()) % modulo)

            if isinstance(other, int) and isinstance(modulo, IntegerValue):
                return IntegerValue((self._value ** other) % modulo._value)

            if isinstance(other, IntegerValue) and isinstance(modulo, IntegerValue):
                return IntegerValue((self._value ** other.get()) % modulo._value)

        if (is_mod_int and is_other_float) or (is_mod_float and is_other_int):
            raise TypeError("pow() 3rd argument not allowed "
                            "unless all arguments are integers")

        return NotImplemented

    def __rpow__(self, other: int | float | IntegerValue | FloatValue,
                 modulo: Optional[int | IntegerValue] = None) \
            -> IntegerValue | FloatValue:
        if modulo is None:
            if isinstance(other, int):
                return IntegerValue(other ** self._value)

            if isinstance(other, float):
                return FloatValue(other ** self._value)

            if isinstance(other, IntegerValue):
                return IntegerValue(other.get() ** self._value)

            if isinstance(other, FloatValue):
                return FloatValue(other.get() ** self._value)

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        if is_mod_int and is_other_int:
            if isinstance(other, int) and isinstance(modulo, int):
                return IntegerValue((other ** self._value) % modulo)

            if isinstance(other, IntegerValue) and isinstance(modulo, int):
                return IntegerValue((other.get() ** self._value) % modulo)

            if isinstance(other, int) and isinstance(modulo, IntegerValue):
                return IntegerValue((other ** self._value) % modulo._value)

            if isinstance(other, IntegerValue) and isinstance(modulo, IntegerValue):
                return IntegerValue((other.get() ** self._value) % modulo._value)

        if (is_mod_int and is_other_float) or (is_mod_float and is_other_int):
            raise TypeError("pow() 3rd argument not allowed "
                            "unless all arguments are integers")

        return NotImplemented

    def __imod__(self, other) -> IntegerValue:
        if isinstance(other, int):
            self._value %= other
            return self

        if isinstance(other, IntegerValue):
            self._value %= other.get()
            return self

        return NotImplemented

    def __mod__(self, other: int | IntegerValue) -> IntegerValue:
        if isinstance(other, int):
            return IntegerValue(self._value % other)

        if isinstance(other, IntegerValue):
            return IntegerValue(self._value % other.get())

        return NotImplemented

    def __rmod__(self, other: int | IntegerValue) -> IntegerValue:
        if isinstance(other, int):
            return IntegerValue(other % self._value)

        if isinstance(other, IntegerValue):
            return IntegerValue(other.get() % self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __divmod__(self, other: SupportsIndex) \
            -> Tuple[IntegerValue, IntegerValue]:
        if isinstance(other, SupportsIndex):
            var1, var2 = self._value.__divmod__(other.__index__())
            return IntegerValue(var1), IntegerValue(var2)

        return NotImplemented

    def __rdivmod__(self, other: SupportsIndex) \
            -> Tuple[IntegerValue, IntegerValue]:
        if isinstance(other, int):
            var1, var2 = other.__index__().__divmod__(self._value)
            return IntegerValue(var1), IntegerValue(var2)

        return NotImplemented

    def __lt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than(other)

    def __le__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than_or_equal_to(other)

    def __gt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than(other)

    def __ge__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than_or_equal_to(other)

    ########################################
    # Integer Only Dunder Methods          #
    ########################################

    # Has to return int to satisfy SupportsIndex
    def __index__(self) -> int:
        return self._value

    def __invert__(self) -> IntegerValue:
        return IntegerValue(self._value.__invert__())

    # noinspection SpellCheckingInspection
    def __ilshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            self._value <<= other.__index__()
            return self

        return NotImplemented

    def __lshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(self._value << other.__index__())

        return NotImplemented

    def __rlshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(other.__index__() << self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __irshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            self._value >>= other.__index__()
            return self

        return NotImplemented

    def __rshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(self._value >> other.__index__())

        return NotImplemented

    def __rrshift__(self, other: SupportsIndex) -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(other.__index__() >> self._value)

        return NotImplemented

    def __iand__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            self._value &= other.__index__()
            return self

        return NotImplemented

    def __and__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(self._value & other.__index__())

        return NotImplemented

    def __rand__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(other.__index__() & self._value)

        return NotImplemented

    def __ior__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            self._value |= other.__index__()
            return self

        return NotImplemented

    def __or__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(self._value | other.__index__())

        return NotImplemented

    def __ror__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(other.__index__() | self._value)

        return NotImplemented

    def __ixor__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            self._value ^= other.__index__()
            return self

        return NotImplemented

    def __xor__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(self._value ^ other.__index__())

        return NotImplemented

    def __rxor__(self, other: SupportsIndex) \
            -> IntegerValue:
        if isinstance(other, SupportsIndex):
            return IntegerValue(other.__index__() ^ self._value)

        return NotImplemented

    ########################################
    # Instance Methods                     #
    ########################################

    # Must return int
    @property
    def value(self) -> int:
        """
        Returns the value.

        :return: the value
        """
        return self._value

    # Must return int
    def get(self) -> int:
        """
        Returns the value.

        :return the value
        """
        return self._value

    def set(self, value: SupportsIntegerFull | StringValue) -> IntegerValue:
        """
        Sets the value.

        :param value: the value to set
        :return this instance for use in method chaining
        """
        self._value = IntegerValue._verify_int(value)
        return self

    # Must return int
    def to_int(self) -> int:
        """
        Converts the value to an int and returns it.

        :return the value converted to an int
        """
        return int(self._value)

    # Must return float
    def to_float(self) -> float:
        """
        Converts the value to a float and returns it.

        :return the value converted to a float
        """
        return float(self._value)

    def increment(self) -> IntegerValue:
        """
        Increments the value.

        :return: this instance for use in method chaining
        """
        self._value += 1
        return self

    def increment_and_get(self) -> IntegerValue:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance
            after it was incremented
        """
        self._value += 1
        return IntegerValue(self._value)

    def get_and_increment(self) -> IntegerValue:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance
            before it was incremented
        """
        before = self._value
        self._value += 1
        return IntegerValue(before)

    def decrement(self) -> IntegerValue:
        """
        Decrements the value.

        :return: this instance for use in method chaining
        """
        self._value -= 1
        return self

    def decrement_and_get(self) -> IntegerValue:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance
            after it was decremented
        """
        self._value -= 1
        return IntegerValue(self._value)

    def get_and_decrement(self) -> IntegerValue:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance
            before it was decremented
        """
        before = self._value
        self._value -= 1
        return IntegerValue(before)

    def add(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Adds a value to the value of this instance.

        :param other: the value to add
        :return: this instance for use in method chaining
        """
        self._value += other
        return self

    def add_and_get(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance
            after adding the other
        """
        self._value += other
        return IntegerValue(self._value)

    def get_and_add(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance
            before adding the other
        """
        before = self._value
        self._value += other
        return IntegerValue(before)

    def subtract(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Subtracts a value to the value of this instance.

        :param other: the value to subtract
        :return: this instance for use in method chaining
        """
        self._value -= other
        return self

    def subtract_and_get(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance
            after subtracting the other
        """
        self._value -= other
        return IntegerValue(self._value)

    def get_and_subtract(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance
            before subtracting the other
        """
        before = self._value
        self._value -= other
        return IntegerValue(before)

    def is_positive(self) -> BooleanValue:
        """
        Returns True if the value is positive, False otherwise.

        :return: True if the value is positive, False otherwise
        """
        return BooleanValue(self._value > 0)

    def is_negative(self) -> BooleanValue:
        """
        Returns True if the value is negative, False otherwise.

        :return: True if the value is negative, False otherwise
        """
        return BooleanValue(self._value < 0)

    def is_zero(self) -> BooleanValue:
        """
        Returns True if the value is zero, False otherwise.

        :return: True if the value is zero, False otherwise
        """
        return BooleanValue(self._value == 0)

    def is_not_zero(self) -> BooleanValue:
        """
        Returns True if the value is not zero, False otherwise.

        :return: True if the value is annotations zero, False otherwise
        """
        return BooleanValue(self._value != 0)

    def is_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is equal to the specified number,
        False otherwise.

        :param number: the number to check
        :return: True if the value is equal to the specified number,
            False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value == number.get())

        return BooleanValue(self._value == number)

    def is_not_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        number, False otherwise.

        :param number: the number to check
        :return: True if the value is not equal to the specified number,
            False otherwise.
        """
        return self.is_equal_to(number).negate()

    def is_less_than_or_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is less than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than or equal to the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value <= number.get())

        return BooleanValue(self._value <= number)

    def is_greater_than_or_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is greater than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than or equal to the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value >= number.get())

        return BooleanValue(self._value >= number)

    def is_less_than(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is less than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value < number.get())

        return BooleanValue(self._value < number)

    def is_greater_than(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is greater than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value > number.get())

        return BooleanValue(self._value > number)

    ########################################
    # Integer Only Instance Methods        #
    ########################################

    @property
    def numerator(self) -> IntegerValue:
        """Integers are their own numerators."""
        return IntegerValue(self._value)

    @property
    def denominator(self) -> IntegerValue:
        """Integers have a denominator of 1."""
        return IntegerValue(1)

    def is_odd(self) -> BooleanValue:
        """
        Returns True if the value is odd, False otherwise.

        :return: True if the value is odd, False otherwise
        """
        return BooleanValue((self._value & 1) == 1)

    def is_even(self) -> BooleanValue:
        """
        Returns True if the value is even, False otherwise.

        :return: True if the value is even, False otherwise
        """
        return BooleanValue((self._value & 1) == 0)

    def is_perfect_square(self) -> BooleanValue:
        """
        Returns True if the value is perfect square, False otherwise.

        :return: True if the value is perfect square, False otherwise
        """
        if self._value < 0:
            return BooleanValue(False)
        if self._value in (0, 1):
            return BooleanValue(True)

        var = self._value // 2
        square_x = var ** 2

        while square_x > self._value:
            var = (square_x + self._value) // (2 * var)
            square_x = var ** 2

        return BooleanValue(self._value == var ** 2)

    def as_integer_ratio(self) -> tuple[int, Literal[1]]:
        """
        Returns integer ratio.

        Returns a pair of integers, whose ratio is exactly equal to the
        original intand with a positive denominator.

        >>> (10).as_integer_ratio()
        (10, 1)
        >>> (-10).as_integer_ratio()
        (-10, 1)
        >>> (0).as_integer_ratio()
        (0, 1)

        :return: a pair of integers, whose ratio is exactly equal to the
            original int and with a positive denominator
        """
        return self._value.as_integer_ratio()

    # Must return int
    def bit_length(self) -> int:
        """
        Returns number of bits necessary to represent self in binary.

        >>> bin(37)
        '0b100101'
        >>> (37).bit_length()
        6

        :return: number of bits necessary to represent self in binary
        """
        return self._value.bit_length()

    def to_bytes(self, length: SupportsIndex,
                 byteorder: Literal["little", "big"],
                 signed: bool) -> bytes:
        """
        Returns an array of bytes representing an integer.

        :param length: Length of bytes object to use. An OverflowError
            is raised if the integer is not representable with the given
            number of bytes.
        :param byteorder: The byte order used to represent the integer.
            If byteorder is 'big', the most significant byte is at the
            beginning of the byte array. If byteorder is 'little', the most
            significant byte is at the end of the byte array. To request
            the native byte order of the host system, use `sys.byteorder'
            as the byte order value.
        :param signed: Determines whether two's complement is used to
            represent the integer. If signed is False and a negative
            integer is given, an OverflowError is raised.
        :return: an array of bytes representing an integer
        """
        return self._value.to_bytes(length, byteorder, signed=signed)

    # noinspection PyShadowingBuiltins
    @classmethod
    def from_bytes(cls, bytes: Iterable[SupportsIndex] | SupportsBytes,
                   byteorder: Literal["little", "big"],
                   signed: bool) -> IntegerValue:
        """
        Returns the integer represented by the given array of bytes.

        :param bytes: Holds the array of bytes to convert. The argument
            must either support the buffer protocol or be an iterable
            object producing bytes. Bytes and bytearray are examples
            of built-in objects that support the buffer protocol.
        :param byteorder: The byte order used to represent the integer.
            If byteorder is 'big', the most significant byte is at the
            beginning of the byte array. If byteorder is 'little', the
            most significant byte is at the end of the byte array. To
            request the native byte order of the host system, use
            'sys.byteorder' as the byte order value.
        :param signed: Indicates whether two's complement is used to
            represent the integer.
        :return: the integer represented by the given array of bytes
        """
        return IntegerValue(int.from_bytes(bytes, byteorder, signed=signed))

    ########################################
    # Custom Instance Methods              #
    ########################################

    def convert_bytes_to_string(self) -> StringValue:
        """
        Returns the conversion from bytes to the correct
        version (1024 bytes = 1 KB) as a string.

        :return: the value converted to a readable string
        """
        number = self._value
        factor = 1024
        if number >= factor:
            number /= factor
            if number >= factor:
                number /= factor
                if number >= factor:
                    number /= factor
                    if number >= factor:
                        number /= factor
                        if number >= factor:
                            number /= factor
                            suffix = " PB"
                        else:
                            suffix = " TB"
                    else:
                        suffix = " GB"
                else:
                    suffix = " MB"
            else:
                suffix = " KB"
        else:
            suffix = " Bytes"

        rounding_factor = 10 ** 2
        rounded = math.floor(number * rounding_factor) / rounding_factor
        return StringValue(f"{rounded:.2f}" + suffix)


class BooleanValue(IntegerValue, SupportsIndex):
    """Provides mutable access to a bool value"""

    def __init__(self, value: Any = False):
        super().__init__(int(value))

    # Must return str
    def __str__(self) -> str:
        return str(bool(self._value))

    # Must return str
    def __repr__(self) -> str:
        return str(bool(self._value))

    # Must return str
    def __format__(self, format_spec) -> str:
        return bool(self._value).__format__(format_spec)

    def __eq__(self, other: bool | BooleanValue | SupportsIndex) \
            -> BooleanValue:
        """
        Returns True if the value is equal to the specified value,
        False otherwise.

        :return: True if the value is equal to the specified value,
            False otherwise.
        """
        if isinstance(other, (BooleanValue, IntegerValue)):
            return BooleanValue(self._value == other.get())

        return BooleanValue(self._value == other)

    def __ne__(self, other: bool | BooleanValue | SupportsIndex) \
            -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        value, False otherwise.

        :return: True if the value is not equal to the specified value,
            False otherwise.
        """
        return self.__eq__(other).negate()

    # noinspection PyPropertyDefinition,PyPep8Naming
    @classmethod
    @property
    def TRUE(cls) -> BooleanValue:
        """
        Returns True as a BooleanValue.

        :return: True as a BooleanValue
        """
        return BooleanValue(True)

    # noinspection PyPropertyDefinition,PyPep8Naming
    @classmethod
    @property
    def FALSE(cls) -> BooleanValue:
        """
        Returns False as a BooleanValue.

        :return: False as a BooleanValue
        """
        return BooleanValue(False)

    # Must return bool
    @property
    def value(self) -> bool:
        """
        Returns the value.

        :return: the value
        """
        return bool(self._value)

    # Must return bool
    def get(self) -> bool:
        """
        Returns the value.

        :return: the value
        """
        return bool(self._value)

    def set(self, value: Any) \
            -> BooleanValue:
        """
        Sets the value.

        :param value: the value to set
        :return: this instance for use in method chaining
        """
        if isinstance(value, (BooleanValue, IntegerValue)):
            self._value = int(bool(value.get()))
        else:
            self._value = int(bool(value))
        return self

    def is_equal_to(
            self, value: bool | BooleanValue | SupportsIndex) \
            -> BooleanValue:
        """
        Returns True if the value is equal to the specified value,
        False otherwise.

        :param value: the value to check
        :return: True if the value is equal to the specified value,
            False otherwise.
        """
        if isinstance(value, (BooleanValue, IntegerValue)):
            return BooleanValue(self._value == value._value)

        return BooleanValue(self._value == value)

    def is_not_equal_to(
            self, value: bool | BooleanValue | SupportsIndex) \
            -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        value, False otherwise.

        :param value: the value to check
        :return: True if the value is not equal to the specified value,
            False otherwise.
        """
        return self.is_equal_to(value).negate()

    def is_true(self) -> BooleanValue:
        """
        Checks if the value equals true.

        :return: if the value equals true
        """
        return BooleanValue(bool(self._value) is True)

    def is_false(self) -> BooleanValue:
        """
        Checks if the value equals false.

        :return: if the value equals false
        """
        return BooleanValue(bool(self._value) is False)

    def set_true(self) -> BooleanValue:
        """
        Sets the value to true.

        :return: this instance for use in method chaining
        """
        self._value = 1
        return self

    def set_false(self) -> BooleanValue:
        """
        Sets the value to false.

        :return: this instance for use in method chaining
        """
        self._value = 0
        return self

    def if_true(self, *args, function=lambda *_, **__: None, **kwargs) -> BooleanValue:
        """
        Runs the specified runnable if the value is true.

        :param function: the runnable to run
        :param args: the args to pass to the function
            if value is true
        :param kwargs: the kwargs to pass to the function
            if value is true
        :return: this instance for use in method chaining
        """
        if self._value:
            function(*args, **kwargs)
        return self

    def if_false(self, *args, function=lambda *_, **__: None, **kwargs) -> BooleanValue:
        """
        Runs the specified runnable if the value is false.

        :param function: the runnable to run
        :param args: the args to pass to the function
            if value is false
        :param kwargs: the kwargs to pass to the function
            if value is false
        :return: this instance for use in method chaining
        """
        if not self._value:
            function(*args, **kwargs)
        return self

    def negate(self) -> BooleanValue:
        """
        Sets the value to the opposite of the current value.

        :return: this instance for use in method chaining
        """
        self._value = not self._value
        return self


class FloatValue(NumberValue):
    """Provides mutable access to a float"""

    def __init__(self, number: SupportsFloatFull | StringValue):
        self._value: float = self._verify_float(number)

    @staticmethod
    def _verify_float(number: SupportsFloatFull | StringValue) \
            -> float:
        if number is None:
            raise TypeError("FloatValue() argument must be a string, "
                            "a bytes-like object or a number, not 'NoneType'")

        if isinstance(number, (str, bytes, bytearray)):
            try:
                value: float = float(number)
            except ValueError as ex:
                if "invalid literal for float() with base 10:" in str(ex):
                    raise TypeError(str(ex).replace("float()", "FloatValue()"))

                raise
        elif isinstance(number, StringValue):
            try:
                value: float = float(number.get())
            except ValueError as ex:
                if "invalid literal for float() with base 10:" in str(ex):
                    raise TypeError(str(ex).replace("float()", "FloatValue()"))

                raise
        elif isinstance(number, (int, float)):
            value: float = float(number)
        elif isinstance(number, SupportsFloat):
            return FloatValue._verify_float(number.__float__())
        elif isinstance(number, SupportsIndex):
            return FloatValue._verify_float(number.__index__())
        elif isinstance(number, SupportsInt):
            return FloatValue._verify_float(number.__int__())
        else:
            raise TypeError("FloatValue() argument must be a string, "
                            "a bytes-like object or a number,"
                            f" not '{type(number).__name__}'")
        return value

    ########################################
    # Dunder Methods                       #
    ########################################

    # Must return str
    def __str__(self) -> str:
        return str(self._value)

    # Must return str
    def __repr__(self) -> str:
        return repr(self._value)

    # Must return str
    def __format__(self, format_spec) -> str:
        return self._value.__format__(format_spec)

    # Must return bool
    def __bool__(self) -> bool:
        return self._value != 0

    def __getnewargs__(self) -> tuple[float]:
        return self._value.__getnewargs__()

    def __eq__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_equal_to(other)

    def __ne__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_not_equal_to(other)

    __hash__ = None

    # Must return int
    def __int__(self) -> int:
        return int(self._value)

    # Must return float
    def __float__(self) -> float:
        return self._value

    # Must return complex
    def __complex__(self) -> complex:
        return complex(self._value)

    def __pos__(self) -> FloatValue:
        return FloatValue(self._value.__pos__())

    def __neg__(self) -> FloatValue:
        return FloatValue(self._value.__neg__())

    def __abs__(self) -> FloatValue:
        return FloatValue(abs(self._value))

    # noinspection SpellCheckingInspection
    # Has to return int to satisfy SupportsRound
    def __round__(self, ndigits: SupportsIndex = None) -> int:
        return self._value.__round__()

    # Has to return int to satisfy SupportsTrunc
    def __trunc__(self) -> int:
        return self._value.__trunc__()

    def __floor__(self) -> IntegerValue:
        return IntegerValue(self._value.__floor__())

    def __ceil__(self) -> IntegerValue:
        return IntegerValue(self._value.__ceil__())

    def __iadd__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            self._value += other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value += other.get()
            return self

        return NotImplemented

    def __add__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value + other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value + other.get())

        return NotImplemented

    def __radd__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other + self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() + self._value)

        return NotImplemented

    def __isub__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            self._value -= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value -= other.get()
            return self

        return NotImplemented

    def __sub__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value - other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value - other.get())

        return NotImplemented

    def __rsub__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other - self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() - self._value)

        return NotImplemented

    def __imul__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            self._value *= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value *= other.get()
            return self

        return NotImplemented

    def __mul__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value * other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value * other.get())

        return NotImplemented

    def __rmul__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other * self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() * self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __itruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            self._value /= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value /= other.get()
            return self

        return NotImplemented

    def __truediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __rtruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other / self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() / self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ifloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __floordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __rfloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ipow__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value ** other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value ** other.get())

        return NotImplemented

    def __pow__(self, other: int | float | IntegerValue | FloatValue,
                modulo: Optional[float | FloatValue] = None) \
            -> FloatValue:
        if modulo is None:
            if isinstance(other, (int, float)):
                return FloatValue(self._value ** other)

            if isinstance(other, (IntegerValue, FloatValue)):
                return FloatValue(self._value ** other.get())

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        # TODO: replace with less conditions
        if (is_mod_int and is_other_int) \
                or (is_mod_int and is_other_float) \
                or (is_mod_float and is_other_int):
            raise TypeError("TypeError: pow() 3rd argument not allowed "
                            "unless all arguments are integers")

        return NotImplemented

    def __rpow__(self, other: int | float | IntegerValue | FloatValue,
                 modulo: Optional[float | FloatValue] = None) \
            -> FloatValue:
        if modulo is None:
            if isinstance(other, (int, float)):
                return FloatValue(other ** self._value)

            if isinstance(other, (IntegerValue, FloatValue)):
                return FloatValue(other.get() ** self._value)

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        # TODO: replace with less conditions
        if (is_mod_int and is_other_int) \
                or (is_mod_int and is_other_float) \
                or (is_mod_float and is_other_int):
            raise TypeError("TypeError: pow() 3rd argument not allowed "
                            "unless all arguments are integers")

        return NotImplemented

    def __imod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        if isinstance(other, (int, float)):
            self._value %= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value %= other.get()
            return self

        return NotImplemented

    def __mod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(self._value % other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value % other.get())

        return NotImplemented

    def __rmod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        if isinstance(other, (int, float)):
            return FloatValue(other % self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() % self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __divmod__(self, other: int | float | IntegerValue | FloatValue) \
            -> Tuple[FloatValue, FloatValue]:
        if isinstance(other, (int, float)):
            var1, var2 = self._value.__divmod__(other)
            return FloatValue(var1), FloatValue(var2)

        if isinstance(other, (IntegerValue, FloatValue)):
            var1, var2 = self._value.__divmod__(other.get())
            return FloatValue(var1), FloatValue(var2)

        return NotImplemented

    def __rdivmod__(self, other: float | FloatValue) \
            -> Tuple[FloatValue, FloatValue]:
        if isinstance(other, float):
            var1, var2 = other.__divmod__(self._value)
            return FloatValue(var1), FloatValue(var2)

        if isinstance(other, FloatValue):
            var1, var2 = other.get().__divmod__(self._value)
            return FloatValue(var1), FloatValue(var2)

        return NotImplemented

    def __lt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than(other)

    def __le__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_less_than_or_equal_to(other)

    def __gt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than(other)

    def __ge__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        return self.is_greater_than_or_equal_to(other)

    ########################################
    # Instance Methods                     #
    ########################################

    # Must return float
    @property
    def value(self) -> float:
        """
        Returns the value.

        :return: the value
        """
        return self._value

    # Must return float
    def get(self) -> float:
        """
        Returns the value.

        :return the value
        """
        return self._value

    def set(self, value: SupportsFloatFull | StringValue) \
            -> FloatValue:
        """
        Sets the value.

        :param value: the value to set
        :return this instance for use in method chaining
        """
        self._value = FloatValue._verify_float(value)
        return self

    # Must return int
    def to_int(self) -> int:
        """
        Converts the value to an int and returns it.

        :return the value converted to an int
        """
        return int(self._value)

    # Must return float
    def to_float(self) -> float:
        """
        Converts the value to a float and returns it.

        :return the value converted to a float
        """
        return float(self._value)

    def increment(self) -> FloatValue:
        """
        Increments the value.

        :return: this instance for use in method chaining
        """
        self._value += 1
        return self

    def increment_and_get(self) -> FloatValue:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance

        :return: the value associated with the instance
            after it was incremented
        """
        self._value += 1
        return FloatValue(self._value)

    def get_and_increment(self) -> FloatValue:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance

        :return: the value associated with the instance
            before it was incremented
        """
        before = self._value
        self._value += 1
        return FloatValue(before)

    def decrement(self) -> FloatValue:
        """
        Decrements the value.

        :return: this instance for use in method chaining
        """
        self._value -= 1
        return self

    def decrement_and_get(self) -> FloatValue:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance

        :return: the value associated with the instance
            after it was decremented
        """
        self._value -= 1
        return FloatValue(self._value)

    def get_and_decrement(self) -> FloatValue:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance

        :return: the value associated with the instance
            before it was decremented
        """
        before = self._value
        self._value -= 1
        return FloatValue(before)

    def add(self, other: int | float) -> FloatValue:
        """
        Adds a value to the value of this instance.

        :param other: the value to add
        :return: this instance for use in method chaining
        """
        self._value += other
        return self

    def add_and_get(self, other: int | float) -> FloatValue:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance
            after adding the other
        """
        self._value += other
        return FloatValue(self._value)

    def get_and_add(self, other: int | float) -> FloatValue:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance
            before adding the other
        """
        before = self._value
        self._value += other
        return FloatValue(before)

    def subtract(self, other: int | float) -> FloatValue:
        """
        Subtracts a value to the value of this instance.

        :param other: the value to subtract
        :return: this instance for use in method chaining
        """
        self._value -= other
        return self

    def subtract_and_get(self, other: int | float) -> FloatValue:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance
            after subtracting the other
        """
        self._value -= other
        return FloatValue(self._value)

    def get_and_subtract(self, other: int | float) -> FloatValue:
        """
        Decrements this instance's value by 'other', then
        returns the value associated with the instance immediately
        before to the subtraction operation.

        :param other: the quantity to subtract
        :return: the value associated with this instance
            before subtracting the other
        """
        before = self._value
        self._value -= other
        return FloatValue(before)

    def is_positive(self) -> BooleanValue:
        """
        Returns True if the value is positive, False otherwise.

        :return: True if the value is positive, False otherwise
        """
        return BooleanValue(self._value > 0.0)

    def is_negative(self) -> BooleanValue:
        """
        Returns True if the value is negative, False otherwise.

        :return: True if the value is negative, False otherwise
        """
        return BooleanValue(self._value < 0.0)

    def is_zero(self) -> BooleanValue:
        """
        Returns True if the value is zero, False otherwise.

        :return: True if the value is zero, False otherwise
        """
        return BooleanValue(self._value == 0.0)

    def is_not_zero(self) -> BooleanValue:
        """
        Returns True if the value is not zero, False otherwise.

        :return: True if the value is annotations zero, False otherwise
        """
        return BooleanValue(self._value != 0.0)

    def is_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is equal to the specified number,
        False otherwise.

        :param number: the number to check
        :return: True if the value is equal to the specified number,
            False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value == number.get())

        return BooleanValue(self._value == number)

    def is_not_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        number, False otherwise.

        :param number: the number to check
        :return: True if the value is not equal to the specified number,
            False otherwise.
        """
        return self.is_equal_to(number).negate()

    def is_less_than_or_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is less than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than or equal to the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value <= number.get())

        return BooleanValue(self._value <= number)

    def is_greater_than_or_equal_to(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is greater than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than or equal to the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value >= number.get())

        return BooleanValue(self._value >= number)

    def is_less_than(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is less than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value < number.get())

        return BooleanValue(self._value < number)

    def is_greater_than(
            self, number: int | float | IntegerValue | FloatValue) -> BooleanValue:
        """
        Returns True if the value is greater than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than the
            specified number, False otherwise.
        """
        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value > number.get())

        return BooleanValue(self._value > number)

    ########################################
    # Float Only Instance Methods          #
    ########################################

    # The following regular methods are int only methods and don't apply to 'floats'
    # Must return tuple[int, int]
    def as_integer_ratio(self) -> tuple[int, int]:
        # noinspection PyRedundantParentheses
        """
        Returns integer ratio.

        Return a pair of integers, whose ratio is exactly equal to the original float
        and with a positive denominator.

        Raise OverflowError on infinities and a ValueError on NaNs.

        >>> (10.0).as_integer_ratio()
        (10, 1)
        >>> (0.0).as_integer_ratio()
        (0, 1)
        >>> (-.25).as_integer_ratio()
        (-1, 4)

        :return: a pair of integers, whose ratio is exactly equal to the original float
            and with a positive denominator
        :raises OverflowError: on infinities and a ValueError on NaNs
        """
        return self.as_integer_ratio()

    def is_integer(self) -> BooleanValue:
        """
        Returns True if the float is an integer.

        :return: True if the float is an integer
        """
        return BooleanValue(self._value.is_integer())

    def hex(self) -> StringValue:
        """
        Returns a hexadecimal representation of the value.

        >>> (-0.1).hex()
        '-0x1.999999999999ap-4'
        >>> 3.14159.hex()
        '0x1.921f9f01b866ep+1'

        :return: a hexadecimal representation of the value
        """
        return StringValue(self._value.hex())

    # noinspection SpellCheckingInspection
    @staticmethod
    def fromhex(value: str) -> FloatValue:
        """
        Create a floating-point number from the specified
        hexadecimal string.

        >>> float.fromhex('0x1.ffffp10')
        2047.984375
        >>> float.fromhex('-0x1p-1074')
        -5e-324

        :param value: the string to convert
        :return: a floating-point number from the specified
            hexadecimal string
        """
        return FloatValue(float.fromhex(value))


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
        return repr(self._value)

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
        if isinstance(other, str):
            return BooleanValue(self._value < other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value < other.get())

        type_name = type(other).__name__
        raise TypeError("'<' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __le__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        if isinstance(other, str):
            return BooleanValue(self._value <= other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value <= other.get())

        type_name = type(other).__name__
        raise TypeError("'<=' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __gt__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
        if isinstance(other, str):
            return BooleanValue(self._value > other)
        if isinstance(other, StringValue):
            return BooleanValue(self._value > other.get())

        type_name = type(other).__name__
        raise TypeError("'>' not supported between "
                        f"instances of 'StringValue' and '{type_name}'")

    def __ge__(self, other: str | Sequence[str] | StringValue) \
            -> BooleanValue:
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

    def partition(self, sep: str | StringValue) -> Tuple[str, str, str]:
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
        return IntegerValue(self._value)

    def to_float(self) -> FloatValue:
        """
        Converts the value to a FloatValue and returns it.

        :return the value converted to a FloatValue
        """
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
        check_argument(isinstance(default, int), "\"default\" must be a"
                                                 " int or IntegerValue!")

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
        check_argument(isinstance(default, float), "\"default\" must be a"
                                                   " float or FloatValue!")

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
        return BooleanValue("".__eq__(self._value))

    def is_not_empty(self) -> BooleanValue:
        """
        Returns True if the value is not empty.

        :return: True if the value is not empty
        """
        return BooleanValue(not "".__eq__(self._value))

    def is_blank(self) -> BooleanValue:
        """
        Returns True if the value is whitespace or empty.

        :return: True if the value is whitespace or empty
        """
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(False)

    def is_not_blank(self) -> BooleanValue:
        """
        Returns True if the value is not whitespace or empty.

        :return: True if the value is not whitespace or empty
        """
        try:
            return BooleanValue(not "".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(True)

    def is_blank_or_none(self) -> BooleanValue:
        """
        Returns True if the value is whitespace, empty or None.

        :return: True if the value is whitespace, empty or None
        """
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(self._value is None)

    def is_not_blank_or_none(self) -> BooleanValue:
        """
        Returns True if the value is not whitespace, empty or None.

        :return: True if the value is not whitespace, empty or None
        """
        try:
            return BooleanValue("".__eq__(self._value.strip()))
        except AttributeError:
            return BooleanValue(self._value is not None)
