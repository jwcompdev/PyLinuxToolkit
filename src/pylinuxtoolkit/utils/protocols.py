# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# protocols.py
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
This file contains simple protocol classes to be used in isinstance
checks.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import runtime_checkable, Protocol, NoReturn


@runtime_checkable
class SupportsClose(Protocol):
    """An ABC with one abstract method close."""
    __slots__ = ()

    # noinspection PyMissingOrEmptyDocstring
    @abstractmethod
    def close(self) -> NoReturn:
        raise NotImplementedError


@runtime_checkable
class SupportsWith(Protocol):
    """An ABC with one abstract methods __enter__ and __exit__."""
    __slots__ = ()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        raise NotImplementedError


@runtime_checkable
class SupportsWithClose(Protocol):
    """An ABC with one abstract methods close, __enter__ and __exit__."""
    __slots__ = ()

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        raise NotImplementedError

    # noinspection PyMissingOrEmptyDocstring
    @abstractmethod
    def close(self) -> NoReturn:
        raise NotImplementedError
