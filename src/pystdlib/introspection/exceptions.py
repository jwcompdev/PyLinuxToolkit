# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# exceptions.py
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

"""Contains the introspection Exceptions."""


class FuncError(Exception):
    """The base FuncError."""


class FuncSignatureError(FuncError):
    """The FuncSignatureError."""


class FuncArgsMismatchError(FuncError):
    """The FuncArgsMismatchError."""


class FuncReturnMismatchError(FuncError):
    """The FuncReturnMismatchError."""
