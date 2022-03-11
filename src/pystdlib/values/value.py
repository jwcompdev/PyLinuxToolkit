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