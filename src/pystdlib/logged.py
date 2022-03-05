# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# logged.py
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
Contains the Logged class, a data object that contains
info about the most recent run command.
"""
import functools
import logging
from typing import NoReturn, Any


class Logged:
    """Class which can be inherited from to automatically adds a named
    logger to your class.

    Adds easy access to debug, info, warning, error, exception and log
    methods.

    >>> class MyClass(Logged):
    ...     def __init__(self):
    ...         Logged.__init__(self)
    >>> my_class = MyClass()
    >>> my_class._debug('debug')
    >>> my_class._info('info')
    >>> my_class._warning('warning')
    >>> my_class._error('error')
    >>> my_class._exception('exception')
    >>> my_class._log(0, 'log')
    """

    __logger: logging.Logger

    def __new__(cls, *args, **kwargs):
        cls.__logger = logging.getLogger(
            cls.__get_name(cls.__module__, cls.__name__))

        return super(Logged, cls).__new__(cls)

    @classmethod
    def __get_name(cls, *name_parts: str) -> str:
        return '.'.join(n.strip() for n in name_parts if n.strip())

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Return a logger with the specified name, creating it if necessary.

        If no name is specified, return the root logger.
        """
        return cls.__logger

    @classmethod
    def set_log_level(cls, level: int) -> NoReturn:
        """
        Sets the logging level of this logger.
        The 'level' must be an int or a str.
        """
        cls.__logger.setLevel(level)

    @classmethod
    def add_log_handler(cls, handler: logging.Handler) -> NoReturn:
        """
        Adds the specified handler to this logger.
        :param handler: the handler to add
        """
        cls.__logger.addHandler(handler)

    @classmethod
    @functools.wraps(logging.debug)
    def _debug(cls, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._debug("Houston, we have a %s",
        >>>              "thorny problem", exc_info=1)
        """
        cls.__logger.debug(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.info)
    def _info(cls, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._info("Houston, we have a %s",
        >>>             "interesting problem", exc_info=1)
        """
        cls.__logger.info(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.warning)
    def _warning(cls, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._warning("Houston, we have a %s",
        >>>                "bit of a problem", exc_info=1)
        """
        cls.__logger.warning(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.error)
    def _error(cls, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._error("Houston, we have a %s",
        >>>              "major problem", exc_info=1)
        """
        cls.__logger.error(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.exception)
    def _exception(cls, msg: str, *args: Any, exc_info=True, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Convenience method for logging an ERROR with exception
        information.
        """
        cls.__logger.exception(msg, *args, exc_info, **kwargs)

    @classmethod
    @functools.wraps(logging.critical)
    def _critical(cls, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._critical("Houston, we have a %s",
        >>>                 "major disaster", exc_info=1)
        """
        cls.__logger.critical(msg, *args, **kwargs)

    @classmethod
    @functools.wraps(logging.log)
    def _log(cls, level: int, msg: str, *args: Any, **kwargs: Any) -> NoReturn:
        # noinspection PyUnresolvedReferences
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument
        exc_info with a true value, e.g.

        >>> self._log(level, "We have a %s",
        >>>                   "mysterious problem", exc_info=1)
        """
        cls.__logger.log(level, msg, *args, **kwargs)
