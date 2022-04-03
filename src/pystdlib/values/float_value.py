# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# float_value.py
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
Contains the FloatValue class, which provides
mutable access to a float value.
"""
from __future__ import annotations

from typing import SupportsFloat, SupportsIndex, SupportsInt, Optional, TYPE_CHECKING

from pystdlib.protocols import SupportsFloatFull
from pystdlib.str_utils import build_repr
from pystdlib.values.number_value import NumberValue

if TYPE_CHECKING:
    from pystdlib.values import IntegerValue, BooleanValue, StringValue


class FloatValue(NumberValue):
    """Provides mutable access to a float"""

    def __init__(self, number: SupportsFloatFull | StringValue):
        self._value: float = self._verify_float(number)

    @staticmethod
    def _verify_float(number: SupportsFloatFull | StringValue) -> float:
        from pystdlib.values.string_value import StringValue

        if number is None:
            raise TypeError(
                "FloatValue() argument must be a string, "
                "a bytes-like object or a number, not 'NoneType'"
            )

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
            raise TypeError(
                "FloatValue() argument must be a string, "
                "a bytes-like object or a number,"
                f" not '{type(number).__name__}'"
            )
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

    def __getnewargs__(self) -> tuple[float]:
        return self._value.__getnewargs__()

    def __eq__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
        return self.is_equal_to(other)

    def __ne__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
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
        from pystdlib.values.integer_value import IntegerValue

        return IntegerValue(self._value.__floor__())

    def __ceil__(self) -> IntegerValue:
        from pystdlib.values.integer_value import IntegerValue

        return IntegerValue(self._value.__ceil__())

    def __iadd__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            self._value += other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value += other.get()
            return self

        return NotImplemented

    def __add__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> IntegerValue | FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value + other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value + other.get())

        return NotImplemented

    def __radd__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(other + self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() + self._value)

        return NotImplemented

    def __isub__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            self._value -= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value -= other.get()
            return self

        return NotImplemented

    def __sub__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value - other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value - other.get())

        return NotImplemented

    def __rsub__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(other - self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() - self._value)

        return NotImplemented

    def __imul__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            self._value *= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value *= other.get()
            return self

        return NotImplemented

    def __mul__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value * other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value * other.get())

        return NotImplemented

    def __rmul__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(other * self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() * self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __itruediv__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            self._value /= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value /= other.get()
            return self

        return NotImplemented

    def __truediv__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value / other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value / other.get())

        return NotImplemented

    def __rtruediv__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(other / self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() / self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ifloordiv__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __floordiv__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    def __rfloordiv__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value // other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value // other.get())

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __ipow__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value**other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value ** other.get())

        return NotImplemented

    def __pow__(
        self,
        other: int | float | IntegerValue | FloatValue,
        modulo: Optional[float | FloatValue] = None,
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if modulo is None:
            if isinstance(other, (int, float)):
                return FloatValue(self._value**other)

            if isinstance(other, (IntegerValue, FloatValue)):
                return FloatValue(self._value ** other.get())

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        # TODO: replace with less conditions
        if (
            (is_mod_int and is_other_int)
            or (is_mod_int and is_other_float)
            or (is_mod_float and is_other_int)
        ):
            raise TypeError(
                "TypeError: pow() 3rd argument not allowed "
                "unless all arguments are integers"
            )

        return NotImplemented

    def __rpow__(
        self,
        other: int | float | IntegerValue | FloatValue,
        modulo: Optional[float | FloatValue] = None,
    ) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if modulo is None:
            if isinstance(other, (int, float)):
                return FloatValue(other**self._value)

            if isinstance(other, (IntegerValue, FloatValue)):
                return FloatValue(other.get() ** self._value)

            return NotImplemented

        is_other_int = other is int or isinstance(other, IntegerValue)
        is_other_float = other is float or isinstance(other, FloatValue)
        is_mod_int = modulo is int or isinstance(modulo, IntegerValue)
        is_mod_float = modulo is float or isinstance(modulo, FloatValue)

        # TODO: replace with less conditions
        if (
            (is_mod_int and is_other_int)
            or (is_mod_int and is_other_float)
            or (is_mod_float and is_other_int)
        ):
            raise TypeError(
                "TypeError: pow() 3rd argument not allowed "
                "unless all arguments are integers"
            )

        return NotImplemented

    def __imod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            self._value %= other
            return self

        if isinstance(other, (IntegerValue, FloatValue)):
            self._value %= other.get()
            return self

        return NotImplemented

    def __mod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(self._value % other)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(self._value % other.get())

        return NotImplemented

    def __rmod__(self, other: int | float | IntegerValue | FloatValue) -> FloatValue:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            return FloatValue(other % self._value)

        if isinstance(other, (IntegerValue, FloatValue)):
            return FloatValue(other.get() % self._value)

        return NotImplemented

    # noinspection SpellCheckingInspection
    def __divmod__(
        self, other: int | float | IntegerValue | FloatValue
    ) -> tuple[FloatValue, FloatValue]:
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(other, (int, float)):
            var1, var2 = self._value.__divmod__(other)
            return FloatValue(var1), FloatValue(var2)

        if isinstance(other, (IntegerValue, FloatValue)):
            var1, var2 = self._value.__divmod__(other.get())
            return FloatValue(var1), FloatValue(var2)

        return NotImplemented

    def __rdivmod__(self, other: float | FloatValue) -> tuple[FloatValue, FloatValue]:
        if isinstance(other, float):
            var1, var2 = other.__divmod__(self._value)
            return FloatValue(var1), FloatValue(var2)

        if isinstance(other, FloatValue):
            var1, var2 = other.get().__divmod__(self._value)
            return FloatValue(var1), FloatValue(var2)

        return NotImplemented

    def __lt__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
        return self.is_less_than(other)

    def __le__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
        return self.is_less_than_or_equal_to(other)

    def __gt__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
        return self.is_greater_than(other)

    def __ge__(self, other: int | float | IntegerValue | FloatValue) -> BooleanValue:
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

    def set(self, value: SupportsFloatFull | StringValue) -> FloatValue:
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
        from pystdlib.values.boolean_value import BooleanValue

        return BooleanValue(self._value > 0.0)

    def is_negative(self) -> BooleanValue:
        """
        Returns True if the value is negative, False otherwise.

        :return: True if the value is negative, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue

        return BooleanValue(self._value < 0.0)

    def is_zero(self) -> BooleanValue:
        """
        Returns True if the value is zero, False otherwise.

        :return: True if the value is zero, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue

        return BooleanValue(self._value == 0.0)

    def is_not_zero(self) -> BooleanValue:
        """
        Returns True if the value is not zero, False otherwise.

        :return: True if the value is annotations zero, False otherwise
        """
        from pystdlib.values.boolean_value import BooleanValue

        return BooleanValue(self._value != 0.0)

    def is_equal_to(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is equal to the specified number,
        False otherwise.

        :param number: the number to check
        :return: True if the value is equal to the specified number,
            False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value == number.get())

        return BooleanValue(self._value == number)

    def is_not_equal_to(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is not equal to the specified
        number, False otherwise.

        :param number: the number to check
        :return: True if the value is not equal to the specified number,
            False otherwise.
        """
        return self.is_equal_to(number).negate()

    def is_less_than_or_equal_to(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is less than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than or equal to the
            specified number, False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value <= number.get())

        return BooleanValue(self._value <= number)

    def is_greater_than_or_equal_to(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is greater than or equal to the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than or equal to the
            specified number, False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value >= number.get())

        return BooleanValue(self._value >= number)

    def is_less_than(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is less than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is less than the
            specified number, False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        from pystdlib.values.integer_value import IntegerValue

        if isinstance(number, (IntegerValue, FloatValue)):
            return BooleanValue(self._value < number.get())

        return BooleanValue(self._value < number)

    def is_greater_than(
        self, number: int | float | IntegerValue | FloatValue
    ) -> BooleanValue:
        """
        Returns True if the value is greater than the
        specified number, False otherwise.

        :param number: the number to check
        :return: True if the value is greater than the
            specified number, False otherwise.
        """
        from pystdlib.values.boolean_value import BooleanValue
        from pystdlib.values.integer_value import IntegerValue

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
        return self._value.as_integer_ratio()

    def is_integer(self) -> BooleanValue:
        """
        Returns True if the float is an integer.

        :return: True if the float is an integer
        """
        from pystdlib.values.boolean_value import BooleanValue

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
        from pystdlib.values.string_value import StringValue

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
