# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# caller.py
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
Contains the Caller class, that
wraps the caller of the current method
to provide basic info about it.
"""
from __future__ import annotations

from types import ModuleType

from pystdlib.introspection import CallFrame
from pystdlib.str_utils import build_repr


class Caller:
    """
    Wraps the caller of the current method
    to provide basic info about it.
    """

    def __init__(self):
        """Initializes the CallerWrapper instance."""
        # Grabs the stack from the location the "__init__"
        # method was called.
        self._frame = CallFrame.current().parent.parent

    def __repr__(self):
        return build_repr(self)

    @property
    def name(self) -> str:
        """
        Returns the caller's name.

        This is equivalent to "obj.__name__".

        :return: the caller's name
        """
        return self._frame.current_method_name

    @property
    def cls(self) -> type | None:
        """
        Returns the caller's class.

        :return: the caller's class
        """
        return self._frame.current_cls

    @property
    def cls_instance(self):
        """
        Returns the caller's class instance.

        :return: the caller's class instance
        """
        return self._frame.current_cls_instance

    @property
    def cls_name(self) -> str | None:
        """
        Returns the caller's class name.

        :return: the caller's class name
        """
        return self._frame.current_cls_name

    @property
    def module(self) -> ModuleType | None:
        """
        Returns the caller's module.

        :return: the caller's module
        """
        return self._frame.current_module

    @property
    def module_name(self) -> str | None:
        """
        Returns the caller's module name.

        :return: the caller's module name
        """
        return self._frame.cu

    @property
    def module_filename(self) -> str | None:
        """
        Returns the caller's module filename.

        :return: the caller's module filename
        """
        return self._frame.current_module_filename

    @property
    def package_name(self) -> str | None:
        """
        Returns the caller's package name.

        :return: the caller's package name
        """
        return self._frame.current_package_name

    @property
    def root_package_name(self) -> str | None:
        """
        Returns the caller's root package name.

        :return: the caller's root package name
        """
        return self._frame.current_root_package_name

    @property
    def full_name(self) -> str:
        """
        Returns the caller's full name with the class included.
        If the class name is *None* then just the caller name
        is returned.

        :return: the full name
        """
        return self._frame.current_full_name

    @property
    def full_path(self) -> str:
        """
        Returns the caller's full path with class and package name.
        If the class name is *None* then just the module and
        caller name is returned ("module.caller").
        If the module name is *None* then just the class and
        caller name is returned ("class.caller").
        If both are *None* then just the caller name is
        returned.

        :return: the full path
        """
        return self._frame.current_full_path

    def name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the caller method matches
        the specified name or names, False otherwise.

        :param comparison: the name or names to check against
        :return: True if the name of the caller method matches
            the specified name, False otherwise
        """
        return self.name in list(comparison)

    def cls_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the caller class matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller class matches
            the specified name, False otherwise
        """
        return self.cls_name in list(comparison)

    def module_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the caller module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller module
            matches the specified module, False otherwise
        """
        return self.module_name in list(comparison)

    def module_filename_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the caller module
        filename matches the specified module filename, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller module
            filename matches the specified module filename,
            False otherwise
        """
        return self.module_filename in list(comparison)

    def path_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the caller's full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the caller's full path
            matches the specified path, False otherwise
        """
        return self.full_path in list(comparison)
