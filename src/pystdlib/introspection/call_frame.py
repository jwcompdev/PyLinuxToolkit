# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# call_frame.py
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
Contains the CallFrame class, that represents a call frame.
"""
from __future__ import annotations

import inspect
import sys
from inspect import Traceback
from types import FrameType, CodeType
from typing import Optional, Callable, Any


class CallFrame:
    """
    Represents a call frame - an element of the call stack.
    It keeps track of local and closure variables.

    Although ``CallFrame`` does not inherit from :data:`types.FrameType`,
    they can be used just like regular frame objects.

    Note that storing CallFrames in variables can create reference
    cycles where a frame contains a reference to itself. To avoid
    this, CallFrames can be used as context managers - upon exit,
    the reference to the underlying frame object is released::

        with CallFrame.current() as frame:
            ...  # do stuff with the frame
        # at this point, the frame has become unusable
    """

    __slots__ = ('__frame',)

    def __init__(self, frame):
        """
        Creates a new ``CallFrame`` from a ``CallFrame``
        or :data:`types.FrameType` object.

        :param frame: An existing frame object
        """
        # noinspection PyTypeChecker
        if isinstance(frame, __class__):
            # noinspection PyUnresolvedReferences
            frame = frame.__frame

        self.__frame = frame

    @classmethod
    def current(cls) -> CallFrame:
        """
        Retrieves the current call frame.

        :return: the current call frame
        """
        return cls(inspect.currentframe().f_back)

    @classmethod
    def from_frame(cls, frame):
        """
        Creates a new ``CallFrame`` from a ``CallFrame``
        or :data:`types.FrameType` object.

        This is equivalent to calling ``CallFrame(frame)``.
        """
        return cls(frame)

    def __getattr__(self, attr):
        return getattr(self.__frame, attr)

    def __eq__(self, other):
        # noinspection PyTypeChecker
        if isinstance(other, __class__):
            # noinspection PyUnresolvedReferences
            return self.__frame == other.__frame

        if isinstance(other, FrameType):
            return self.__frame == other

        return NotImplemented

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__frame = None

    @property
    def frame(self):
        """
        Returns the wrapped frame.

        :return: the wrapped frame
        """
        return self.__frame

    @property
    def parent(self) -> CallFrame | None:
        """
        Returns the next frame one level higher on the call stack.

        :return: the next frame one level higher on the call stack
        """
        parent = self.__frame.f_back
        if parent is None:
            return None

        cls = type(self)
        return cls(parent)

    @property
    def builtins(self) -> dict[str, Any]:
        """
        Returns the builtins seen by this frame.

        :return: the builtins seen by this frame
        """
        return self.__frame.f_builtins

    @property
    def globals(self) -> dict[str, Any]:
        """
        Returns the global scope seen by this frame.

        :return: the global scope seen by this frame
        """
        return self.__frame.f_globals

    @property
    def locals(self) -> dict[str, Any]:
        """
        Returns the frame's local variable scope.

        :return: the frame's local variable scope
        """
        return self.__frame.f_locals

    @property
    def current_line_num(self) -> int:
        """
        Returns the current line number of the frame.

        :return: the current line number of the frame
        """
        return self.__frame.f_lineno

    @property
    def code_object(self) -> CodeType:
        """
        Returns the code object being executed in this frame.

        :return: the code object being executed in this frame
        """
        return self.__frame.f_code

    @property
    def current_method_name(self) -> str:
        """
        Retrieves the method name from the frame.

        :return: the method name from the frame
        """
        return self.code_object.co_name

    @property
    def current_cls_instance(self) -> type | None:
        """
        Retrieves the class instance from the frame.

        :return: the class instance from the frame
        """
        return self.locals.get('self', None)

    @property
    def current_cls(self) -> Any | None:
        """
        Retrieves the class from the frame.

        :return: the class from the frame
        """
        instance = self.current_cls_instance
        if instance is not None:
            # return its class
            return getattr(instance, '__class__', None)
        # return None otherwise
        return None

    @property
    def current_cls_name(self) -> str | None:
        """
        Returns the class name from the frame.

        :return: the class name from the frame
        """
        if self.current_cls is not None:
            return self.current_cls.__name__

        return None

    @property
    def current_module(self):
        """
        Retrieves the module from the frame.

        :return: the module from the frame
        """
        module = None

        cls = self.current_cls
        if cls is not None:
            module = sys.modules[cls.__module__]

        if module is None:
            module = sys.modules["__main__"]

        return module

    @property
    def current_module_name(self) -> str | None:
        """
        Returns the module name from the frame.

        :return: the module name from the frame
        """
        if self.current_module is not None:
            return self.current_module.__name__

        return None

    @property
    def current_module_filename(self) -> str | None:
        """
        Returns the module filename from the frame.

        :return: the module filename from the frame
        """
        if self.current_module is not None \
                and hasattr(self.current_module, "__file__"):
            return self.current_module.__file__

        return None

    @property
    def current_package_name(self) -> str | None:
        """
        Returns the package name from the frame.

        :return: the package name from the frame
        """
        if self.current_module is not None \
                and hasattr(self.current_module, "__package__"):
            return self.current_module.__package__

        return None

    @property
    def current_root_package_name(self) -> str | None:
        """
        Returns the root package name from the frame.

        :return: the root package name from the frame
        """
        if self.current_package_name is not None:
            return self.current_package_name.partition('.')[0]

        return None

    @property
    def current_full_name(self):
        """
        Returns the full name with the class included.
        If the class name is *None* then just the method name
        is returned.

        :return: the full name
        """
        if self.current_cls is not None:
            return f"{self.current_cls_name}.{self.current_method_name}"

        return self.current_method_name

    @property
    def current_full_path(self):
        """
        Returns the full path with class and package name.
        If the class name is *None* then just the module and
        method name is returned ("module.object").
        If the module name is *None* then just the class and
        method name is returned ("class.object").
        If both are *None* then just the method name is
        returned.

        :return: the full path
        """
        if self.current_module_name is None:
            if self.current_cls_name is None:
                return self.current_method_name

            return f"{self.current_cls_name}" \
                   f".{self.current_method_name}"

        if self.current_cls_name is None:
            return f"{self.current_module_name}" \
                   f".{self.current_method_name}"

        return f"{self.current_module_name}" \
               f".{self.current_cls_name}" \
               f".{self.current_method_name}"

    @property
    def file_name(self) -> str:
        """
        Returns the name of the file in which this frame's
        code was defined.

        :return: the name of the file in which this frame's
            code was defined
        """
        return self.code_object.co_filename

    @property
    def scope_name(self) -> str:
        """
        Returns the name of the scope in which this frame's
        code was defined.
        In case of a function, the function's name.
        In case of a class, the class's name.
        In any other case, whichever name the interpreter
        assigned to that scope.

        :return: the name of the scope in which this frame's
        code was defined
        """
        return self.code_object.co_name

    @property
    def traceback(self) -> Traceback:
        """
        Get information about a frame object.

        A tuple of five things is returned: the filename, the line number of
        the current line, the function name, a list of lines of context from
        the source code, and the index of the current line within that list.
        The optional second argument specifies the number of lines of context
        to return, which are centered around the current line.

        :return: information about a frame object
        """
        return inspect.getframeinfo(self.__frame)

    def resolve_name(self, name: str) -> Any:
        """
        Resolves a variable name, returning the variable's value.

        NOTE: Closure variables don't have a named associated with them,
        which means they cannot be looked up with this function.
        This includes variables marked as ``nonlocal``.

        :param name: The name of the variable you want to look up
        :return: The value mapped to the given name
        :raises NameError: If no matching variable is found
        """
        try:
            return self.locals[name]
        except KeyError:
            pass

        try:
            return self.globals[name]
        except KeyError:
            pass

        try:
            return self.builtins[name]
        except KeyError:
            pass

        msg = "Name {!r} not visible from frame {!r}"
        raise NameError(msg.format(name, self))

    def get_surrounding_function(self) -> Optional[Callable]:
        """
        Finds and returns the function in which the code of this
        frame was defined.

        If the function can't be found, ``None`` is returned.

        :return: The calling function object or ``None``
            if it can't be found
        """
        parent = self.parent
        if parent is None:
            return None

        func_name = self.scope_name
        try:
            function = parent.resolve_name(func_name)
        except NameError:
            return None
        finally:
            del parent

        # Make sure the name referred to the correct function
        if getattr(function, '__code__', None) is not self.code_object:
            return None

        return function

    def name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the current method matches
        the specified name or names, False otherwise.

        :param comparison: the name or names to check against
        :return: True if the name of the current method matches
            the specified name, False otherwise
        """
        return self.current_method_name in list(comparison)

    def cls_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the current class matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the current class matches
            the specified name, False otherwise
        """
        return self.current_cls_name in list(comparison)

    def module_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the current module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the current module
            matches the specified module, False otherwise
        """
        return self.current_module_name in list(comparison)

    def module_filename_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the current module
        filename matches the specified module filename,
        False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the current module
            filename matches the specified module filename,
            False otherwise
        """
        return self.current_module_filename in list(comparison)

    def path_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the current full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the current full path
            matches the specified path, False otherwise
        """
        return self.current_full_path in list(comparison)
