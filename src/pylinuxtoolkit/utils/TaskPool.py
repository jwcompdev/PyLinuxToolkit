# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# TaskPool.py
# Copyright (C) 2022 JWCompDev <jwcompdev@outlook.com>
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
This file contains the TaskPool class, a pool of any combination of
threaded or un-threaded tasks that run in the order they are created.
"""
from __future__ import annotations

import functools
from threading import Thread
from time import sleep
from typing import final, NoReturn

from pylinuxtoolkit.utils.Types import Final
from pylinuxtoolkit.utils.Values import BooleanValue, StringValue


@final
class TaskPool(metaclass=Final):
    """
    Creates a pool of any combination of threaded or un-threaded tasks
    that run in the order they are created.
    """

    def __init__(self):
        self.running_thread = 1
        self.current_thread_id = 0

    # noinspection PyMethodParameters
    def decide_class_task(
        pool_name: str = "task_pool",
        threaded: bool | BooleanValue | str | StringValue = True,
    ) -> NoReturn:
        """
        Decorator that creates a task each time
        the decorated function is called.

        If threaded is True the task is run threaded,
        otherwise it is run non-threaded. (Default is True)

        NOTE: If you want to decorate a function you
        need to use instance.decide_task instead.

        :param pool_name: the string name of the task pool instance
        :param threaded: if True the task is run threaded,
            otherwise it is run non-threaded. This may also be the name
            of a method inside the class to be called to retrieve
            the value.
        :return: the new decorated class method
        :raises AttributeError: if a variable with the name matching
            the pool_name argument is not found in the class or if the
            name of a method as a string is supplied to the threaded
            argument, and a matching method is not found in the class
        :raises TypeError: if the name of a method as a string is
            supplied to the threaded argument, and it isn't callable
        :raises ValueError: if the variable with the name matching
            the pool_name argument is found in the class but is
            not an instance of the type TaskPool
        """

        # noinspection PyMissingOrEmptyDocstring
        def pass_name(func) -> NoReturn:
            # noinspection PyMissingOrEmptyDocstring
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs) -> NoReturn:
                if isinstance(threaded, str) or isinstance(threaded, StringValue):
                    threaded_name = str(threaded)
                    try:
                        threaded_func = getattr(self, threaded_name.lstrip("self."))
                    except AttributeError as e:
                        if "object has no attribute '" + threaded_name + "'" in str(e):
                            e.args = (
                                "Function by the name '"
                                + threaded_name
                                + "' specified to return the threaded"
                                + " value not found in the '"
                                + type(threaded_name).__name__
                                + "' class!",
                            )
                            raise
                        else:
                            raise
                    if callable(threaded_func):
                        final_condition = bool(threaded_func())
                    else:
                        raise TypeError(
                            "Specified method by the name '"
                            + threaded
                            + "' is not callable! (Type is: '"
                            + type(threaded).__name__
                            + "')"
                        )
                else:
                    final_condition = bool(threaded)

                TaskPool._internal_class_method_wrapper(
                    self, pool_name, final_condition, func, *args, **kwargs
                )

            return wrapper

        return pass_name

    # noinspection PyMethodParameters
    def threaded_class_task(pool_name: str = "task_pool") -> NoReturn:
        """
        Decorator that creates a threaded task each time
        the decorated class method is called.

        NOTE: If you want to decorate a function you
        need to use instance.threaded_task instead.

        :param pool_name: the string name of the task pool instance
        :return: the new decorated class method
        """

        # noinspection PyMissingOrEmptyDocstring
        def pass_name(func) -> NoReturn:
            # noinspection PyMissingOrEmptyDocstring
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs) -> NoReturn:
                TaskPool._internal_class_method_wrapper(
                    self, pool_name, True, func, *args, **kwargs
                )

            return wrapper

        return pass_name

    # noinspection PyMethodParameters
    def non_threaded_class_task(pool_name: str = "task_pool") -> NoReturn:
        """
        Decorator that creates a non-threaded task each time
        the decorated class method is called.

        NOTE: If you want to decorate a function you
        need to use instance.non_threaded_task instead.

        :param pool_name: the string name of the task pool instance
        :return: the new decorated class method
        """

        # noinspection PyMissingOrEmptyDocstring
        def pass_name(func) -> NoReturn:
            # noinspection PyMissingOrEmptyDocstring
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs) -> NoReturn:
                TaskPool._internal_class_method_wrapper(
                    self, pool_name, False, func, *args, **kwargs
                )

            return wrapper

        return pass_name

    def threaded_task(self, func) -> NoReturn:
        """
        Decorator that creates a threaded task each time
        the decorated function is called.

        NOTE: If you want to decorate a class method you
        need to use instance.threaded_class_task instead.

        :param func: the function that is decorated
        :return: the new decorated function
        """

        # noinspection PyMissingOrEmptyDocstring
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> NoReturn:
            self._threaded(func, *args, **kwargs)

        return wrapper

    def non_threaded_task(self, func) -> NoReturn:
        """
        Decorator that creates a non-threaded task each time
        the decorated function is called.

        NOTE: If you want to decorate a class method you
        need to use instance.non_threaded_class_task instead.

        :param func: the function that is decorated
        :return: the new decorated function
        """

        # noinspection PyMissingOrEmptyDocstring
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> NoReturn:
            self._non_threaded(func, *args, **kwargs)

        return wrapper

    def decide_task(self, threaded=True) -> NoReturn:
        """
        Decorator that creates a task each time
        the decorated function is called.

        If threaded is True the task is run threaded,
        otherwise it is run non-threaded.

        NOTE: If you want to decorate a class method you
        need to use instance.decide_class_task instead.

        :param threaded: if True the task is run threaded,
            otherwise it is run non-threaded
        :return: the new decorated function
        """

        # noinspection PyMissingOrEmptyDocstring
        def validate(func) -> NoReturn:
            # noinspection PyMissingOrEmptyDocstring
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> NoReturn:
                if threaded:
                    self._threaded(func, *args, **kwargs)
                else:
                    self._non_threaded(func, *args, **kwargs)

            return wrapper

        return validate

    def _get_next_id(self) -> int:
        return self.current_thread_id + 1

    def _is_task_ready(self, task_id: int) -> bool:
        return self.running_thread == task_id

    def _threaded(self, func, *args, **kwargs) -> NoReturn:
        thread = Thread(
            target=self._base_task,
            args=(self._get_next_id(), func, *args),
            kwargs=kwargs,
        )
        thread.start()
        self.current_thread_id += 1

    def _non_threaded(self, func, *args, **kwargs) -> NoReturn:
        self._base_task(self._get_next_id(), func, *args, **kwargs)
        self.current_thread_id += 1

    def _base_task(self, task_id: int, func, *args, **kwargs) -> NoReturn:
        # print("Task " + str(task_id) + " Starting...")
        while not self._is_task_ready(task_id):
            sleep(0.001)

        func(*args, **kwargs)

        # print("Task " + str(task_id) + " Complete!")

        sleep(0.1)

        # Makes the next thread run
        self.running_thread += 1

    @staticmethod
    def _internal_class_method_wrapper(
        local_self, pool_name: str, threaded: bool, func, *args, **kwargs
    ) -> NoReturn:
        if isinstance(pool_name, str):
            try:
                pool: TaskPool = getattr(local_self, pool_name.lstrip("self."))
                if isinstance(pool, TaskPool):
                    if threaded:
                        dec_func = pool.threaded_task
                    else:
                        dec_func = pool.non_threaded_task
                else:
                    raise ValueError(
                        "Specified variable by the name '"
                        + pool_name
                        + "' is not a TaskPool object!"
                    )
                return dec_func(func)(local_self, *args, **kwargs)
            except AttributeError as e:
                if "object has no attribute '" + pool_name + "'" in str(e):
                    e.args = (
                        "TaskPool instance variable by the name '"
                        + pool_name
                        + "' not found in the '"
                        + type(local_self).__name__
                        + "' class!",
                    )
                raise
        else:
            raise ValueError("pool_name must be a string!")
