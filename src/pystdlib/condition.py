# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# condition.py
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
Contains the Condition class, an object that allows evaluation of
one or more conditions.
"""
from __future__ import annotations

from typing import Set, List, Dict, Tuple, Union, Any, Type, SupportsIndex

from pystdlib.str_utils import build_repr

_SupportsBuiltInBool = Union[bool, set[bool], list[bool],
                             dict[Any, bool],
                             tuple[bool, ...]]

_SupportsTypingBool = Union[Set[bool], List[bool],
                            Dict[Any, bool], Tuple[bool]]

_SupportsBool = Union[_SupportsBuiltInBool, _SupportsTypingBool]


class Condition:
    """
    An object that allows evaluation of
    one or more conditions.
    """

    def __init__(self, *conditions: _SupportsBool,
                 use_or: bool = False, use_not: bool = False,
                 ignore_invalid: bool = False, lazy: bool = False):
        """
        Initializes the Condition object.

        :param conditions: the condition or conditions to check
        :param use_or: checks if any of the conditions are true instead
            of checking if all the conditions are True
        :param use_not: negates the result of each condition
        :param ignore_invalid: if True ignores any conditions that aren't
            a valid bool value
        :param lazy: if True doesn't evaluate the condition until the
            'evaluate' method is run
        """
        self._result = None

        self._conditions: list[bool] = []
        self._use_or = use_or
        self._use_not = use_not
        self._ignore_invalid = ignore_invalid
        self._lazy = lazy

        self._append_conditions(*conditions)

        if not self._lazy:
            self.evaluate()

    # Must return str
    def __str__(self) -> str:
        return str(self._result)

    # Must return str
    def __repr__(self) -> str:
        return build_repr(self, self._result)

    # Must return str
    def __format__(self, format_spec) -> str:
        return bool(self._result).__format__(format_spec)

    def __eq__(self, other: bool | SupportsIndex) -> bool:
        """
        Returns True if the result is equal to the specified value,
        False otherwise.

        :return: True if the result is equal to the specified value,
            False otherwise.
        """
        return self._result == other

    def __ne__(self, other: bool | SupportsIndex) -> bool:
        """
        Returns True if the result is not equal to the specified
        value, False otherwise.

        :return: True if the result is not equal to the specified value,
            False otherwise.
        """
        return self._result != other

    def __bool__(self) -> bool:
        if self._result is None:
            raise ValueError("Condition has yet to be evaluated! "
                             "'evaluate()' method needs to be called.")

        return self._result

    def _append_conditions(self, *conditions: _SupportsBool):
        for index, condition in enumerate(conditions, 1):
            if isinstance(condition, bool):
                self._conditions.append(condition)
            elif isinstance(condition, dict):
                for item in condition.values():
                    if isinstance(item, bool):
                        self._conditions.append(item)
            elif isinstance(condition, (set, list, tuple)):
                for item in condition:
                    if isinstance(item, bool):
                        self._conditions.append(item)
            else:
                if not self._ignore_invalid:
                    raise ValueError(f"condition value #{str(index)} "
                                     "is not a supported type!")

    # Must return bool
    def get(self) -> bool | None:
        """
        Returns the result.

        :return: the result
        """
        return self._result

    def evaluate(self, *conditions: _SupportsBool) -> Condition:
        """
        Evaluates the condition if the lazy param is true,
        otherwise does nothing.

        :param conditions: the conditions to check, if conditions were
            added in the init method then they are appended
        :return: this instance for use in method chaining
        """
        self._append_conditions(*conditions)

        if self._conditions is None or len(self._conditions) == 0:
            raise ValueError("condition or multiple conditions must be specified!")

        if self._use_or:
            if self._use_not:
                self._result = any(not item for item in self._conditions)
            else:
                self._result = any(item for item in self._conditions)
        else:
            if self._use_not:
                self._result = all(not item for item in self._conditions)
            else:
                self._result = all(item for item in self._conditions)

        return self

    @property
    def result(self) -> bool | None:
        """
        Returns the result.

        :return: the result
        """
        return self._result

    def is_true(self) -> bool | None:
        """
        Checks if the result equals true.

        :return: if the result equals true
        """
        return self._result

    def is_false(self) -> bool | None:
        """
        Checks if the result equals false.

        :return: if the result equals false
        """
        if self._result is None:
            return self._result

        return not self._result

    def if_true(self, func=lambda *_, **__: None, *args, **kwargs) -> Condition:
        """
        Runs the specified function if the result is true.

        NOTE: If the 'lazy' is set to true during object creation,
        then the 'evaluate()' method must be called before calling
        this method or a 'ValueError' exception will be raised.

        :param func: the function to call
        :param args: the args to pass to the function
            if result is true
        :param kwargs: the kwargs to pass to the function
            if result is true
        :return: this instance for use in method chaining
        :raise ValueError: if 'lazy' is True and 'evaluate()'
            has yet to be run or if 'func' isn't callable
        """
        if self._result is None:
            raise ValueError("Condition has yet to be evaluated! "
                             "'evaluate()' method needs to be called.")

        if not callable(func):
            raise ValueError("Specified 'function' is not a callable!")

        if self._result:
            func(*args, **kwargs)
        return self

    def if_false(self, func=lambda *_, **__: None, *args, **kwargs) -> Condition:
        """
        Runs the specified function if the result is false.

        NOTE: If the 'lazy' is set to true during object creation,
        then the 'evaluate()' method must be called before calling
        this method or a 'ValueError' exception will be raised.

        :param func: the function to call
        :param args: the args to pass to the function
            if result is false
        :param kwargs: the kwargs to pass to the function
            if result is false
        :return: this instance for use in method chaining
        :raise ValueError: if 'lazy' is True and 'evaluate()'
            has yet to be run or if 'func' isn't callable
        """
        if self._result is None:
            raise ValueError("Condition has yet to be evaluated! "
                             "'evaluate()' method needs to be called.")

        if not callable(func):
            raise ValueError("Specified 'function' is not a callable!")

        if not self._result:
            func(*args, **kwargs)
        return self

    def raise_if_true(self, exception: Type[Exception] = AssertionError,
                      message: str = "") -> Condition:
        """
        Raises the specified exception with the specified message if
        the result is True.

        NOTE: If the 'lazy' is set to true during object creation,
        then the 'evaluate()' method must be called before calling
        this method or a 'ValueError' exception will be raised.

        :param exception: the exception to raise
        :param message: the message for the exception
        :return: this instance for use in method chaining
        :raise ValueError: if 'lazy' is True and 'evaluate()'
            has yet to be run or if 'exception' doesn't
            inherit from Exception
        """
        if self._result is None:
            raise ValueError("Condition has yet to be evaluated! "
                             "'evaluate()' method needs to be called.")

        if not issubclass(exception, Exception):
            raise ValueError("Specified 'exception' is not an Exception!")

        if self._result:
            raise exception(message)
        return self

    def raise_if_false(self, exception: Type[Exception] = AssertionError,
                       message: str = "") -> Condition:
        """
        Raises the specified exception with the specified message if
        the result is False.

        NOTE: If the 'lazy' is set to true during object creation,
        then the 'evaluate()' method must be called before calling
        this method or a 'ValueError' exception will be raised.

        :param exception: the exception to raise
        :param message: the message for the exception
        :return: this instance for use in method chaining
        :raise ValueError: if 'lazy' is True and 'evaluate()'
            has yet to be run or if 'exception' doesn't
            inherit from Exception
        """
        if self._result is None:
            raise ValueError("Condition has yet to be evaluated! "
                             "'evaluate()' method needs to be called.")

        if not issubclass(exception, Exception):
            raise ValueError("Specified 'exception' is not an Exception!")

        if not self._result:
            raise exception(message)
        return self
