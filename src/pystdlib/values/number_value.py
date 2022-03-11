# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# number_value.py
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
Contains the NumberValue class, which provides
mutable access to a number value.
"""
from __future__ import annotations

from abc import abstractmethod
from numbers import Number
from typing import (
    SupportsInt, SupportsFloat, SupportsIndex,
    Optional, Tuple, TYPE_CHECKING
)

from pystdlib.protocols import SupportsIntFloatStr
from pystdlib.values.value import Value

if TYPE_CHECKING:
    from pystdlib.values import (
        IntegerValue, FloatValue, BooleanValue, StringValue
    )


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

    @abstractmethod
    def __lt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        pass

    @abstractmethod
    def __le__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        pass

    @abstractmethod
    def __gt__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        pass

    @abstractmethod
    def __ge__(self, other: int | float | IntegerValue | FloatValue) \
            -> BooleanValue:
        pass

    @abstractmethod
    def get(self) -> int | float:
        """
        Returns the value.

        :return the value
        """

    @abstractmethod
    def set(self, value: int | float | IntegerValue | FloatValue) -> NumberValue:
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
    def increment_and_get(self) -> NumberValue:
        """
        Increments this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance after it was
            incremented
        """

    @abstractmethod
    def get_and_increment(self) -> NumberValue:
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
    def decrement_and_get(self) -> NumberValue:
        """
        Decrements this instance's value by 1 then
        returns the value associated with the instance.

        :return: the value associated with the instance after it was
            decremented
        """

    @abstractmethod
    def get_and_decrement(self) -> NumberValue:
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
    def add_and_get(self, other: int | float) -> NumberValue:
        """
        Increments this instance's value by 'other', then
        returns the value associated with the instance immediately
        after the addition operation.

        :param other: the quantity to add
        :return: the value associated with this instance after
            adding the other
        """

    @abstractmethod
    def get_and_add(self, other: int | float) -> NumberValue:
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
