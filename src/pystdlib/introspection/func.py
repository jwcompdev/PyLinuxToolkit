# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# func.py
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
Contains the Func class, that
wraps a function
to provide basic info about it.
"""
from __future__ import annotations

import functools
import inspect
import time
import typing
from inspect import Parameter
from types import ModuleType, CodeType

from pystdlib.introspection.exceptions import FuncArgsMismatchError
from pystdlib.introspection.caller import Caller
from pystdlib.introspection.object_info import ObjectInfo
from pystdlib.introspection.signature import Signature
from pystdlib.types import NoneType
from pystdlib.values import StringValue

if typing.TYPE_CHECKING:
    from pystdlib.event import Event, Namespace


class Func:
    """Wraps a function to provide basic info about it."""

    def __init__(
        self,
        func: typing.Callable,
        *,
        strict: bool = False,
        strict_args: bool = False,
        strict_return: bool = False,
        sleep_after: int = 0,
        sleep_before: int = 0,
        debug: bool = False,
    ):
        """
        Initializes the FuncWrapper instance.

        :param func: the function to wrap
        :param strict: if True enables both strict arg checking and
            strict return checking
        :param strict_args: if True enables strict arg checking
        :param strict_return: if True enables strict return checking
        :param sleep_after: if non-zero sleeps after the function is
            called for the specified seconds
        :param sleep_before: if non-zero sleeps before the function is
            called for the specified seconds
        :param debug: if True enables auto-printing of debug info
        """
        if func is None:
            raise ValueError("'func' must not be None!")

        self._func = func
        self._signature = Signature(func)

        self._info = ObjectInfo.from_func(func)

        # Call Options
        if strict:
            self._strict_args = True
            self._strict_return = True
        else:
            self._strict_args = strict_args
            self._strict_return = strict_return

        self._sleep_after: int = sleep_after
        self._sleep_before: int = sleep_before
        self._fire_event_before: bool = False
        self._fire_event_after: bool = False
        self._before_event: Event | None = None
        self._after_event: Event | None = None
        self._before_event_namespace: str = ""
        self._after_event_namespace: str = ""

        self._debug = debug
        self._last_run_time = 0.0
        self._last_result = None
        self._last_args = []
        self._last_kwargs = {}
        self._last_caller = None
        self._number_calls = 0

        self.__name__ = self.name
        # noinspection PyUnresolvedReferences
        self.__closure__ = self._func.__closure__
        self.__qualname__ = self._func.__qualname__
        # noinspection PyUnresolvedReferences
        self.__globals__ = self._func.__globals__
        self.__doc__ = self.doc
        self.__module__ = self.module_name
        self.__defaults__ = self.defaults
        # noinspection SpellCheckingInspection
        self.__kwdefaults__ = self.kwdefaults
        self.__code__ = self.code
        self.__annotations__ = self.annotations

    @functools.wraps
    def __call__(self, *args, **kwargs):
        """
        Calls the function.

        Each time the function is called the execution is timed
        using "time.perf_counter" and saved to "last_run_time".

        :param args: the args to pass to the function
        :param kwargs: the kwargs to pass to the function
        :return: the function's return value
        """
        # Retrieve the caller info
        self._last_caller = Caller()

        # Check if args match
        if self._strict_args:
            self._signature.verify_args(*args, **kwargs)

        # Initiate perf counter
        timer = time.perf_counter

        # Fire 'before' event if enabled and setup
        if self._fire_event_before and self._before_event is not None:
            self._before_event.fire(self._before_event_namespace, func=self)

        # Sleep if 'sleep before' time is > 0
        time.sleep(self._sleep_before)

        # Start perf counter
        start = timer()

        # Call the function with the passed args and kwargs
        result = self._func(*args, **kwargs)

        # End perf counter
        end = timer()

        # Sleep if 'sleep after' is > 0
        time.sleep(self._sleep_after)

        # Fire 'after' event if enabled and setup
        if self._fire_event_after and self._after_event is not None:
            self._after_event.fire(self._after_event_namespace, func=self)

        # Save call debug info
        self._last_run_time = end - start
        self._last_args = args
        self._last_kwargs = kwargs
        self._number_calls += 1
        self._last_result = result

        # Verify return value
        if self._strict_return:
            return_annotation = self._signature.return_annotation

            if return_annotation is Parameter.empty:
                return_annotation = NoneType

            match = isinstance(result, return_annotation) or issubclass(
                type(result), return_annotation
            )

            if not match:
                raise FuncArgsMismatchError(
                    "Return Type Mismatch:"
                    f"\n>>> Expected: '{return_annotation.__name__}',"
                    f" Found: '{type(result).__name__}'"
                    f" with value '{str(result)}'"
                )

        # If 'debug' enabled print trace to the console
        if self._debug:
            print(self.last_trace)

        return result

    def __str__(self):
        # noinspection PyUnresolvedReferences
        return self._func.__str__()

    def __repr__(self):
        # noinspection PyUnresolvedReferences
        return self._func.__repr__()

    @property
    def name(self) -> str:
        """
        Returns the function's name.

        This is equivalent to "func.__name__".

        :return: the function's name
        """
        return self._info.name

    @property
    def cls(self) -> type | None:
        """
        Returns the function's parent class.

        :return: the parent class
        """
        return self._info.cls

    @property
    def cls_name(self) -> str | None:
        """
        Returns the function's parent class name.

        :return: the parent class name
        """
        return self._info.cls_name

    @property
    def module(self) -> ModuleType | None:
        """
        Returns the function's parent module.

        This is equivalent to calling "inspect.getmodule(func)".

        :return: the parent module
        """
        return self._info.module

    @property
    def module_name(self) -> str | None:
        """
        Returns the function's parent module name.

        :return: the parent module name
        """
        return self._info.module_name

    @property
    def module_filename(self) -> str | None:
        """
        Returns the function's module filename.

        :return: the module filename
        """
        return self._info.module_filename

    @property
    def package_name(self) -> str | None:
        """
        Returns the function's package name.

        :return: the package name
        """
        return self._info.package_name

    @property
    def root_package_name(self) -> str | None:
        """
        Returns the function's root package name.

        :return: the root package name
        """
        return self._info.root_package_name

    @property
    def full_name(self) -> str:
        """
        Returns the function's full name with the class included.
        If the class name is *None* then just the function name
        is returned.

        :return: the full name
        """
        return self._info.full_name

    @property
    def full_path(self) -> str:
        """
        Returns the function's full path with class and package name.
        If the class name is *None* then just the module and
        function name is returned ("module.function").
        If the module name is *None* then just the class and
        function name is returned ("class.function").
        If both are *None* then just the function name is
        returned.

        :return: the full path
        """
        return self._info.full_path

    def name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the function matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function matches
            the specified name, False otherwise
        """
        return self.name in list(comparison)

    def cls_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the function's parent class
        matches the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent class
            matches the specified name, False otherwise
        """
        return self.cls_name in list(comparison)

    def module_name_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the function's parent module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent module
            matches the specified module, False otherwise
        """
        return self.module_name in list(comparison)

    def module_filename_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the function's parent module
        filename matches the specified module filename, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent module
            filename matches the specified module filename,
            False otherwise
        """
        return self.module_filename in list(comparison)

    def path_matches(self, *comparison: str) -> bool:
        """
        Returns True if the name of the function's full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the function's full path
            matches the specified path, False otherwise
        """
        return self.full_path in list(comparison)

    @property
    def doc(self) -> str:
        # noinspection GrazieInspection
        """
        Get the documentation string for an object.

        All tabs are expanded to spaces. To clean up docstrings that are
        indented to line up with blocks of code, any whitespace that can be
        uniformly removed from the second line onwards is removed.

        This is equivalent to calling "inspect.getdoc(func)"
        """
        return inspect.getdoc(self._func)

    @property
    def code(self) -> CodeType:
        """
        Returns the code object representing the
        compiled function body.

        :return: the code object representing the
        compiled function body
        """
        # noinspection PyUnresolvedReferences
        return self._func.__code__

    @property
    def defaults(self) -> tuple | None:
        """
        Returns a tuple containing default argument values for those
        arguments that have defaults, or None if no arguments have a
        default value.

        :return: a tuple containing default argument values
        """
        # noinspection PyUnresolvedReferences
        return self._func.__defaults__

    # noinspection SpellCheckingInspection
    @property
    def kwdefaults(self) -> dict[str, typing.Any]:
        """
        Returns a dict containing defaults for keyword-only parameters.

        :return: a dict containing defaults for keyword-only parameters
        """
        # noinspection PyUnresolvedReferences
        return self._func.__kwdefaults__

    @property
    def signature(self) -> Signature:
        """
        Returns the signature of the function.

        :return: the signature of the function
        """
        return self._signature

    @property
    def attributes(self) -> list[tuple[str, typing.Any]]:
        """
        Return all attributes as (name, value) pairs sorted by name.

        This is equivalent to calling
        "inspect.getmembers(func)".

        :return: all attributes as (name, value) pairs sorted by name
        """
        return inspect.getmembers(self._func)

    @property
    def annotations(self) -> dict[str, typing.Any]:
        """
        Returns a dict containing annotations of parameters. The keys
        of the dict are the parameter names, and 'return' for the
        return annotation, if provided.

        :return: a dict containing annotations of parameters
        """
        # noinspection PyUnresolvedReferences
        return self._func.__annotations__

    @property
    def last_run_time(self) -> float:
        """
        Returns the execution time of the last time the function
        was called.

        NOTE: if you pass this to the "print()" function it will
        print inspect scientific notation. To avoid that use
        call "last_run_time_string" instead.

        :return: the execution time of the last time the function
        was called
        """
        return self._last_run_time

    @property
    def last_run_time_string(self) -> str:
        """
        Returns the execution time of the last time the function
        was called, as a formatted string, so it doesn't print in
        scientific notation when using the "print()" function.

        :return: the execution time of the last time the function
        was called, as a string
        """
        return (
            f"{self._last_run_time:.35f}" if self._last_run_time is not None else ""
        ).rstrip("0")

    @property
    def last_args(self) -> list:
        """
        Returns the last args passed to the function.

        :return: the last args passed to the function
        """
        return self._last_args

    @property
    def last_kwargs(self) -> dict:
        """
        Returns the last kwargs passed to the function.

        :return: the last kwargs passed to the function
        """
        return self._last_kwargs

    @property
    def last_caller(self) -> Caller:
        """
        Returns info about the caller that called the function
        last.

        :return: the last caller
        """
        return self._last_caller

    @property
    def last_trace(self) -> str:
        """
        Returns a string with some basic info about the last time
        the function was called.

        :return: a string with some basic info about the last time
        the function was called
        """
        return (
            f"'{self.full_name}' last execution took:\n"
            f"{self.last_run_time_string} seconds\n"
            "and was last called with:\n"
            f"args: {self._last_args}\n"
            f"kwargs: {self._last_kwargs}"
        )

    @property
    def last_result(self) -> typing.Any | None:
        """
        Returns the value returned the last time the function
        was called.

        :return: the value returned the last time the function
        was called
        """
        return self._last_result

    @property
    def last_result_type(self) -> type | None:
        """
        Returns the object type of the value returned the last
        time the function was called.

        :return: the object type of the value returned the last
        time the function was called
        """
        return type(self._last_result)

    @property
    def number_of_calls(self) -> int:
        """
        Returns the number of times the function has been called.

        :return: the number of times the function has been called
        """
        return self._number_calls

    def enable_strict_checking(self) -> Func:
        """
        Enables both strict arg type checking and strict return
        value type checking.

        :return: this instance for use in method chaining
        """
        self._strict_args = True
        self._strict_return = True

        return self

    def disable_strict_checking(self) -> Func:
        """
        Disables both strict arg type checking and strict return
        value type checking.

        :return: this instance for use in method chaining
        """
        self._strict_args = False
        self._strict_return = False

        return self

    @property
    def strict_arg_checking(self) -> bool:
        """
        Returns True if strict arg type checking is enabled.

        :return: True if strict arg type checking is enabled
        """
        return self._strict_args

    @strict_arg_checking.setter
    def strict_arg_checking(self, value: bool) -> typing.NoReturn:
        """
        Sets the value of strict arg type checking.

        :param value: the value to set
        """
        self._strict_args = value

    @property
    def strict_return_checking(self) -> bool:
        """
        Returns True if strict return type checking is enabled.

        :return: True if strict return type checking is enabled
        """
        return self._strict_return

    @strict_return_checking.setter
    def strict_return_checking(self, value: bool) -> typing.NoReturn:
        """
        Sets the value of strict return type checking.

        :param value: the value to set
        """
        self._strict_return = value

    def fire_event_before(
        self, event: Event, namespace: str | StringValue | Namespace
    ) -> Func:
        """
        Fires the specified event at the specified namespace right
        before the function is called.

        :param event: the event to fire
        :param namespace: the namespace to use when firing
            the event
        :return: this instance for use in method chaining
        """
        func_param = Parameter("func", Parameter.POSITIONAL_OR_KEYWORD, annotation=Func)
        from pystdlib.event import Event

        if (
            isinstance(event, Event)
            or issubclass(type(event), Event)
            and event.signature == Signature(func=func_param)
        ):
            self._before_event = event
            self._before_event_namespace = namespace
            self._fire_event_before = True

        return self

    def fire_event_after(
        self, event: Event, namespace: str | StringValue | Namespace
    ) -> Func:
        """
        Fires the specified event at the specified namespace right
        after the function is called.

        :param event: the event to fire
        :param namespace: the namespace to use when firing
            the event
        :return: this instance for use in method chaining
        """
        func_param = Parameter("func", Parameter.POSITIONAL_OR_KEYWORD, annotation=Func)
        from pystdlib.event import Event

        if (
            isinstance(event, Event)
            or issubclass(type(event), Event)
            and event.signature == Signature(func=func_param)
        ):
            self._after_event = event
            self._after_event_namespace = namespace
            self._fire_event_after = True

        return self

    def enable_before_event(self) -> Func:
        """
        Enables the before event if already setup.

        :return: this instance for use in method chaining
        """
        if self._before_event is not None:
            self._fire_event_before = True
        return self

    def disable_before_event(self) -> Func:
        """
        Disables the before event.

        :return: this instance for use in method chaining
        """
        self._fire_event_before = False
        return self

    def enable_after_event(self) -> Func:
        """
        Enables the after event if already setup.

        :return: this instance for use in method chaining
        """
        if self._after_event is not None:
            self._fire_event_after = True
        return self

    def disable_after_event(self) -> Func:
        """
        Disables the after event.

        :return: this instance for use in method chaining
        """
        self._fire_event_after = False
        return self

    @property
    def sleep_before(self) -> int:
        """
        Returns the amount of seconds to sleep before
        the function is called.

        :return: the amount of seconds to sleep before
        the function is called
        """
        return self._sleep_before

    @sleep_before.setter
    def sleep_before(self, seconds: int):
        """
        Sets the amount of seconds to sleep before
        the function is called.

        :param seconds: the amount of seconds to sleep before
        the function is called
        """
        self._sleep_before = seconds

    @property
    def sleep_after(self) -> int:
        """
        Returns the amount of seconds to sleep after
        the function is called.

        :return: the amount of seconds to sleep after
        the function is called
        """
        return self._sleep_after

    @sleep_after.setter
    def sleep_after(self, seconds: int):
        """
        Sets the amount of seconds to sleep after
        the function is called.

        :param seconds: the amount of seconds to sleep after
        the function is called
        """
        self._sleep_after = seconds

    @property
    def debug(self) -> bool:
        """
        Returns True if debug printing is enabled.

        :return: if debug printing is enabled
        """
        return self._debug

    def enable_debug(self) -> Func:
        """
        Enables debug printing.

        :return: this instance for use in method chaining
        """
        self._debug = True

        return self

    def disable_debug(self) -> Func:
        """
        Disables debug printing.

        :return: this instance for use in method chaining
        """
        self._debug = False

        return self
