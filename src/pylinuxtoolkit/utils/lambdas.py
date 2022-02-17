# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# lambdas.py
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
This file contains the Lambda class that contains methods that represent
lambda functions to use as defaults for function parameters.
"""
from typing import NoReturn, Any, Callable

from pylinuxtoolkit.utils.literals import EMPTY


class Lambdas:
    """
    Contains methods that represent lambda functions to use as
    defaults for function parameters.
    """

    @staticmethod
    def no_return() -> NoReturn:
        """
        Lambda that follows the Callable[[], NoReturn] signature
        and has no return and just passes.

        >>> func: Callable[[], NoReturn] = Lambdas.no_return

        :return: NoReturn
        """
        pass

    @staticmethod
    def return_none() -> None:
        """
        Lambda that follows the Callable[[], None] signature
        and returns None.

        >>> func: Callable[[], None] = Lambdas.return_none

        :return: None
        """
        return None

    @staticmethod
    def return_empty_str() -> str:
        """
        Lambda that follows the Callable[[], str] signature
        and returns an empty string.

        >>> func: Callable[[], str] = Lambdas.return_empty_str

        :return: an empty string
        """
        return EMPTY

    @staticmethod
    def return_zero() -> int:
        """
        Lambda that follows the Callable[[], int] signature
        and returns 0.

        >>> func: Callable[[], int] = Lambdas.return_zero

        :return: 0
        """
        return 0

    @staticmethod
    def return_one() -> int:
        """
        Lambda that follows the Callable[[], int] signature
        and returns 1.

        >>> func: Callable[[], int] = Lambdas.return_one

        :return: 1
        """

        return 1

    @staticmethod
    def return_true() -> bool:
        """
        Lambda that follows the Callable[[], bool] signature
        and returns True.

        >>> func: Callable[[], bool] = Lambdas.return_true

        :return: True
        """

        return True

    @staticmethod
    def return_false() -> bool:
        """
        Lambda that follows the Callable[[], bool] signature
        and returns False.

        >>> func: Callable[[], bool] = Lambdas.return_false

        :return: False
        """

        return False

    @staticmethod
    # noinspection PyUnusedLocal
    def one_arg_no_return(arg: Any) -> NoReturn:
        """
        Lambda that follows the Callable[[Any], NoReturn] signature
        and has no return and just passes.

        >>> func: Callable[[Any], NoReturn] = Lambdas.one_arg_no_return

        :return: NoReturn
        """

        pass

    @staticmethod
    # noinspection PyUnusedLocal
    def two_args_no_return(arg1: Any, arg2: Any) -> NoReturn:
        """
        Lambda that follows the Callable[[Any, Any], NoReturn] signature
        and has no return and just passes.

        >>> func: Callable[[Any, Any], NoReturn] = Lambdas.two_args_no_return

        :return: NoReturn
        """

        pass

    @staticmethod
    # noinspection PyUnusedLocal
    def three_args_no_return(arg1: Any, arg2: Any) -> NoReturn:
        """
        Lambda that follows the Callable[[Any, Any, Any], NoReturn] signature
        and has no return and just passes.

        >>> func: Callable[[Any, Any, Any], NoReturn] = Lambdas.three_args_no_return

        :return: NoReturn
        """

        pass
