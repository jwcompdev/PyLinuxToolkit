# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# value.py
# Copyright (C) 2022 JWCompDev <jwcompdev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by
# the Apache Software Foundation; either version 2.0 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License for more details.
#
# You should have received a copy of the Apache License
# along with this program.  If not, see <https://www.apache.org/licenses/>.

"""
Contains the Value class, which provides
mutable access to a value.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


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
