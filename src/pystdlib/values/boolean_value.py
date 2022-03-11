from __future__ import annotations

from typing import Any, SupportsIndex

from pystdlib.str_utils import build_repr
from pystdlib.values.integer_value import IntegerValue


class BooleanValue(IntegerValue, SupportsIndex):
    """Provides mutable access to a bool value"""

    def __init__(self, value: Any = False):
        super().__init__(int(value))

    # Must return str
    def __str__(self) -> str:
        return str(bool(self._value))

    # Must return str
    def __repr__(self) -> str:
        return build_repr(self, bool(self._value))

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
