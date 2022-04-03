# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# signature.py
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
Contains the Signature class, a data object that represents
a function parameter signature.
"""
from __future__ import annotations

import inspect
import typing
from inspect import Parameter

from pystdlib.condition import Condition
from pystdlib.introspection.exceptions import FuncSignatureError, FuncArgsMismatchError
from pystdlib.types import is_instance, is_subclass, get_type_from_name


class Signature(inspect.Signature):
    """Represents a function parameter signature."""

    @staticmethod
    def _format_annotation(annotation, base_module=None):
        if getattr(annotation, "__module__", None) == "typing":
            return repr(annotation).replace("typing.", "")
        if isinstance(annotation, type):
            if annotation.__module__ in ("builtins", base_module):
                return annotation.__qualname__
            return annotation.__module__ + "." + annotation.__qualname__
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
        if type_ == inspect.Parameter.empty:
            return True

        return is_instance(value, type_) or is_subclass(type(value), type_)

    def __init__(
        self,
        _func=None,
        *,
        _signature: inspect.Signature | Signature = None,
        _return_type=None,
        _make_keyword_only: bool = False,
        **kwargs: type | Parameter,
    ):
        """
        Initializes the Signature object.

        NOTE: all parameter names start with an '_' to prevent the
        signature names from clashing if the signature needs to
        use the same names.

        NOTE: if "_func" is not None then all other arguments are
        ignored.

        :param _func: the function to retrieve the signature of,
            if None then "_signature" and "__return_type" are used
            instead
        :param _signature: if "_func" is None then this is used to
            create the signature instead. This must be of type
            inspect.Signature or an instance of this class.
        :param _return_type: if "_func" is None, sets the return type
        :param _make_keyword_only: if True then all custom parameters
            will be set as "KEYWORD_ONLY" instead of the default
            "POSITIONAL_OR_KEYWORD"
        :param kwargs: if "_func" is None, the keyword signature to
            set, the name is the name of the parameter and the value
            is the type hint. You can also specify inspect.Parameter
            instances instead of the type hint.
        """
        if _func is not None:
            sig = inspect.signature(_func, follow_wrapped=True)

            _new_signature = list(sig.parameters.values())
            _new_return_annotation = sig.return_annotation
        elif _signature is not None and isinstance(
            _signature, (inspect.Signature, Signature)
        ):
            _new_signature = list(_signature.parameters.values())
            _new_return_annotation = _signature.return_annotation
        else:
            valid = True
            for value in kwargs.values():
                if (
                    not isinstance(value, Parameter)
                    and not isinstance(value, type)
                    and "typing." not in str(value)
                ):
                    valid = False
                    break

            if valid:
                _new_signature: list[Parameter] = []
                for name, value in kwargs.items():
                    if isinstance(value, Parameter):
                        _new_parameter = value
                    else:
                        kind = (
                            Parameter.KEYWORD_ONLY
                            if _make_keyword_only
                            else Parameter.POSITIONAL_OR_KEYWORD
                        )

                        _new_parameter = Parameter(name, kind, annotation=value)

                    _new_signature.append(_new_parameter)
            else:
                raise FuncSignatureError(
                    "'kwargs' has the wrong value types! They must be"
                    " any combination of 'typing.Parameter',"
                    " 'type' or any type hint from the 'typing'"
                    " module."
                )

            _new_return_annotation = _return_type

        # Check if any of the type annotations are a string and
        # replace them with their respective types
        values = list(_new_signature)
        for index, param in enumerate(values):
            if isinstance(param.annotation, str):
                name = param.name
                annotation = get_type_from_name(param.annotation)
                kind = param.kind
                default = param.default
                values[index] = Parameter(
                    name, kind, default=default, annotation=annotation
                )

        _new_signature = values

        # Check if the return annotation is a string and
        # replace it with its respective types
        if isinstance(_new_return_annotation, str):
            _new_return_annotation = get_type_from_name(_new_return_annotation)

        super().__init__(
            _new_signature,
            return_annotation=_new_return_annotation,
            __validate_parameters__=False,
        )

        types: list[type] = [par.annotation for par in list(self.parameters.values())]

        func_error = "Function signature parameters cannot be of type '%s'!"

        # Check for 'NoReturn' type
        if typing.NoReturn in types:
            raise FuncSignatureError(func_error % "typing.NoReturn")

        # Check for 'Final' type
        # This has to check by string because
        # Final might be parameterized
        if any("typing.Final" in str(type_) for type_ in types):
            raise FuncSignatureError(func_error % "typing.Final")

        for type_ in types:
            # Check if the type is actually a type, a type hint or Parameter.empty
            valid = Condition(
                type_ is Parameter.empty,
                type_ is None,
                type == type_.__class__,
                str(typing.get_origin(type_)).startswith("typing."),
                str(type_).startswith("typing."),
                use_or=True,
            )

            if not valid:
                raise FuncSignatureError(
                    f"Function signature parameters must be a valid type! Provided Type: {type_}"
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
    def has_return_annotation(self) -> bool:
        """
        Returns whether the signature's return annotation is
        not :attr:`Signature.empty`.

        :return: True if the signature has a return annotation
        """
        return self.return_annotation is not Signature.empty

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
            if (
                param.kind == param.VAR_POSITIONAL
                or param.kind == param.VAR_KEYWORD
                or param.kind == param.KEYWORD_ONLY
                or param.default != param.empty
            ):
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
        specified name. If the parameter has no annotation then
        this attribute is set to 'Parameter.empty'.

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
        and
        https://docs.python.org/3/library/inspect.html#inspect.Parameter.kind

        :param name: the key to match
        :return: the parameter kind matching the specified name
        """
        return self.parameters[name].kind

    def _check_args_length(self, *args, **kwargs):
        actual_arg_count = len(args)
        actual_kwarg_count = len(kwargs)

        is_valid = True

        if (
            not self.expected_arg_count == actual_arg_count
            and self.expected_arg_count <= actual_kwarg_count
        ):
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
                arg_error_text = f"'args' must have at least {_length} arguments:"

            if actual_arg_count == 1 and actual_kwarg_count == 1:
                arg_text = "and instead has 1 argument and has 1 kwarg."
            elif actual_arg_count == 1 and actual_kwarg_count > 1:
                arg_text = (
                    "and instead has "
                    "1 argument "
                    f"and has {actual_kwarg_count} kwargs."
                )
            elif actual_arg_count > 1 and actual_kwarg_count == 1:
                arg_text = (
                    "and instead has "
                    f"{actual_arg_count} arguments "
                    "and has 1 kwarg."
                )
            else:
                arg_text = (
                    "and instead has "
                    f"{actual_arg_count} arguments "
                    f"and has {actual_kwarg_count} kwargs."
                )

            raise FuncArgsMismatchError(f"{arg_error_text} ({self}) {arg_text}")

    def _check_arg(self, name, arg):
        arg_error_text = f"Signature Mismatch ({self}) [Parameter '{name}']: "

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
                raise FuncArgsMismatchError(
                    arg_error_text + f"\n>>> Expected: '{p_type_name}',"
                    f" Found: '{a_type_name}'"
                    f" with value '{arg}'"
                )

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
