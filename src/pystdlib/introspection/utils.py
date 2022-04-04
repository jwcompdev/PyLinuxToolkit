# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# utils.py
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

"""Contains basic introspection utilities."""
from __future__ import annotations

import inspect
import sys
from types import ModuleType


def get_method_parent(meth) -> type | None:
    """
    Returns the class of the parent of the specified method.

    :param meth: the method to check
    :return: the class of the parent of the specified method
    """
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
    return getattr(meth, "__objclass__", None)  # handle special descriptor objects


def get_method_name_from_frame(frame) -> str:
    """
    Retrieves the method name from the specified frame.

    :param frame: the frame to check
    :return: the method name from the specified frame
    """
    return frame.f_code.co_name


def get_class_instance_from_frame(frame):
    """
    Retrieves the class instance from the specified frame.

    :param frame: the frame to check
    :return: the class instance from the specified frame
    """
    return frame.f_locals.get("self", None)


def get_class_from_frame(frame) -> type | None:
    """
    Retrieves the class object from the specified frame.

    :param frame: the frame to check
    :return: the class object from the specified frame
    """
    instance = frame.f_locals.get("self", None)
    if instance:
        # return its class
        return getattr(instance, "__class__", None)
    # return None otherwise
    return None


def get_module_from_frame(frame) -> ModuleType | None:
    """
    Retrieves the module from the specified frame.

    :param frame: the frame to check
    :return: the module from the specified frame
    """
    module = None
    instance = frame.f_locals.get("self", None)
    if instance:
        # return its class
        cls = getattr(instance, "__class__", None)
        module = sys.modules[cls.__module__]

    if module is None:
        module = sys.modules["__main__"]

    # return None otherwise
    return module
