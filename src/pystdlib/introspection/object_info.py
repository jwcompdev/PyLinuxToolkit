# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# object_info.py
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
Contains the ObjectInfo class, an object that
contains basic info about another object.
"""
from __future__ import annotations

import inspect
import sys
from dataclasses import dataclass, field
from types import ModuleType

from pystdlib.introspection import CallFrame


@dataclass
class ObjectInfo:
    """Contains basic info about an object."""

    _name: str = field(default="")
    _cls: type = field(default=None)
    _module: ModuleType = field(default=None)
    _cls_name: str | None = field(init=False, default=None)
    _module_name: str | None = field(init=False, default=None)
    _module_filename: str | None = field(init=False, default=None)
    _package_name: str | None = field(init=False, default=None)
    _root_package_name: str | None = field(init=False, default=None)
    _full_name: str | None = field(init=False, default=None)
    _full_path: str | None = field(init=False, default=None)

    def __post_init__(self):
        if self._cls is not None:
            self._cls_name = self._cls.__name__
            self._full_name = f"{self._cls_name}.{self._name}"
        else:
            self._full_name = self._name

        if self._module is not None:
            self._module_name = self._module.__name__

            if hasattr(self._module, "__file__"):
                self._module_filename = self._module.__file__

            if hasattr(self._module, "__package__"):
                self._package_name = self._module.__package__

        if self._package_name is not None:
            self._root_package_name = self._package_name.partition(".")[0]

        if self._module_name is None:
            if self._cls_name is None:
                self._full_path = self._name
            else:
                self._full_path = f"{self._cls_name}.{self._name}"

        if self._cls_name is None:
            self._full_path = f"{self._module_name}.{self._name}"
        else:
            self._full_path = f"{self._module_name}.{self._cls_name}.{self._name}"

    @property
    def name(self) -> str:
        """
        Returns the object's name.

        This is equivalent to "obj.__name__".

        :return: the object's name
        """
        return self._name

    @property
    def cls(self) -> type | None:
        """
        Returns the object's parent class.

        :return: the parent class
        """
        return self._cls

    @property
    def cls_name(self) -> str | None:
        """
        Returns the object's parent class name.

        :return: the parent class name
        """
        return self._cls_name

    @property
    def module(self) -> ModuleType | None:
        """
        Returns the object's parent module.

        This is equivalent to calling "inspect.getmodule(obj)".

        :return: the parent module
        """
        return self._module

    @property
    def module_name(self) -> str | None:
        """
        Returns the object's parent module name.

        :return: the parent module name
        """
        return self._module_name

    @property
    def module_filename(self) -> str | None:
        """
        Returns the object's module filename.

        :return: the module filename
        """
        return self._module_filename

    @property
    def package_name(self) -> str | None:
        """
        Returns the object's package name.

        :return: the package name
        """
        return self._package_name

    @property
    def root_package_name(self) -> str | None:
        """
        Returns the object's root package name.

        :return: the root package name
        """
        return self._root_package_name

    @property
    def full_name(self) -> str:
        """
        Returns the object's full name with the class included.
        If the class name is *None* then just the object name
        is returned.

        :return: the full name
        """
        return self._full_name

    @property
    def full_path(self) -> str:
        """
        Returns the object's full path with class and package name.
        If the class name is *None* then just the module and
        object name is returned ("module.object").
        If the module name is *None* then just the class and
        object name is returned ("class.object").
        If both are *None* then just the object name is
        returned.

        :return: the full path
        """
        return self._full_path

    @staticmethod
    def _get_parent_class(meth) -> type | None:
        """
        Returns the class of the parent of the specified object.

        :param meth: the object to check
        :return: the class of the parent of the specified object
        """
        if inspect.isclass(meth):
            return type(meth)

        if inspect.ismethod(meth) or (
            inspect.isbuiltin(meth)
            and getattr(meth, "__self__", None) is not None
            and getattr(meth.__self__, "__class__", None)
        ):
            for cls in inspect.getmro(meth.__self__.__class__):
                if meth.__name__ in cls.__dict__:
                    return cls
            meth = getattr(meth, "__func__", meth)  # fallback to __qualname__ parsing

        if inspect.isfunction(meth):
            cls = getattr(
                inspect.getmodule(meth),
                meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
                None,
            )
            if isinstance(cls, type):
                return cls

        # noinspection SpellCheckingInspection
        return getattr(meth, "__objclass__", None)  # handle special descriptor objects

    @staticmethod
    def _get_name_from_frame(frame: CallFrame) -> str:
        """
        Retrieves the method name from the specified frame.

        :param frame: the frame to check
        :return: the method name from the specified frame
        """
        return frame.code_object.co_name

    @staticmethod
    def _get_class_from_frame(frame: CallFrame):
        """
        Retrieves the class from the specified frame.

        :param frame: the frame to check
        :return: the class from the specified frame
        """
        instance = frame.locals.get("self", None)
        if instance:
            # return its class
            return getattr(instance, "__class__", None)
        # return None otherwise
        return None

    @staticmethod
    def _get_module_from_frame(frame: CallFrame):
        """
        Retrieves the module from the specified frame.

        :param frame: the frame to check
        :return: the module from the specified frame
        """
        module = None
        instance = frame.locals.get("self", None)
        if instance:
            # return its class
            cls = getattr(instance, "__class__", None)
            module = sys.modules[cls.__module__]

        if module is None:
            module = sys.modules["__main__"]

        # return None otherwise
        return module

    @classmethod
    def from_frame(cls, stack_frame: CallFrame) -> ObjectInfo | None:
        """
        Creates a new instance from a CallFrame.

        :param stack_frame: the call frame
        :return: a new instance of ObjectInfo
        """
        if stack_frame is not None:
            _name = cls._get_name_from_frame(stack_frame)
            _cls = cls._get_class_from_frame(stack_frame)
            _module = cls._get_module_from_frame(stack_frame)

            return cls(_name, _cls, _module)

            # if _module is None:
            #     # Shouldn't ever happen but if it does at least we
            #     # should be able to get the module filename
            #     _module_filename = stack_frame.traceback.filename

        return None

    @classmethod
    def from_func(cls, func) -> ObjectInfo | None:
        """
        Creates a new instance from a function.

        :param func: the function
        :return: a new instance of ObjectInfo
        """
        if func is not None:
            _name = func.__name__
            _cls = cls._get_parent_class(func)
            _module = inspect.getmodule(func)

            return cls(_name, _cls, _module)

        return None

    def name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the object matches
        the specified name or names, False otherwise.

        :param comparison: the name or names to check against
        :return: True if the name of the object matches
            the specified name, False otherwise
        """
        return self.name in list(comparison)

    def cls_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the object's class matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the object's class matches
            the specified name, False otherwise
        """
        return self.cls_name in list(comparison)

    def module_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the object module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the object module
            matches the specified module, False otherwise
        """
        return self.module_name in list(comparison)

    def module_filename_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the object's module
        filename matches the specified module filename, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the object's module
            filename matches the specified module filename,
            False otherwise
        """
        return self.module_filename in list(comparison)

    def path_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the object's full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the object's full path
            matches the specified path, False otherwise
        """
        return self.full_path in list(comparison)
