# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# types.py
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
Contains some general type classes that can be inherited from
and some basic typing utils.
"""
from __future__ import annotations

import builtins
import inspect
import typing
from collections import (
    deque, defaultdict, OrderedDict, UserDict, ChainMap, Counter, UserList
)

from inspect import Parameter

from introspection.typing import (
    get_generic_base_class, is_generic_base_class, is_parameterized_generic
)


class Final(type):
    """
    A metaclass that can be assigned to a class to completely prevent
    that class from being subclassed.

    >>> class NewClass(metaclass=Final)
    """

    # noinspection PyMethodParameters,SpellCheckingInspection
    def __new__(cls, name, bases, classdict):
        for base in bases:
            if isinstance(base, Final):
                raise TypeError(f"type '{base.__name__}' "
                                "is not an acceptable base type")
        return type.__new__(cls, name, bases, dict(classdict))


NoneType = type(None)


def _get_subtypes(cls):
    subtypes = cls.__args__

    if get_generic_base_class(cls) is typing.Callable \
            and len(subtypes) != 2 or subtypes[0] is not ...:
        subtypes = (subtypes[:-1], subtypes[-1])

    return subtypes


def _is_callable(value, type_):
    if not callable(value):
        return False

    if is_generic_base_class(type_):
        return True

    param_types, ret_type = _get_subtypes(type_)
    sig = inspect.signature(value)

    missing_annotations = []

    if param_types is not ...:
        if len(param_types) != len(sig.parameters):
            return False

        # TODO: add support for TypeVars

        # If any of the existing annotations don't match the type, we'll return False.
        # Then, if any annotations are missing, we'll throw an exception.
        for param, expected_type in zip(sig.parameters.values(), param_types):
            param_type = param.annotation
            if param_type is Parameter.empty:
                missing_annotations.append(param)
                continue

            if not is_subclass(param_type, expected_type):
                return False

    if sig.return_annotation is Parameter.empty:
        missing_annotations.append('return')
    else:
        if not is_subclass(sig.return_annotation, ret_type):
            return False

    if missing_annotations:
        raise ValueError(f"Missing annotations: {missing_annotations}")

    return True


def _is_origin_type(base, value, type_):
    iterables = [
        typing.Container, typing.Collection, typing.AbstractSet,
        typing.MutableSet, typing.Sequence, typing.MutableSequence,
        typing.ByteString, typing.Deque, typing.List, typing.Set,
        typing.FrozenSet, typing.KeysView, typing.ValuesView,
        typing.AsyncIterable, set, list, deque, UserList
    ]

    mappings = [
        typing.Mapping, typing.MutableMapping, typing.MappingView,
        typing.Dict, typing.DefaultDict, typing.Counter, typing.ChainMap,
        dict, defaultdict, OrderedDict, UserDict, ChainMap, Counter
    ]

    if base in iterables:
        type_args = _get_subtypes(type_)

        if len(type_args) != 1:
            raise TypeError("Generic iterables must have "
                            f"exactly 1 type argument; found {type_args}")

        type_ = type_args[0]
        return all(is_instance(val, type_) for val in value)

    if base in mappings or base is typing.ItemsView:
        view = value

        if base is not typing.ItemsView:
            view = value.items()

        type_args = _get_subtypes(type_)
        if len(type_args) != 2:
            raise TypeError("Generic mappings must have "
                            f"exactly 2 type arguments; found {type_args}")

        key_type, value_type = type_args
        return all(is_instance(key, key_type)
                   and is_instance(val, value_type)
                   for key, val in view)

    if base in (typing.Tuple, tuple):
        type_args = _get_subtypes(type_)
        if len(value) != len(type_args):
            return False

        return all(is_instance(val, type_)
                   for val, type_ in zip(value, type_args))

    raise NotImplementedError(f"Cannot perform isinstance check for type {type_}")


def _is_special_instance(base, value, type_):
    if base in (typing.Union, typing.Optional):
        types = _get_subtypes(type_)
        return any(is_instance(value, typ) for typ in types)

    if base == typing.Callable:
        return _is_callable(value, type_)

    if base == typing.Type:
        # if it's not a class, return False
        if not isinstance(value, type):
            return False

        if is_generic_base_class(type_):
            return True

        type_args = _get_subtypes(type_)
        if len(type_args) != 1:
            raise TypeError("Type must have exactly 1 type"
                            f" argument; found {type_args}")

        # noinspection PyTypeChecker
        return is_subclass(value, type_args[0])

    if base is typing.Any:
        return True

    return False


def to_python_type(annotation):
    """
    Given a type annotation or a class as input, returns the
    corresponding python class.

    Examples:

    >>> to_python_type(typing.Dict)
    <class 'dict'>
    >>> to_python_type(dict[int, int])
    <class 'dict'>
    >>> to_python_type(typing.List[int])
    <class 'list'>
    >>> to_python_type(int)
    <class 'int'>

    :param annotation: the annotation to check
    :return: the corresponding python class
    """
    mro = getattr(annotation, "mro", None)

    if mro is not None and callable(mro):
        mro = annotation.mro()
    else:
        # if it doesn't have a mro method,
        # it must be a weird typing object
        return annotation.__origin__

    if typing.Type in mro:
        return annotation.python_type

    if annotation.__module__ == 'typing':
        return annotation.__origin__

    if '[' in str(annotation) and ']' in str(annotation):
        return get_type_from_name(annotation.__name__)

    return annotation


def get_type_from_name(name: str) -> type | None:
    """
    Returns the type matching the specified name
    or None if not found.

    :param name: the name of the type to lookup
    :return: the type matching the specified name
        or None if annotations found
    """
    try:
        return getattr(builtins, name)
    except AttributeError:
        try:
            obj = globals()[name]
        except KeyError:
            return None

        return obj if isinstance(obj, type) else None


# noinspection PyProtectedMember,PyUnresolvedReferences
def is_generic(cls):
    """
    Detects any kind of generic, for example `List` or `List[int]`.
    This includes "special" types like
    Union and Tuple - anything that's subscriptable, basically.

    :param cls: the class to check
    :return: True if the class is any kind of generic
    """
    if isinstance(cls, typing._GenericAlias):
        return True

    if isinstance(cls, typing._SpecialForm):
        return cls is not typing.Any

    return False


def is_instance_namedtuple(obj) -> bool:
    """
    Checks if the object is an instance of 'namedtuple'.

    :param obj: the object to check
    :return: True if the object is an instance of 'namedtuple'
    """
    return (
            isinstance(obj, tuple) and
            hasattr(obj, '_asdict') and
            hasattr(obj, '_fields')
    )


def is_instance(obj, type_):
    """
    Return whether an object is an instance of a class or of a subclass thereof.

    This function fully supports type checking with the typing module and
    fully supports generics.

    :param obj: the object to check
    :param type_: the expected type of the object
    :return: True if the type matches
    """
    if type_.__module__ == 'typing':
        base_generic = get_generic_base_class(type_) \
            if is_parameterized_generic(type_) else type_

        result = _is_special_instance(base_generic, obj, type_)
        if result:
            return True

    if is_generic_base_class(type_):
        try:
            return isinstance(obj, type_.__origin__)
        except AttributeError:
            return isinstance(obj, type_)

    if is_parameterized_generic(type_):
        if not isinstance(obj, type_.__origin__):
            return False

        base = get_generic_base_class(type_)

        return _is_origin_type(base, obj, type_)

    return isinstance(obj, type_)


def is_subclass(sub_type, super_type):
    """
    Return whether 'cls' is a derived from another class or is the same class.

    This function fully supports type checking with the typing module and
    fully supports generics.

    :param sub_type: the subtype to check
    :param super_type: the expected supertype of the object
    :return: True if the type_ matches
    """
    # Skip if types are equal
    if sub_type is super_type:
        return True

    if not is_generic(sub_type):
        python_super = to_python_type(super_type)
        return issubclass(sub_type, python_super)

    # At this point we know `sub_type` is a generic
    python_sub = to_python_type(sub_type)
    python_super = to_python_type(super_type)
    if not issubclass(python_sub, python_super):
        return False

    # At this point we know that `sub_type`'s base type is a subtype of \
    # `super_type`'s base type.
    # If `super_type` isn't qualified, then there's nothing more to do.
    if not is_generic(super_type) \
            or is_generic_base_class(super_type):
        return True

    # At this point we know that `super_type` is a qualified generic... \
    # so if `sub_type` isn't qualified, it can't be a subtype.
    if is_generic_base_class(sub_type):
        return False

    # at this point we know that both types are qualified generics, \
    # so we just have to compare their subtypes.
    sub_args = _get_subtypes(sub_type)
    super_args = _get_subtypes(super_type)
    return all(is_subclass(sub_arg, super_arg)
               for sub_arg, super_arg
               in zip(sub_args, super_args))
