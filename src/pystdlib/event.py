# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# event.py
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
Contains the Event class and the classes that support it.

The event class is a heavily modified version of 'pymitter'
written by 'Marcel R.' which was originally distributed
under the 'BSD 3-Clause "New" or "Revised" License' and
can be found here: (https://github.com/riga/pymitter).
"""
from __future__ import annotations

import inspect
import logging
from datetime import datetime
from typing import (Iterator, NoReturn, Callable, Optional)

from pystdlib import Chars
from pystdlib.func_utils import FuncInfo, Signature
from pystdlib.logged import Logged
from pystdlib.str_utils import is_blank, is_not_blank
from pystdlib.types import is_subclass
from pystdlib.values import StringValue


class Namespace:
    """
    Represents an event namespace that when iterated over
    gives you the individual parts split by the specified
    delimiter which defaults to "." if not specified.
    """

    _CB_KEY = "__callbacks"
    _NO_NAME = "_NO_NAME"

    def __init__(self, name: str | StringValue, delimiter: str = "."):
        """
        Initializes the Namespace object.

        :param name: the name of the namespace
        :param delimiter: the character that should be used to split
            the name into parts
        """
        if isinstance(name, StringValue):
            self._name = self._NO_NAME if is_blank(name.get()) else name.get()
        elif isinstance(name, str):
            self._name = self._NO_NAME if is_blank(name) else name
        else:
            if isinstance(name, StringValue):
                raise ValueError(f"'event' type is invalid! ({type(name.get())})")
            else:
                raise ValueError(f"'event' type is invalid! ({type(name)})")

        # Split the namespace into it's individual parts
        # Convert to string is done to get value if
        # event is StringValue instead of str
        self._parts = self._name.split(delimiter)

        # Check if '__callbacks' is in event namespace
        if self._CB_KEY in self._parts:
            raise ValueError(f"'{self._CB_KEY}' is not valid for an "
                             "event or namespace level name!")

    def __iter__(self) -> Iterator[str]:
        """
        Returns an iterator of the parts of this namespace.

        :return: an iterator of the parts of this namespace
        """
        return iter(self._parts)

    def __str__(self):
        """
        Returns the namespace name.

        :return: the namespace name
        """
        return self._name

    def __repr__(self):
        """
        Returns a code representation of this namespace.

        :return: a code representation of this namespace
        """
        return f"Namespace(\"{self._name}\")"

    def __eq__(self, other):
        """
        Returns True if 'other' equals this namespace.

        :param other: the object to check
        :return: True if 'other' equals this namespace
        """
        return self._name == other.name

    @property
    def name(self):
        """
        Returns the name of the namespace.

        :return: the name of the namespace
        """
        return self._name


# class Signature():
#     """Represents a function parameter signature."""
#
#     _type_origins = ("Any", "Final", "Literal", "Optional", "Union")
#
#     _type_hints = ("Hashable", "Awaitable", "Coroutine",
#                    "AsyncIterable", "AsyncIterator", "Iterable",
#                    "Iterator", "Reversible", "Sized", "Container",
#                    "Collection", "Callable", "AbstractSet",
#                    "MutableSet", "Mapping", "MutableMapping",
#                    "Sequence", "MutableSequence", "ByteString",
#                    "Tuple", "List", "Deque", "Set", "FrozenSet",
#                    "MappingView", "KeysView", "ItemsView",
#                    "ValuesView", "ContextManager",
#                    "AsyncContextManager",
#                    "Dict", "DefaultDict", "OrderedDict",
#                    "Counter", "ChainMap", "Generator",
#                    "AsyncGenerator", "Type")
#
#     def __init__(self, **kwargs: type):
#         """
#         Initializes the Signature object.
#
#         :param kwargs: the keyword signature to set
#         """
#         self._signature = kwargs
#
#         self._length: int = len(self._signature)
#         self._names: list[str] = list(self._signature.keys())
#         self._types: list[type] = list(self._signature.values())
#
#         func_error = "Event signature parameters cannot be of type '%s'!"
#
#         # noinspection PyTypeChecker
#         if self._types.count(None) > 0:
#             raise EventSignatureError(func_error % "None")
#
#         from typing import NoReturn
#         if self._types.count(NoReturn) > 0:
#             raise EventSignatureError(func_error % "typing.NoReturn")
#
#         from typing import ClassVar
#         # noinspection PyTypeChecker
#         if self._types.count(ClassVar) > 0:
#             raise EventSignatureError(func_error % "typing.ClassVar")
#
#         from typing import get_origin
#         for value in self._types:
#             if value.__class__ != type \
#                     and str(get_origin(value)).lstrip("typing.") not in self._type_origins \
#                     and str(value).lstrip("typing.") not in self._type_hints:
#                 raise EventSignatureError(
#                     "Event signature parameters must be a valid type!"
#                 )
#
#     def __contains__(self, item):
#         """
#         Returns True if the item is in the signature.
#
#         :param item: the item to check
#         :return: True if the item is in the signature
#         """
#         return item in self._signature
#
#     def __str__(self):
#         """
#         Returns a string representation of the signature.
#
#         :return: a string representation of the signature
#         """
#         if self._length == 0:
#             return "NONE"
#
#         return ", ".join(k + "=" + v.__name__
#                          if str(v).startswith("<class")
#                          else k + "=" + str(v)
#                          for k, v in self._signature.items())
#
#     def __repr__(self):
#         """
#         Returns a code representation of this signature.
#
#         :return: a code representation of this signature
#         """
#         return f"Signature({self})"
#
#     def __eq__(self, other):
#         """
#         Returns True if 'other' equals this signature.
#
#         :param other: the object to check
#         :return: True if 'other' equals this signature
#         """
#         if isinstance(other, Signature):
#             return self._names == other._names and self._types == other._types
#
#         return False
#
#     @property
#     def length(self) -> int:
#         """
#         Returns the signature length.
#
#         :return: the signature length
#         """
#         return self._length
#
#     @property
#     def names(self) -> list[str]:
#         """
#         Returns a surface copy list of all parameter names.
#
#         :return: a surface copy list of all parameter names
#         """
#         return list(self._names)
#
#     @property
#     def types(self) -> list[type]:
#         """
#         Returns a surface copy list of all parameter types.
#
#         :return: a surface copy list of all parameter types
#         """
#         return list(self._types)
#
#     def get_type(self, key) -> type:
#         """
#         Returns the type matching the specified key.
#
#         :param key: the key to match
#         :return: the type matching the specified key
#         """
#         return self._signature[key]
#
#     def verify_kwargs(self, **kwargs):
#         """
#         Verifies if the specified kwargs matches the signature.
#
#         :param kwargs: the kwargs to verify
#         :raises EventFireMismatchError: if the kwargs doesn't match
#         """
#         self._check_length(kwargs, "'kwargs'", "argument", EventFireMismatchError)
#
#         for key, value in kwargs.items():
#             arg_error_text = "Signature Mismatch " \
#                              f"({self}) " \
#                              f"[Parameter '{key}']: "
#
#             # Checks if the parameter is in the signature
#             if key in self._signature:
#                 p_value = self._signature[key]
#
#                 # Converts the name for error messages
#                 if str(p_value).startswith("<class"):
#                     p_value_name = p_value.__name__
#                 else:
#                     p_value_name = str(p_value)
#
#                 # Checks if the parameter type is one of the built-in type hints
#                 if str(get_origin(p_value)) in (
#                         'typing.Union', 'typing.Optional', 'typing.Final'
#                 ):
#                     params = get_args(p_value)
#                     # if it is a type hint, expands the hint parameters
#                     # and checks parameter type against them
#                     if type(value) not in params:
#                         raise EventFireMismatchError(arg_error_text +
#                                                      f"Type should be '{p_value_name}'")
#                 # Checks if the parameter type is the Literal type hint
#                 elif str(get_origin(p_value)) == "typing.Literal":
#                     params = get_args(p_value)
#                     # if it is a Literal, expands the Literal literals
#                     # and checks value against them
#                     if value not in params:
#                         raise EventFireMismatchError(arg_error_text +
#                                                      f"Literal should be one of '{params}'")
#                 elif p_value == Callable:
#                     if not callable(value):
#                         raise EventFireMismatchError(arg_error_text +
#                                                      f"Type should be 'typing.Callable'")
#
#                 # Checks if the parameter type is the Any type hint,
#                 # otherwise checks if type matches the actual signature type
#                 elif p_value != Any and type(value) is not p_value:
#                     raise EventFireMismatchError(arg_error_text +
#                                                  f"Type should be '{p_value_name}'")
#             else:
#                 raise EventFireMismatchError(arg_error_text + "Not Found")


class _Handler:
    """
    A simple event handler class that wraps a function *func* for a
    specific *event* and that keeps track of the times left to handle.
    """

    def __init__(self, func: Callable,
                 namespace: Optional[Namespace],
                 ttl: int):
        self._name = func.__name__
        self._func = func
        self._namespace = namespace
        self._ttl = ttl

        # store the registration time
        self.time = datetime.now()

    def __repr__(self):
        """
        Returns a code representation of this handler.

        :return: a code representation of this handler
        """
        return f"Handler({self._func},{self._namespace},{self._ttl})"

    @property
    def name(self) -> str:
        """
        Returns the assigned function's name.

        :return: the assigned function's name
        """
        return self._name

    @property
    def func(self) -> Callable:
        """
        Returns the assigned function.

        :return: the assigned function
        """
        return self._func

    @property
    def namespace(self) -> Namespace:
        """
        Returns the event namespace.

        :return: the event namespace
        """
        return self._namespace

    @property
    def ttl(self) -> int:
        """
        Returns the Times To Listen (TTL) value.

        :return: the Times To Listen (TTL) value
        """
        return self._ttl

    def handle(self, *args, **kwargs) -> int:
        """
        Invokes the wrapped function when ttl is non-zero, decreases
        the ttl value when positive and returns whether it reached
        zero or not.

        :return: True if ttl value is zero
        """
        if self._ttl != 0:
            self._func(*args, **kwargs)

        if self._ttl > 0:
            self._ttl -= 1

        return self._ttl == 0


class Branch(Logged):
    """Represents an event hierarchy branch."""

    _CB_KEY = "__callbacks"
    _WC_CHAR = "*"

    def __init__(self, name: str):
        """
        Initializes the Branch object.

        :param name: the name of the branch
        """
        self._name = name
        self._root: dict = self._new_branch()
        self._handlers: list[_Handler] = self._root[self._CB_KEY]

        self.set_log_level(logging.DEBUG)

        self._debug(f"New Branch Created: {name}")

    def __repr__(self):
        """
        Returns a code representation of this branch.

        :return: a code representation of this branch
        """
        return f"Branch(\"{self._name}\")"

    @classmethod
    def _new_branch(cls) -> dict:
        """
        Returns a new branch. Essentially, a branch is just a
        dictionary with a special item *CB_KEY* that holds
        registered functions. All other items are used to
        build a tree structure.

        :return: a new empty branch
        """
        return {cls._CB_KEY: []}

    def get_handlers(self) -> list[_Handler]:
        """
        Returns a surface copy list of all root handlers.

        :return: a surface copy list of all root handlers
        """
        return list(self._handlers)

    def add_handler(self, handler: _Handler) -> Branch:
        """
        Adds the specified handler to the root list.

        :param handler: the handler to add
        :return: this instance for use in method chaining
        """
        self._handlers.append(handler)
        return self

    def remove_handler(self, handler: Callable) -> NoReturn:
        """
        Removes a handler given by its function *func*.

        :param handler: the function to remove as handler
        """
        indexes = [index for index, hdr in enumerate(self._handlers) if hdr.func == handler]

        for i in indexes[::-1]:
            self._handlers.pop(i)

    def get_branches(self) -> list[Branch]:
        """
        Returns a surface copy list of all sub-branches.

        :return: a surface copy list of all sub-branches
        """
        branches: list[Branch] = []

        for item in self._root.values():
            if not isinstance(item, list):
                branches.append(item)

        return branches

    def get_branch(self, name: str) -> Branch:
        """
        Returns the branch matching the specified name.

        :param name: the name of the branch
        :return: the branch matching the specified name
        """
        return self._root[name]

    def add_branch(self, name: str) -> Branch:
        """
        Adds a new sub-branch to this branch.

        :param name: the name of the branch
        :return: this instance for use in method chaining
        """
        if name not in self._root:
            self._root[name] = Branch(name)
        return self

    def find_branch(self, namespace: Namespace) \
            -> Optional[Branch]:
        """
        Returns a branch of the tree structure that matches *namespace*.
        Wildcards are not applied.

        :param namespace: the namespace to search
        :return: a branch of the tree structure that matches *namespace*
        """
        branch: Branch = self

        if is_not_blank(namespace.name):
            for part in namespace:
                branch = branch.get_branch(part)

        return branch

    def get_namespace_branches(self, namespace: Namespace,
                               wildcard: bool = False) \
            -> list[Branch]:
        """
        Returns a list of all branches that match the namespace parts
        and if wildcard is True then any wildcard branches are
        returned as well.

        :param namespace: the namespace to match
        :param wildcard: if True then any wildcard branches are
            returned as well
        :return: a list of the matching branches
        """
        branches = [self]

        if is_not_blank(namespace.name):
            # Search through namespace parts and if they match branches
            # then add them to the list and if part is wildcard
            # and wildcard is enabled then add them too
            for part in namespace:
                _branches = []
                for branch in branches:
                    for name, sub_branch in branch.root.items():
                        if name == self._CB_KEY:
                            continue
                        if name == part:
                            _branches.append(sub_branch)
                        elif wildcard and self._WC_CHAR in (part, name):
                            _branches.append(sub_branch)
                branches = _branches

        return branches

    def expand_namespace(self, namespace: Namespace) \
            -> Optional[Branch]:
        """
        Loop through each part of namespace and create new branch
        for each part if it doesn't exist.

        :param namespace: the namespace to expand
        :return: the lowest branch in the namespace
        """
        branch = self

        if is_not_blank(namespace.name):
            for part in namespace:
                branch.add_branch(part)
                branch = branch.get_branch(part)

        return branch

    @property
    def root(self) -> dict:
        """
        Returns the root.

        :return: the root
        """
        return self._root


class Event(Logged):
    """
    An event is an object that, when fired, calls any added handler
    functions and passes them arguments.

    The user can specify an event signature upon inizializazion,
    defined by kwargs in the form of argumentname=class (e.g. num=int).
    The arguments' types are checked and verified when a handler is added
    and when the event is fired. Callables with a matching signature can
    be added with '+=' or removed with '-='. All handlers can be notified
    by calling 'Event.fire' with correct arguments.

    >>> event = Event(num=int, data=dict)
    >>> event += lambda num, data: print(f"{num} {data}")
    >>> event.fire(num=5, data={"foo": "bar"})
    5 {'foo': 'bar'}

    >>> event = Event(num=int)
    >>> event += lambda wrong_name: None
    Traceback (most recent call last):
        ...
    EventHandlerMismatchError: Signature Mismatch
    (num=int) [Parameter #1 'wrong_name']: Name should be 'num'.

    >>> event = Event(num=int)
    >>> event += lambda num: None
    >>> event.fire(wrong_name=0)
    Traceback (most recent call last):
        ...
    EventFireMismatchError: Signature Mismatch
    (num=int) [Parameter 'wrong_name']: Not Found
    """

    _NEW_HANDLER = Namespace("new_handler")
    _NO_NAME = "_NO_NAME"

    def __init__(self, _wildcard: bool = False,
                 _new_handler: bool = False,
                 _max_handlers: int = -1,
                 _delimiter: str = Chars.DOT,
                 _signature: dict[str, type] | Signature = None,
                 _make_keyword_only: bool = False,
                 **kwargs: type):
        """
        Initializes the Event object.

        NOTE: all parameter names start with an '_' to prevent the
        signature names from clashing if the signature needs to
        use the same names.

        NOTE: the '_signature' and 'kwargs' can be used either or
        together, either way the result of both will be combined
        with the '_signature' values being added before the 'kwargs'
        values. This allows for a predefined Signature object to be
        extended if needed.

        :param _wildcard: if True wildcards in event names are taken
            into account
        :param _new_handler: if True, a 'new_handler' event is
            emitted every time a new handler is registered with
            arguments '(handler, event=None)'
        :param _max_handlers: the maximum number of event handlers.
            A negative number means that this number is unlimited.
        :param _delimiter: the character to separate each part of
            namespaces
        :param _signature: the parameter signature that all handlers
            are required to match and the signature that will be
            required to use when the event is fired.
        :param kwargs: the parameter signature that all handlers
            are required to match and the signature that will be
            required to use when the event is fired.
        """
        self._wildcard = _wildcard
        self._delimiter = _delimiter
        self._new_handler = _new_handler
        self._max_handlers = _max_handlers

        if _signature is None:
            self._signature = Signature(_make_keyword_only=_make_keyword_only, **kwargs)
        elif isinstance(_signature, dict):
            self._signature = Signature(_make_keyword_only=_make_keyword_only, **{**_signature, **kwargs})
        elif isinstance(_signature, Signature):
            self._signature = _signature
        else:
            raise ValueError(f"'signature' type is invalid! ({type(_signature)})")

        self._new_handler_signature = Signature(_func=Callable, evt=str)

        self._root = Branch("ROOT")

    def __str__(self):
        """
        Returns a string representation of the signature.

        :return: a string representation of the signature
        """
        return self._signature.__str__()

    def __repr__(self):
        """
        Returns a code representation of this event.

        :return: a code representation of this event
        """
        value = "Signature("

        if self._wildcard:
            value += f"_wildcard={self._wildcard}, "

        if self._new_handler:
            value += f"_new_handler={self._new_handler}, "

        if self._max_handlers >= 0:
            value += f"_max_handlers={self._max_handlers}, "

        if self._delimiter != Chars.DOT:
            value += f"_delimiter=\"{self._delimiter}\", "

        if self._signature is not None:
            value += f"{self._signature}"

        return value.rstrip(", ") + ")"

    def __iadd__(self, handler):
        """
        Registers a function to an un-named event.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        NOTE: handler can also be a collection of handlers
        or even a tuple (event += handler1, handler2).

        :param handler: the function to add as handler
        """
        try:
            iter(handler)
        except TypeError:
            if callable(handler):
                self.on(handler=handler)
        else:
            for item in handler:
                if callable(item):
                    self.on(handler=item)

        return self

    def __isub__(self, handler):
        """
        Removes a function that is registered to the un-named event.

        NOTE: handler can also be a collection of handlers
        or even a tuple (event += handler1, handler2).

        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        """
        try:
            iter(handler)
        except TypeError:
            if callable(handler):
                self.off(handler=handler)
        else:
            for item in handler:
                if callable(item):
                    self.off(handler=item)

        return self

    def signature(self, **kwargs) -> Event:
        """
        Sets the event signature.

        :param kwargs: the keyword signature to set
        :return: this instance for use in method chaining
        """
        self._signature = Signature(**kwargs)
        return self

    def is_wildcard_enabled(self) -> bool:
        """
        Returns True if wildcard is enabled.

        :return: True if wildcard is enabled
        """
        return self._wildcard

    def enable_wildcard(self) -> Event:
        """
        Enables wildcard.

        :return: this instance for use in method chaining
        """
        self._wildcard = True
        return self

    def disable_wildcard(self) -> Event:
        """
        Disables wildcard.

        :return: this instance for use in method chaining
        """
        self._wildcard = False
        return self

    @property
    def delimiter(self) -> str:
        """
        Returns the delimiter.

        :return: the delimiter
        """
        return self._delimiter

    @delimiter.setter
    def delimiter(self, delimiter: str) -> NoReturn:
        """
        Sets the delimiter.

        :param delimiter: the delimiter to set
        """
        self._delimiter = delimiter

    def is_new_handler_enabled(self) -> bool:
        """
        Returns True if new handler is enabled.

        :return: True if new handler is enabled
        """
        return self._new_handler

    def enable_new_handler(self) -> Event:
        """
        Enables new_handler.

        :return: this instance for use in method chaining
        """
        self._new_handler = True
        return self

    def disable_new_handler(self) -> Event:
        """
        Disables new_handler.

        :return: this instance for use in method chaining
        """
        self._new_handler = False
        return self

    @property
    def max_handlers(self) -> int:
        """
        Returns the value of max_handlers.

        :return: the value of max_handlers
        """
        return self._max_handlers

    @max_handlers.setter
    def max_handlers(self, max_handlers: int) -> NoReturn:
        """
        Sets the value of max_handlers.

        :param max_handlers: the value to set
        """
        self._max_handlers = max_handlers

    def _check_handler_length(self, obj, requirement_name: str, value_name: str, exception, signature: Signature):
        # Checks to see if there is fewer parameters than what is required
        if len(obj) < signature.length:
            if signature.length == 1:
                arg_error_text = f"{requirement_name} must have at least 1 {value_name}:"
            else:
                arg_error_text = f"{requirement_name} must have at least " \
                                 f"{signature.length} {value_name}s:"

            if len(obj) == 0:
                arg_text = f"and instead has 0 {value_name}s."
            elif len(obj) == 1:
                arg_text = f"and instead only has 1 {value_name}."
            else:
                arg_text = "and instead only has " \
                           f"{len(obj)} {value_name}s."

            raise exception(arg_error_text
                            + f" ({self}) "
                            + arg_text)

    def _verify_handler(self, handler: Callable, signature: Signature) -> NoReturn:
        """
        Verifies if the specified handler matches the signature.

        :param handler: the handler to verify
        :param signature: the signature to match
        :raises EventHandlerMismatchError: if the handler doesn't match
        """
        params = Signature(handler).parameters

        # Skip check if only param in handler is kwargs
        if not (len(params) == 1
                and list(params.values())[0].kind == inspect.Parameter.VAR_KEYWORD):

            self._check_handler_length(params, "Handler", "parameter", EventHandlerMismatchError, signature)

            index_offset = 0

            # Loops through all the parameters to see if they match the signature
            for index, param in enumerate(params.values(), 0):
                arg_error_text = "Signature Mismatch " \
                                 f"({self}) " \
                                 f"[Parameter #{index + 1} '{param.name}']: "

                mod_index = index + index_offset

                # Checks if this parameter can be assigned by a keyword argument
                if param.kind == param.POSITIONAL_ONLY:
                    raise EventHandlerMismatchError(
                        arg_error_text +
                        "Cannot be assigned with keyword argument!")

                # Checks if the current param a *args
                if param.kind == param.VAR_POSITIONAL:
                    # Checks if any params exist after *args
                    if index == len(params) - 1:
                        raise EventHandlerMismatchError(
                            arg_error_text +
                            f"No match after '{param.name}'"
                            " that can be assigned with keyword "
                            "argument!")

                    index_offset -= 1

                # Skip if the current param is a **kwargs
                elif param.kind == param.VAR_KEYWORD:
                    break

                # Checks if this is an additional parameter beyond signature requirement
                elif mod_index > signature.length - 1:
                    # Checks if this additional parameter has a default value
                    if param.default is param.empty:
                        raise EventHandlerMismatchError(
                            arg_error_text + "No Default Value!")
                    else:
                        self._warning(arg_error_text +
                                      f"Default Value - '{param.default}'")

                # Checks if this parameter has the correct name
                elif param.name != signature.names[mod_index]:
                    raise EventHandlerMismatchError(
                        arg_error_text +
                        "Name should be "
                        f"'{signature.names[mod_index]}'.")

                # Checks if this parameter has the correct type
                elif param.annotation is not param.empty:
                    param_type: type = param.annotation

                    if not is_subclass(param_type, signature.types[mod_index]):
                        raise EventHandlerMismatchError(
                            arg_error_text +
                            "Type should be "
                            f"'{str(signature.types[mod_index])}' "
                            f"not {str(param_type)}.")

        return handler

    def on(self, event: str | StringValue | Namespace = "",
           handler: Callable = None,
           ttl: int = -1) -> Callable:
        """
        Registers a function to an event.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param event: the event to register
        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        :param ttl: the amount of times to listen. Negative values mean
            infinity.
        """

        def on(func: Callable) -> Callable:
            """
            The internal *on* function.

            :param func: the function to add as handler
            :return: the function
            """
            # if func is not callable or None, ignore
            if not callable(func):
                return func

            if isinstance(event, Namespace):
                namespace = event
            else:
                namespace = Namespace(event)

            if namespace.name == self._NEW_HANDLER.name:
                self._verify_handler(func, self._new_handler_signature)
            else:
                self._verify_handler(func, self._signature)

            # Grab current root branch and create
            # new branches if they don't exist
            branch = self._root.expand_namespace(namespace)

            # Grab the list of handlers in the lowest level branch in
            # the namespace
            handlers = branch.get_handlers()

            # If max handlers isn't disabled (-1)
            # then check if handlers has exceeded max handlers
            if 0 <= self._max_handlers <= len(handlers):
                self._warning("Cannot add "
                              f"'{FuncInfo(func).full_name}' "
                              f"as handler to '{str(event)}' event, "
                              f"Max handlers ({self._max_handlers}) "
                              f"has been exceeded!")
                return func

            # Create a new handler and append it to the list
            new_handler = _Handler(func, namespace, ttl)
            branch.add_handler(new_handler)

            self._debug(f"New handler '{func.__name__}' added for event '{namespace}'!")

            # If new_handler is enabled then emit new_handler event
            if self._new_handler:
                self.fire(self._NEW_HANDLER, func=func, evt=namespace.name)

            return func

        return on(handler) if handler else on

    def on_new_handler(self, handler: Callable = None, ttl: int = -1) -> Callable:
        """
        Registers a function to the 'new_handler' event.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param handler: the function to add as handler
        :param ttl: the amount of times to listen. Negative values mean
            infinity.
        """
        return self.on(self._NEW_HANDLER, handler, ttl)

    def once(self, event: str | StringValue | Namespace,
             handler: Callable = None):
        """
        Registers a function to an event that is called once.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param event: the event to register
        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        """
        return self.on(event, handler=handler, ttl=1)

    def on_any(self, handler: Callable = None, ttl: int = -1) -> Callable:
        """
        Registers a function that is called every time an event is emitted.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        :param ttl: the amount of times to listen. Negative values mean
            infinity.
        """

        def on_any(func: Callable) -> Callable:
            """
            The internal *on any* function.

            :param func: the function to add as handler
            :return: the function
            """
            # if func is not callable or None, ignore
            if not callable(func):
                return func

            # Grab the list of handlers in the root branch
            handlers = self._root.get_handlers()

            # If max handlers isn't disabled (-1)
            # then check if handlers has exceeded max handlers
            if 0 <= self._max_handlers <= len(handlers):
                return func

            # Create a new handler and append it to the list
            new_handler = _Handler(func, None, ttl)
            self._root.add_handler(new_handler)

            self._debug(f"New handler '{func.__name__}' added for 'on_any'!")

            # If new_handler is enabled then emit new_handler event
            if self._new_handler:
                self.fire(self._NEW_HANDLER, func=func, evt="")

            return func

        return on_any(handler) if handler else on_any

    def off(self,
            event: str | StringValue | Namespace = "",
            handler: Callable = None) -> Callable:
        """
        Removes a function that is registered to an event.

        :param event: the event to de-register
        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        """

        def off(func: Callable) -> Callable:
            """
            The internal *off* function.

            :param func: the function to remove as handler
            :return: the function
            """
            if isinstance(event, Namespace):
                namespace = event
            else:
                namespace = Namespace(event)

            # Grab the lowest level branch in the namespace
            branch = self._root.find_branch(namespace)

            # If the branch doesn't exist, ignore
            if branch is None:
                self._warning("Cannot remove "
                              f"'{FuncInfo(func).full_name}' "
                              f"handler from '{str(event)}' event, "
                              f"Event doesn't exist!")
                return func

            branch.remove_handler(func)

            self._debug(f"Removed handler '{func.__name__}' from event '{namespace}'!")

            return func

        return off(handler) if handler else off

    def off_any(self, handler: Callable = None) -> Callable:
        """
        Removes a function that was registered via 'on_any'.

        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        """

        def off_any(func: Callable) -> Callable:
            """
            The internal *off any* function.

            :param func: the function to remove as handler
            :return: the function
            """
            self._root.remove_handler(func)

            self._debug(f"Removed all 'on_any' event handlers!")

            return func

        return off_any(handler) if handler else off_any

    def off_all(self) -> NoReturn:
        """
        Removes all registered functions.
        """
        self._root = Branch("ROOT")

        self._debug(f"Removed all event handlers!")

    def handlers(self,
                 event: str | StringValue | Namespace = "") \
            -> list[Callable]:
        """
        Returns all functions that are registered to an event.
        Wildcards are not applied.

        :param event: the event to lookup
        :return: all functions that are registered to an event
        """
        if isinstance(event, Namespace):
            namespace = event
        else:
            namespace = Namespace(event)

        # Grab the lowest level branch in the namespace
        branch = self._root.find_branch(namespace)

        # If the branch doesn't exist, return empty list
        if branch is None:
            return []

        return [handler.func for handler in branch.get_handlers()]

    def handlers_any(self) -> list[Callable]:
        """
        Returns all functions that were registered using 'on_any'.

        :return: all functions that were registered using 'on_any'
        """
        return [handler.func for handler in self._root.get_handlers()]

    def handlers_all(self) -> list[Callable]:
        """
        Returns all registered functions.

        :return: all registered functions
        """

        # Grab the list of handlers in the root branch
        handlers = self._root.get_handlers()

        # Grab the list of all branches
        branches = self._root.get_branches()

        # Look for handlers in any sub-branches
        for branch in branches:
            # If more sub-branches found add to list
            branches.extend(branch.get_branches())

            # If handlers found add to list
            handlers.extend(branch.get_handlers())

        return [handler.func for handler in handlers]

    def fire(self,
             event: str | StringValue | Namespace = "",
             *args, **kwargs) -> NoReturn:
        """
        Fires an *event*. All functions of events that match *event*
        are invoked with *kwargs* in the exact order of
        their registration. Wildcards might be applied.

        :param event: the event to fire
        :param kwargs: keyword args to pass to handlers
        """
        self._fire(event, False, *args, **kwargs)

    def fire_reverse(self,
                     event: str | StringValue | Namespace = "",
                     *args, **kwargs) -> NoReturn:
        """
        Fires an *event*. All functions of events that match *event*
        are invoked with *kwargs* in the reverse order of
        their registration. Wildcards might be applied.

        :param event: the event to fire
        :param kwargs: keyword args to pass to handlers
        """
        self._fire(event, True, *args, **kwargs)

    def _fire(self,
              event: str | StringValue | Namespace, reverse: bool,
              *args, **kwargs) -> NoReturn:
        # Grab the list of handlers in the root branch
        handlers = self._root.get_handlers()

        if isinstance(event, Namespace):
            namespace = event
        else:
            namespace = Namespace(event)

        if namespace.name == self._NEW_HANDLER.name:
            self._new_handler_signature.verify_args(*args, **kwargs)
        else:
            self._signature.verify_args(*args, **kwargs)

        # Grab the list of branches
        branches = self._root.get_namespace_branches(
            namespace, self.is_wildcard_enabled())

        # Add all handlers from found branches to the list
        for branch in branches:
            handlers.extend(branch.get_handlers())

        if reverse:
            self._debug(f"Firing event '{namespace}' in reverse order!")
        else:
            self._debug(f"Firing event '{namespace}'!")

        # Call handlers in the order of their registration time
        for handler in sorted(handlers,
                              key=lambda hdr: hdr.time,
                              reverse=reverse):
            handler.handle(*args, **kwargs)

        # Remove handlers whose ttl value is 0
        for handler in handlers:
            if handler.ttl == 0:
                self.off(event=handler.namespace.name, handler=handler.func)


class EventSignatureError(Exception):
    """The EventSignatureError."""


class EventHandlerMismatchError(Exception):
    """The EventHandlerMismatchError."""


class EventFireMismatchError(Exception):
    """The EventFireMismatchError."""
