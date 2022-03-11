# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# integer_value.py
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

"""
Contains the IntegerValue class, which provides
mutable access to an int value.
"""
from __future__ import annotations

import math
from typing import (
    SupportsInt, SupportsIndex, Optional, Literal,
    Iterable, SupportsBytes, TYPE_CHECKING
)

from pystdlib.protocols import SupportsIntegerFull, SupportsIntFloatStr
from pystdlib.str_utils import build_repr
from pystdlib.values.number_value import NumberValue

if TYPE_CHECKING:
    from pystdlib.values import (
        FloatValue, BooleanValue, StringValue
    )


class IntegerValue(NumberValue):
    """Provides mutable access to a int"""

    def __init__(self, number: SupportsIntegerFull | StringValue = 0):
        self._value: int = self._verify_int(number)

    @staticmethod
    def _verify_int(number: SupportsIntegerFull | StringValue = 0) \
            -> int:
        from pystdlib.values.string_value import StringValue
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
        return build_repr(self, self._value)

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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.string_value import StringValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __truediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __rtruediv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(other / self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() / self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ifloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __floordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __rfloordiv__(self, other: int | float | IntegerValue | FloatValue) \
            -> FloatValue:
        from pystdlib.values.float_value import FloatValue
        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ipow__(self, other: int | float | IntegerValue | FloatValue) \
            -> IntegerValue | FloatValue:
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
        from pystdlib.values.float_value import FloatValue
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
            -> tuple[IntegerValue, IntegerValue]:
        if isinstance(other, SupportsIndex):
            var1, var2 = self._value.__divmod__(other.__index__())
            return IntegerValue(var1), IntegerValue(var2)

        return NotImplemented

    def __rdivmod__(self, other: SupportsIndex) \
            -> tuple[IntegerValue, IntegerValue]:
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
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value > 0)

    def is_negative(self) -> BooleanValue:
        """
        Returns True if the value is negative, False otherwise.

        :return: True if the value is negative, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value < 0)

    def is_zero(self) -> BooleanValue:
        """
        Returns True if the value is zero, False otherwise.

        :return: True if the value is zero, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue(self._value == 0)

    def is_not_zero(self) -> BooleanValue:
        """
        Returns True if the value is not zero, False otherwise.

        :return: True if the value is annotations zero, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.float_value import FloatValue
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue((self._value & 1) == 1)

    def is_even(self) -> BooleanValue:
        """
        Returns True if the value is even, False otherwise.

        :return: True if the value is even, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
        return BooleanValue((self._value & 1) == 0)

    def is_perfect_square(self) -> BooleanValue:
        """
        Returns True if the value is perfect square, False otherwise.

        :return: True if the value is perfect square, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue
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
        from pystdlib.values.string_value import StringValue
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
