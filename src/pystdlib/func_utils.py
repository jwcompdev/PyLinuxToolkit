# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# func_utils.py
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
Contains the FuncWrapper class, that wraps a function
to provide basic info about it.
"""
from __future__ import annotations

import inspect
import typing
from inspect import Parameter
from types import ModuleType

from pystdlib.logged import Logged
from pystdlib.types import is_instance, is_subclass, get_type_from_name
from pystdlib.values import StringValue


class FuncInfo:
    """Wraps a function to provide basic info about it."""

    def __init__(self, func):
        """
        Initializes the FuncWrapper instance.

        :param func: the function to wrap
        """
        self._func = func
        self._name = func.__name__
        self._doc = inspect.getdoc(func)
        self._signature = Signature(func)
        self._cls = self._get_method_parent(func)
        self._module = inspect.getmodule(func)

    def __name__(self):
        return self._name

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    @staticmethod
    def _get_method_parent(meth) -> type | None:
        """
        Returns the class of the parent of the specified method.

        :param meth: the method to check
        :return: the class of the parent of the specified method
        """
        if inspect.ismethod(meth) \
                or (inspect.isbuiltin(meth)
                    and getattr(meth, '__self__', None) is not None
                    and getattr(meth.__self__, '__class__', None)):
            for cls in inspect.getmro(meth.__self__.__class__):
                if meth.__name__ in cls.__dict__:
                    return cls
            meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(inspect.getmodule(meth),
                          meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                          None)
            if isinstance(cls, type):
                return cls
        # noinspection SpellCheckingInspection
        return getattr(meth, '__objclass__', None)  # handle special descriptor objects

    @property
    def name(self) -> str:
        """
        Returns the function's name.

        :return: the function's name
        """
        return self._name

    @property
    def cls(self) -> type | None:
        """
        Returns the function's parent class.

        :return: the parent class
        """
        return self._cls

    @property
    def cls_name(self) -> str | None:
        """
        Returns the function's parent class name.

        :return: the parent class name
        """
        if self._cls is not None:
            return self._cls.__name__
        return None

    @property
    def module(self) -> ModuleType | None:
        """
        Returns the function's parent module.

        :return: the parent module
        """
        return self._module

    @property
    def module_name(self) -> str | None:
        """
        Returns the function's parent module name.

        :return: the parent module name
        """
        if self._module is not None:
            return self._module.__name__
        return None

    @property
    def module_filename(self) -> str | None:
        """
        Returns the function's module filename.

        :return: the module filename
        """
        if self._module is not None:
            return self._module.__file__
        return None

    @property
    def package_name(self) -> str | None:
        """
        Returns the function's package name.

        :return: the package name
        """
        if self._module is not None:
            return self._module.__package__
        return None

    @property
    def root_package_name(self) -> str | None:
        """
        Returns the function's root package name.

        :return: the root package name
        """
        if self.package_name is not None:
            return self.package_name.partition('.')[0]
        return None

    @property
    def full_name(self) -> str:
        """
        Returns the function's full name with the class included.
        If the class name is *None* then just the function name
        is returned.

        :return: the full name
        """
        if self.cls_name is None:
            return self.name

        return f"{self.cls_name}.{self.name}"

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
        if self.module_name is None:
            if self.cls_name is None:
                return self.name

            return f"{self.cls_name}.{self.name}"

        if self.cls_name is None:
            return f"{self.module_name}.{self.name}"

        return f"{self.module_name}.{self.cls_name}.{self.name}"

    @property
    def doc(self) -> str:
        # noinspection GrazieInspection
        """
        Get the documentation string for an object.

        All tabs are expanded to spaces. To clean up docstrings that are
        indented to line up with blocks of code, any whitespace than can be
        uniformly removed from the second line onwards is removed.

        This is equivalent to running "inspect.getdoc(func)"
        """
        return self._doc

    @property
    def signature(self) -> Signature:
        """
        Returns the signature of the function.

        :return: the signature of the function
        """
        return self._signature

    def name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the function matches
        the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function matches
            the specified name, False otherwise
        """
        return self.name == comparison

    def cls_name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the function's parent class
        matches the specified name, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent class
            matches the specified name, False otherwise
        """
        return self.cls_name == comparison

    def module_name_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the function's parent module
        matches the specified module, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent module
            matches the specified module, False otherwise
        """
        return self.module_name == comparison

    def module_filename_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the function's parent module
        filename matches the specified module filename, False otherwise.

        :param comparison: the name to check against
        :return: True if the name of the function's parent module
            filename matches the specified module filename,
            False otherwise
        """
        return self.module_filename == comparison

    def path_matches(self, comparison: str | StringValue):
        """
        Returns True if the name of the function's full path
        matches the specified path, False otherwise.

        :param comparison: the path to check against
        :return: True if the name of the function's full path
            matches the specified path, False otherwise
        """
        return self.full_path == comparison


class FuncSignatureError(Exception):
    """The FuncSignatureError."""


class FuncArgsMismatchError(Exception):
    """The FuncArgsMismatchError."""


class Signature(inspect.Signature, Logged):
    """Represents a function parameter signature."""

    @staticmethod
    def _format_annotation(annotation, base_module=None):
        if getattr(annotation, '__module__', None) == 'typing':
            return repr(annotation).replace('typing.', '')
        if isinstance(annotation, type):
            if annotation.__module__ in ('builtins', base_module):
                return annotation.__qualname__
            return annotation.__module__ + '.' + annotation.__qualname__
        return repr(annotation)

    @staticmethod
    def _parse_name_for_error(value) -> str:
        if str(value).startswith("<class"):
            return value.__name__

        return str(value)

    @classmethod
    def from_function(cls, func):
        """Constructs Signature for the given python function.

        Deprecated since Python 3.5, use `Signature.from_callable()`.
        """
        # noinspection PyUnresolvedReferences
        sig = inspect.Signature.from_function(func)
        return Signature(_signature=sig)

    @classmethod
    def from_callable(cls, obj, *, follow_wrapped=True, **kwargs):
        """Constructs Signature for the given callable object."""
        sig = inspect.Signature.from_callable(obj, follow_wrapped=follow_wrapped)
        return Signature(_signature=sig)

    @staticmethod
    def _validate_type(value, type_):
        if type_ == Parameter.empty:
            return True

        return is_instance(value, type_) or is_subclass(type(value), type_)

    def __init__(self, _func=None, *, _return_type=None,
                 _signature: inspect.Signature = None,
                 _make_keyword_only: bool = False,
                 **kwargs: type | Parameter):
        """
        Initializes the Signature object.

        NOTE: all parameter names start with an '_' to prevent the
        signature names from clashing if the signature needs to
        use the same names.

        :param kwargs: the keyword signature to set
        """
        _new_signature: dict[str, Parameter] = {}

        if _func is None:
            if _signature is not None:
                super().__init__(
                    list(_signature.parameters.values()),
                    return_annotation=_signature.return_annotation,
                    __validate_parameters__=False
                )
            else:
                # Check if all values are of the type 'type'
                type_valid = True
                for value in kwargs.values():
                    if not isinstance(value, type) \
                            and "typing." not in str(value):
                        type_valid = False
                        break

                # Check if all values are of the type 'Parameter'
                param_valid = all(isinstance(value, Parameter)
                                  for value in kwargs.values())

                if type_valid:
                    if _make_keyword_only:
                        for name, type_ in kwargs.items():
                            _new_signature[name] = Parameter(
                                name, Parameter.KEYWORD_ONLY,
                                annotation=type_
                            )
                    else:
                        for name, type_ in kwargs.items():
                            _new_signature[name] = Parameter(
                                name, Parameter.POSITIONAL_OR_KEYWORD,
                                annotation=type_
                            )
                elif param_valid:
                    for name, param in kwargs.items():
                        _new_signature[name] = param
                else:
                    raise FuncSignatureError(
                        "'kwargs' has the wrong value types!")

                values = list(_new_signature.values())
                for index in range(len(values)):
                    param = values[index]
                    if type(param.annotation) is str:
                        name = param.name
                        annotation = get_type_from_name(param.annotation)
                        kind = param.kind
                        default = param.default
                        values[index] = Parameter(
                            name, kind, default=default,
                            annotation=annotation
                        )

                super().__init__(
                    values,
                    return_annotation=_return_type,
                    __validate_parameters__=False
                )
        else:
            sig = inspect.signature(_func)

            values = list(sig.parameters.values())
            for index in range(len(values)):
                param = values[index]
                if type(param.annotation) is str:
                    name = param.name
                    annotation = get_type_from_name(param.annotation)
                    kind = param.kind
                    default = param.default
                    values[index] = Parameter(
                        name, kind, default=default,
                        annotation=annotation
                    )

            super().__init__(
                values,
                return_annotation=sig.return_annotation,
                __validate_parameters__=False
            )

        _types: list[type] = [par.annotation for par
                              in list(self.parameters.values())]

        func_error = "Function signature parameters cannot be of type '%s'!"

        # Check for 'None' type
        if None in _types:
            raise FuncSignatureError(func_error % "None")

        # Check for 'NoReturn' type
        if typing.NoReturn in _types:
            raise FuncSignatureError(func_error % "typing.NoReturn")

        # Check for 'Final' type
        if any("typing.Final" in str(type_) for type_ in _types):
            raise FuncSignatureError(func_error % "typing.Final")

        for type_ in _types:
            # Check if the type is actually a type or a type hint
            if type_ is not Parameter.empty \
                    and type != type_.__class__ \
                    and not str(typing.get_origin(type_)).startswith("typing.") \
                    and not str(type_).startswith("typing."):
                raise FuncSignatureError(
                    "Function signature parameters must be a valid type!"
                )

    def __contains__(self, item):
        """
        Returns True if the item is in the signature.

        If item is a string, it will be checked against
        the parameter names list.

        If item is a parameter, it will be checked against
        the parameter list.

        :param item: the item to check
        :return: True if the item is in the signature
        """
        if isinstance(item, str):
            return item in self.parameters.items()

        if isinstance(item, Parameter):
            return item in self.parameters.items()

        return False

    def __len__(self):
        """
        Returns the number of parameters inspect the signature.

        :return: the number of parameters inspect the signature
        """
        return len(self.parameters)

    @property
    def length(self) -> int:
        """
        Returns the signature length.

        :return: the signature length
        """
        return len(self.parameters)

    @property
    def names(self) -> list[str]:
        """
        Returns a surface copy list of all parameter names.

        :return: a surface copy list of all parameter names
        """
        return list(self.parameters.keys())

    @property
    def params(self) -> list[Parameter]:
        """
        Returns a surface copy list of all parameters.

        :return: a surface copy list of all parameters
        """
        return list(self.parameters.values())

    @property
    def types(self) -> list[type]:
        """
        Returns a surface copy list of all types.

        :return: a surface copy list of all types
        """
        return [par.annotation for par in self.parameters.values()]

    @property
    def all(self) -> dict[str, Parameter]:
        """
        Returns the parameters as a dict.

        :return: the parameters as a dict
        """
        return dict(self.parameters)

    @property
    def has_var_args(self) -> bool:
        """
        Returns True if the signature includes a '*args' parameter.

        :return: True if the signature includes a '*args' parameter
        """
        has_args = False

        for param in self.parameters.values():
            if param.kind == Parameter.VAR_POSITIONAL:
                has_args = True
                break

        return has_args

    @property
    def has_var_kwargs(self) -> bool:
        """
        Returns True if the signature includes a '*kwargs' parameter.

        :return: True if the signature includes a '*kwargs' parameter
        """
        has_kwargs = False

        for param in self.parameters.values():
            if param.kind == Parameter.VAR_KEYWORD:
                has_kwargs = True
                break

        return has_kwargs

    @property
    def expected_arg_count(self) -> int:
        """
        Returns the number of required arguments.

        If a parameter is either '*args', '**kwargs',
        has the 'KEYWORD_ONLY' kind or has a default
        value then the count is reduced by 1.

        :return: the number of required arguments
        """
        num_args = 0

        for param in self.parameters.values():
            if param.kind == param.VAR_POSITIONAL \
                    or param.kind == param.VAR_KEYWORD \
                    or param.kind == param.KEYWORD_ONLY \
                    or param.default != param.empty:
                break

            num_args += 1

        return num_args

    def get_param(self, name: str):
        """
        Returns the parameter matching the specified name.

        :param name: the key to match
        :return: the parameter matching the specified name
        """
        return self.parameters[name]

    def get_param_type(self, name: str) -> type:
        """
        Returns the type of the parameter matching the specified name.

        :param name: the key to match
        :return: the type of the parameter matching the specified name
        """
        return self.parameters[name].annotation

    def get_param_default(self, name: str) -> typing.Any:
        """
        Returns the default value of the parameter matching the
        specified name.

        :param name: the key to match
        :return: the default value of the parameter matching the
            specified name
        """
        return self.parameters[name].default

    def get_param_kind(self, name: str) -> typing.Any:
        """
        Returns the kind of the parameter matching the specified name.

        There are five kinds:
            - POSITIONAL_ONLY - args before a '/' in the list
            - KEYWORD_ONLY - args after a '*' in the list
            - POSITIONAL_OR_KEYWORD - any normal arg or kwarg
            - VAR_POSITIONAL - any *args
            - VAR_KEYWORD - any **kwargs

        More info can be found here:
        https://www.educative.io/edpresso/what-are-positional-only-arguments-in-python

        :param name: the key to match
        :return: the parameter kind matching the specified name
        """
        return self.parameters[name].kind

    def _check_args_length(self, *args, **kwargs):
        actual_arg_count = len(args)
        actual_kwarg_count = len(kwargs)

        is_valid = True

        if not self.expected_arg_count == actual_arg_count \
                and self.expected_arg_count <= actual_kwarg_count:
            has_positional_only = False

            for param in self.parameters.values():
                if param.kind == Parameter.POSITIONAL_ONLY:
                    has_positional_only = True
                    break

            if has_positional_only:
                is_valid = False

        if not is_valid:
            _length = len(self.parameters)

            if _length == 1:
                arg_error_text = "'args' must have at least 1 argument:"
            else:
                arg_error_text = "'args' must have at least " \
                                 f"{_length} arguments:"

            if actual_arg_count == 1 and actual_kwarg_count == 1:
                arg_text = "and instead has " \
                           "1 argument " \
                           "and has 1 kwarg."
            elif actual_arg_count == 1 and actual_kwarg_count > 1:
                arg_text = "and instead has " \
                           "1 argument " \
                           f"and has {actual_kwarg_count} kwargs."
            elif actual_arg_count == 1 and actual_kwarg_count > 1:
                arg_text = "and instead has " \
                           f"{actual_arg_count} arguments " \
                           "and has 1 kwarg."
            else:
                arg_text = "and instead has " \
                           f"{actual_arg_count} arguments " \
                           f"and has {actual_kwarg_count} kwargs."

            raise FuncArgsMismatchError(f"{arg_error_text} ({self}) {arg_text}")

    def _check_arg(self, name, arg):
        arg_error_text = "Signature Mismatch " \
                         f"({self}) " \
                         f"[Parameter '{name}']: "

        param = self.parameters.get(name)

        # Verify that the kwarg name exists in the signature
        if param is not None:
            p_type = param.annotation

            # If the param type/kwarg is a class then the base
            # name needs to be retrieved otherwise it's probably
            # an object from the typing module or a generic
            p_type_name = Signature._parse_name_for_error(p_type)
            a_type_name = Signature._parse_name_for_error(type(arg))

            # Verify the kwarg is the right type
            kwargs_valid = self._validate_type(arg, p_type)

            if not kwargs_valid:
                raise FuncArgsMismatchError(arg_error_text +
                                            f"\n>>> Expected: '{p_type_name}',"
                                            f" Found: '{a_type_name}'"
                                            f" with value '{arg}'")

    def verify_args(self, *args, **kwargs):
        """
        Verifies that the supplied args and kwargs match the signature.

        :param args: the args to check
        :param kwargs: the kwargs to check
        :return: True of the args and kwargs match the signature
        """
        self._check_args_length(*args, **kwargs)

        for name, arg in zip(list(self.parameters.keys()), args):
            self._check_arg(name, arg)

        for name, kwarg in kwargs.items():
            self._check_arg(name, kwarg)
