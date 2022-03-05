# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# caller.py
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
Contains the Caller class, that wraps the caller of a method
to provide basic info about it.
"""
from __future__ import annotations

import inspect
import sys
from types import ModuleType

from pystdlib.values import StringValue


class Caller:
    """
    Wraps the caller of the current method
    to provide basic info about it.
    """

    def __init__(self):
        """
        Initializes the CallerWrapper instance.
        """
        frame = inspect.stack()[2][0]

        self._name = self.get_method_name_from_frame(frame)
        self._cls = self.get_class_from_frame(frame)
        self._cls_instance = self.get_class_instance_from_frame(frame)
        self._module = self.get_module_from_frame(frame)

    @staticmethod
    def get_method_name_from_frame(frame) -> str:
        """
        Retrieves the method name from the specified frame.

        :param frame: the frame to check
        :return: the method name from the specified frame
        """
        return frame.f_code.co_name

    @staticmethod
    def get_class_from_frame(frame):
        """
        Retrieves the class from the specified frame.

        :param frame: the frame to check
        :return: the class from the specified frame
        """
        args, _, _, value_dict = inspect.getargvalues(frame)
        # we check the first parameter for the frame function is
        # named 'self'
        if len(args) and args[0] == 'self':
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get('self', None)
            if instance:
                # return its class
                return getattr(instance, '__class__', None)
        # return None otherwise
        return None

    @staticmethod
    def get_class_instance_from_frame(frame):
        """
        Retrieves the class instance from the specified frame.

        :param frame: the frame to check
        :return: the class instance from the specified frame
        """
        return frame.f_locals.get('self', None)

    @staticmethod
    def get_module_from_frame(frame):
        """
        Retrieves the class object from the specified frame.

        :param frame: the frame to check
        :return: the class object from the specified frame
        """
        args, _, _, value_dict = inspect.getargvalues(frame)
        # we check the first parameter for the frame function is
        # named 'self'
        if len(args) and args[0] == 'self':
            # in that case, 'self' will be referenced in value_dict
            instance = value_dict.get('self', None)
            if instance:
                # return its class
                cls = getattr(instance, '__class__', None)
                return sys.modules[cls.__module__]
        # return None otherwise
        return None

    @property
    def name(self) -> str:
        """
        Returns the caller's name.

        :return: the caller's name
        """
        return self._name

    @property
    def cls(self) -> type | None:
        """
        Returns the caller's class.

        :return: the caller's class
        """
        return self._cls

    @property
    def cls_instance(self):
        """
        Returns the caller's class instance.

        :return: the caller's class instance
        """
        return self._cls_instance

    @property
    def cls_name(self) -> str | None:
        """
        Returns the caller's class name.

        :return: the caller's class name
        """
        if self._cls is not None:
            return self._cls.__name__
        return None

    @property
    def module(self) -> ModuleType | None:
        """
        Returns the caller's module.

        :return: the caller's module
        """
        return self._module

    @property
    def module_name(self) -> str | None:
        """
        Returns the caller's module name.

        :return: the caller's module name
        """
        if self._module is not None:
            return self._module.__name__
        return None

    @property
    def module_filename(self) -> str | None:
        """
        Returns the caller's module filename.

        :return: the caller's module filename
        """
        if self._module is not None:
            return self._module.__file__
        return None

    @property
    def package_name(self) -> str | None:
        """
        Returns the caller's package name.

        :return: the caller's package name
        """
        if self._module is not None:
            return self._module.__package__
        return None

    @property
    def root_package_name(self) -> str | None:
        """
        Returns the caller's root package name.

        :return: the caller's root package name
        """
        if self.package_name is not None:
            return self.package_name.partition('.')[0]
        return None

    @property
    def full_name(self) -> str:
        """
        Returns the caller's full name with the class included.
        If the class name is *None* then just the caller name
        is returned.

        :return: the full name
        """
        if self.cls_name is None:
            return self.name

        return f"{self.cls_name}.{self.name}"

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
        if self.module_name is None:
            if self.cls_name is None:
                return self.name

            return f"{self.cls_name}.{self.name}"

        if self.cls_name is None:
            return f"{self.module_name}.{self.name}"

        return f"{self.module_name}.{self.cls_name}.{self.name}"

    def name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the caller method matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller method matches
            the specified name, False otherwise
        """
        return self.name == comparison

    def cls_name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the caller class matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller class matches
            the specified name, False otherwise
        """
        return self.cls_name == comparison

    def module_name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the caller module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller module
            matches the specified module, False otherwise
        """
        return self.module_name == comparison

    def module_filename_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the caller module
        filename matches the specified module filename, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the caller module
            filename matches the specified module filename,
            False otherwise
        """
        return self.module_filename == comparison

    def path_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the caller's full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the caller's full path
            matches the specified path, False otherwise
        """
        return self.full_path == comparison
