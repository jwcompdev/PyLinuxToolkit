# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# decorators.py
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

"""Contains common use decorator functions."""
from __future__ import annotations

import cProfile
import functools
import inspect
import logging
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, Future
from functools import partial
from inspect import iscoroutinefunction, isgeneratorfunction
from typing import Any, Callable

from pystdlib.introspection import Func, Signature

logging_logger = logging.getLogger(__name__)

DEF = re.compile(r'\s*def\s*([_\w][_\w\d]*)\s*\(')
POS = inspect.Parameter.POSITIONAL_OR_KEYWORD
EMPTY = inspect.Parameter.empty

_DEFAULT_POOL = ThreadPoolExecutor()


class ClassPropertyContainer:
    """
    Allows creating a class level property (functionality for
    decorator).
    """

    def __init__(self, prop_get: Any, prop_set: Any = None):
        """
        Container that allows having a class property decorator.
        :param prop_get: Class property getter.
        :param prop_set: Class property setter.
        """
        self.prop_get: Any = prop_get
        self.prop_set: Any = prop_set

    def __get__(self, obj: Any, cls: type = None) -> Callable:
        """
        Get the property getter.
        :param obj: Instance of the class.
        :param cls: Type of the class.
        :return: Class property getter.
        """
        if cls is None:
            cls = type(obj)
        return self.prop_get.__get__(obj, cls)()

    def __set__(self, obj, value) -> Callable:
        """
        Get the property setter.
        :param obj: Instance of the class.
        :param value: A value to be set.
        :return: Class property setter.
        """
        if not self.prop_set:
            raise AttributeError("cannot set attribute")
        _type: type = type(obj)
        if _type == ClassPropertyMetaClass:
            _type = obj
        return self.prop_set.__get__(obj, _type)(value)

    def setter(self, func: Callable) -> ClassPropertyContainer:
        """
        Allows creating setter in a property like way.
        :param func: Getter function.
        :return: Setter object for the decorator.
        """
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.prop_set = func
        return self


class ClassPropertyMetaClass(type):
    """Metaclass that allows creating a standard setter."""

    def __setattr__(cls, key, value):
        """Overloads setter for class"""
        obj = None

        if key in cls.__dict__:
            obj = cls.__dict__.get(key)
        if obj and isinstance(obj, ClassPropertyContainer):
            return obj.__set__(cls, value)

        return super().__setattr__(key, value)


class ClassPropertiesMixin(metaclass=ClassPropertyMetaClass):
    """
    This mixin allows using class property setters (getters work
    correctly even without this mixin)
    """


class ConfigClassMeta(type):
    """
    Metaclass that validates class variables in configuration class.
    Requirements for class members are:
        "All members have to be upper case (if they do not start
        with an underscore)."

        "There is no constructor in the class."

        "There is no standard (instance) method in the class.
        Only class methods and static methods are allowed."
    """

    # noinspection SpellCheckingInspection
    def __new__(mcs, name, bases, attrs):
        # Filter all class attributes (variables, methods, etc.)
        #   and check if match conditions:
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                # Test standard (instance) methods
                raise RuntimeError(
                    "no 'standard' methods (instance-level methods) are "
                    "allowed in the config class. Only classmethods and "
                    "staticmethods are allowed "
                    f"('{attr_name}' is a 'standard' method).")
            if not attr_name.startswith("_") \
                    and not isinstance(attr_value, (classmethod, staticmethod)) \
                    and attr_name != attr_name.upper():
                raise RuntimeError(
                    f"all class variable names in class {name} "
                    f"must be upper case ('{attr_name}' value is not)")
        # Create the new type
        new_config_class: type = type.__new__(mcs, name, bases, attrs)

        # Disable class constructor (raises an error if called)
        def _raise_runtime_error(*_, **__):
            raise RuntimeError("configuration class cannot be instantiated")

        new_config_class.__init__ = _raise_runtime_error

        return new_config_class


class ConfigClassMixin(metaclass=ConfigClassMeta):
    """Mixin for configuration classes.
    Requirements for class members are:
        - All members have to be upper case (if they do not start
        with an underscore).
        - There is no constructor in the class.
        - There is no standard (instance) method in the class. Only
        class methods and static methods are allowed.
    """


def _fix(args, kwargs, sig):
    """
    Fix args and kwargs to be consistent
    with the signature
    """
    bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()  # needed for test_dan_schult
    return bound_args.args, bound_args.kwargs


########################################
# Basic Decorators                     #
########################################
def classproperty(func):
    """
    Create a decorator for a class level property.
    :param func: This class method is decorated.
    :return: Modified class method behaving like a class property.
    """
    if not isinstance(func, (classmethod, staticmethod)):
        # The method must be a classmethod (or staticmethod)
        func = classmethod(func)
    return ClassPropertyContainer(func)


# noinspection SpellCheckingInspection
def decorate(func, caller, extras=(), kwsyntax=False):
    """
    Decorates a function/generator/coroutine using a caller.
    If kwsyntax is True calling the decorated functions with keyword
    syntax will pass the named arguments inside the ``kw`` dictionary,
    even if such argument are positional, similarly to what 'functools.wraps'
    does. By default, kwsyntax is False and the arguments are untouched.

    This function is distributed under the "BSD 2-Clause "Simplified" License"
    and was origionally written by 'Michele Simionato' and can be found
    here: (https://github.com/micheles/decorator) v4.4.2

    See
    https://github.com/micheles/decorator/blob/master/docs/documentation.md
    for documentation.
    """
    sig = inspect.signature(func)
    if iscoroutinefunction(caller):
        async def fun(*args, **kwargs):
            """
            The coroutine decorator.

            :param args: the positional args
            :param kwargs: the keyword args
            :return: the decorator
            """
            if not kwsyntax:
                args, kwargs = _fix(args, kwargs, sig)
            return await caller(func, *(extras + args), **kwargs)
    elif isgeneratorfunction(caller):
        def fun(*args, **kwargs):
            """
            The generator decorator.

            :param args: the positional args
            :param kwargs: the keyword args
            :return: the decorator
            """
            if not kwsyntax:
                args, kwargs = _fix(args, kwargs, sig)
            for res in caller(func, *(extras + args), **kwargs):
                yield res
    else:
        def fun(*args, **kwargs):
            """
            The function decorator.

            :param args: the positional args
            :param kwargs: the keyword args
            :return: the decorator
            """
            if not kwsyntax:
                args, kwargs = _fix(args, kwargs, sig)
            return caller(func, *(extras + args), **kwargs)
    fun.__name__ = func.__name__
    fun.__doc__ = func.__doc__
    fun.__wrapped__ = func
    fun.__signature__ = sig
    fun.__qualname__ = func.__qualname__
    # builtin functions like default dict.__setitem__ lack many attributes
    try:
        fun.__defaults__ = func.__defaults__
    except AttributeError:
        pass
    try:
        fun.__kwdefaults__ = func.__kwdefaults__
    except AttributeError:
        pass
    try:
        fun.__annotations__ = func.__annotations__
    except AttributeError:
        pass
    try:
        fun.__module__ = func.__module__
    except AttributeError:
        pass
    try:
        fun.__dict__.update(func.__dict__)
    except AttributeError:
        pass
    return fun


# noinspection SpellCheckingInspection
def decorator(caller, kwsyntax=False):
    """
    Converts a caller function into a decorator.

    If kwsyntax is True calling the decorated functions with keyword
    syntax will pass the named arguments inside the 'kw' dictionary,
    even if such argument are positional, similarly to what
    'functools.wraps' does. By default, kwsyntax is False and the
    arguments are untouched.

    This function is distributed under the "BSD 2-Clause "Simplified" License"
    and was origionally written by 'Michele Simionato' and can be found
    here: (https://github.com/micheles/decorator) v4.4.2

    See
    https://github.com/micheles/decorator/blob/master/docs/documentation.md
    for documentation.

    :param caller: the caller function
    :param kwsyntax: if True arguments decorate passed inside
        the 'kw' dictionary.
    """
    sig = inspect.signature(caller)
    dec_params = [p for p in sig.parameters.values() if p.kind is POS]

    def dec(func=None, *args, **kwargs):
        """
        The decorator.

        :param func: the function
        :param args: the positional args
        :param kwargs: the keyword args
        :return: the decorator
        """
        num_args = len(args) + 1
        extras = args + tuple(kwargs.get(p.name, p.default)
                              for p in dec_params[num_args:]
                              if p.default is not EMPTY)
        if func is None:
            return lambda l_func: decorate(l_func, caller, extras, kwsyntax)

        return decorate(func, caller, extras, kwsyntax)

    dec.__signature__ = sig.replace(parameters=dec_params)
    dec.__name__ = caller.__name__
    dec.__doc__ = caller.__doc__
    dec.__wrapped__ = caller
    dec.__qualname__ = caller.__qualname__
    dec.__kwdefaults__ = getattr(caller, '__kwdefaults__', None)
    dec.__dict__.update(caller.__dict__)
    return dec


def do_nothing(func):
    """
    Used in decorator if conditions.

    >>> PROD = False
    >>> @(do_nothing if PROD else show_time)

    :param func: the function
    """
    return func


########################################
# Performance Decorators               #
########################################
@decorator
def warn_slow(func, timelimit=60, *args, **kwargs):
    # noinspection SpellCheckingInspection
    """
    Decorator that prints a log message if the function execution
    took longer then specified.

    >>> @warn_slow  # warn if it takes more than 1 minute
    >>> def preprocess_input_files(inputdir, tempdir):
    ...
    >>> @warn_slow(timelimit=600)  # warn if it takes more than 10 minutes
    >>> def run_calculation(tempdir, outdir):
    ...
    >>>

    :param func: the decorated function
    :param timelimit: the time limit before warning
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    run_time = end - start
    if run_time > timelimit:
        logging.warning(f"{func.__name__} took {run_time} seconds")
    else:
        logging.info(f"{func.__name__} took {run_time} seconds")
    return result


# noinspection SpellCheckingInspection
@decorator
def show_cputime(func, *args, **kwargs):
    """
    Display CPU Time statistics of given function.

    >>> @show_cputime
    >>> def complex_function(a, b, c):
    ...
    >>> complex_function()
    CPU time for __main__.complex_function:
    3 function calls in 0.013 CPU seconds

    >>> "ncalls  tottime  percall  cumtime  percall filename:lineno(function)"
    >>> "     1    0.013    0.013    0.013    0.013 test_time.py:6(test)"
    >>> "     1    0.000    0.000    0.000    0.000" \
    "{method 'disable' of '_lsprof.Profiler' objects}"
    >>> "     1    0.000    0.000    0.000    0.000 {range}"

    :param func: the decorated function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    print(f"CPU time for {Func(func).full_name}:")

    timer = cProfile.Profile()
    result = timer.runcall(func, *args, **kwargs)
    timer.print_stats()

    return result


@decorator
def show_docs(func, *args, **kwargs):
    """
    Display Docstrings of given function.

    >>> @show_docs
    >>> def complex_function():
    >>>     "Example Documentation for complex_function."
    ...
    >>> complex_function()
    Documentation for __main__.complex_function:
    Example Documentation for complex_function.
    >>>

    :param func: the decorated function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    func = Func(func)

    print(f"Documentation for {func.full_name}:")
    print(func.doc)

    return func(*args, **kwargs)


def show_time(func=None, *, handler=None):
    """
    Display Runtime statistics of given function.

    A custom handler can be passed as a parameter. If no
    handler is supplied, the info is printed as a debug log.
    If provided, a custom exception
    handler must be of type Callable[Exception, Generic[T]]. In other
    words, its signature must take one parameter of type Exception.

    >>> @show_time
    >>> def some_function(a):
    ...
    >>> some_function()
    __main__.some_function executed in
    0.000688076019287 seconds
    >>>
    :param func: the function, if None decorator
        usage is assumed
    :param handler: a change_function that will be called
        when func is done execution
    :return: the function return value
    """

    @decorator
    def _wrapper(_func, *args, **kwargs):
        _func = Func(_func)

        result = _func(*args, **kwargs)

        if handler:
            handler(_func.full_name, _func.last_run_time_string)
        logging_logger.debug(f"{_func.full_name}"
                             f" executed in {_func.last_run_time_string} seconds")

        return result

    return _wrapper if func is None else _wrapper(func)


@decorator
def show_trace(func, *args, **kwargs):
    # noinspection PyShadowingNames
    """
    Display epic argument and context call information of given function.

    >>> @show_trace
    >>> def complex_function(a, b, c, **kwargs):
    ...
    >>> complex_function('alpha', 'beta', False, debug=True)
    calling haystack.submodule.complex_function with
    args: ({'a': 'alpha', 'b': 'beta', 'c': False},)
    kwargs: {'debug': True}
    >>>

    :param func: the decorated function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    func = Func(func)

    print(f"Calling {func.full_name} with: \n   "
          f"args: {args} \n   "
          f"kwargs: {kwargs}")

    return func(*args, **kwargs)


def show_num_calls(func):
    """
    Count the number of calls to a function.

    :param func: the decorated function
    :return: the function return value
    """

    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        _wrapper.num_calls += 1
        return func(*args, **kwargs)

    _wrapper.num_calls = 0
    return _wrapper


########################################
# Class Helper Decorators              #
########################################
def auto_args(func):
    """
    A decorator for automatically copying constructor arguments to `self`.

    :param func: the decorated function
    :return: the function return value
    """
    # Get a signature object for the target method:
    sig = inspect.signature(func)

    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        # Parse the provided arguments using the target's signature:
        bound_args = sig.bind(self, *args, **kwargs)
        # Save away the arguments on `self`:
        for key, value in bound_args.arguments.items():
            if key != "self":
                setattr(self, key, value)
        # Call the actual constructor for anything else:
        return func(self, *args, **kwargs)

    return _wrapper


def singleton(cls):
    """
    Makes the decorated class a singleton.

    :param cls: the decorated class
    :return: the singleton class instance
    """

    @functools.wraps(cls)
    def _wrapper(*args, **kwargs):
        if _wrapper.instance is None:
            _wrapper.instance = cls(*args, **kwargs)
        return _wrapper.instance

    _wrapper.instance = None
    return _wrapper


########################################
# Function Helper Decorators           #
########################################
@decorator
def sleep_after(func, duration: int = 0, *args, **kwargs):
    """
    Sleeps for the specified number of seconds after
    running the function.

    :param func: the decorated function
    :param duration: the number of seconds to sleep
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    result = func(*args, **kwargs)
    time.sleep(duration)
    return result


@decorator
def sleep_before(func, duration: int = 0, *args, **kwargs):
    """
    Sleeps for the specified number of seconds before
    running the function.

    :param func: the decorated function
    :param duration: the number of seconds to sleep
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    time.sleep(duration)
    return func(*args, **kwargs)


# noinspection PyUnusedLocal
@decorator
def todo(func, message="This function is not yet implemented.", *args, **kwargs):
    """
    Mark a function as to-do so that it throws an error when called.

    :param func: the decorated function
    :param message: the error message to display
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :returns: No Value
    """
    raise NotImplementedError(message)


# noinspection SpellCheckingInspection
def trycatch(func=None, *, exception=None, handler=None, silent=False):
    """
    Wraps the function in a try-catch block.

    At least one exception init the 'exception' argument will be
    expected to be caught. This may be one exception, a list or
    a tuple of multiple exceptions.

    If no exception is provided, by default all exceptions will be
    caught excluding SystemExit, KeyboardInterrupt and GeneratorExit
    since they do not subclass the generic Exception class.

    A custom exception handler can be passed as a parameter. If no
    handler is supplied, a stack trace is logged to stderr and the
    program will continue executing. If provided, a custom exception
    handler must be of type Callable[Exception, Generic[T]]. In other
    words, its signature must take one parameter of type Exception.

    NOTE: If an exception is thrown the function will return None.

    >>> @trycatch
    >>> def function():
    >>>     print(0/0) # Division by 0 must raise exception
    ...
    >>> function()
    >>>

    :param func: the function, if None decorator usage is
        assumed
    :param exception: the exception, list or tuple of
        exceptions to check
    :param handler: a function that will be called when an
        exception occurs
    :param silent: if True ignores any exception that occurs
    :return: the function return value
    """
    if not exception:
        exception = Exception
    elif type(exception) is list:
        exception = tuple(exception)

    @decorator
    def _wrapper(_func, *args, **kwargs):
        try:
            return _func(*args, **kwargs)
        except exception as exc:
            if not silent:
                if not handler:
                    logging.exception("Exception occurred during execution"
                                      f" of '{_func.__name__}': [{exc}]")
                else:
                    handler(_func.__name__, exc)

            return None

    return _wrapper if func is None else _wrapper(func)


# noinspection SpellCheckingInspection
def silent_trycatch(func=None, *, exception=None):
    """
    Wraps the change_function init a try-catch block that
    ignores any exceptions that occur.

    This is equivalent to running "@trycatch(silent=True)"

    >>> @silent_trycatch
    ... def function():
    ...     print(0/0) # Division by 0 must raise exception
    ...
    >>> function()
    >>>

    :param func: the decorated function, if None decorator usage
        is assumed
    :param exception: the exception, list or tuple of exceptions
        to check. If empty all exceptions will be caught
    :return: the function return value
    """
    return trycatch(func=func, exception=exception, silent=True)


def throttle(func=None, *, limit=1, every=1):
    # noinspection GrazieInspection
    """
    Throttle the rate the function can be invoked.

    The rate is `limit` over `every`, where limit is the number of
    invocation allowed every `every` seconds.
    "throttle(4, 60)" creates a decorator that limits the function calls
    to 4 per minute. If not specified, "every" defaults to 1 second.

    :param func: the function, if None decorator
        usage is assumed
    :param limit: the limit
    :param every: the number of seconds frequency
    :return: the function return value
    """
    semaphore = threading.Semaphore(limit)

    @decorator
    def _wrapper(_func, *args, **kwargs):
        semaphore.acquire()

        try:
            return _func(*args, **kwargs)

        finally:  # ensure semaphore release
            timer = threading.Timer(every, semaphore.release)
            timer.daemon = True  # allows the timer to be canceled on exit
            timer.start()

    return _wrapper if func is None else _wrapper(func)


@decorator
def require_root(func, *args, **kwargs):
    """
    Runs the decorated function only if user has root/sudo permission.

    :param func: the decorated function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value
    """
    if os.getuid() == 0:
        result = func(*args, **kwargs)
        return result

    logging_logger.critical("[PERMISSION REQUIRED!] You need to be a root user "
                            f"to execute function [{func.__name__}()]")
    sys.exit(0)


########################################
# Validation Decorators                #
########################################


def accepts(func=None, **signature):
    """
    Verifies that the specified signature matches the arguments
    when the function is called.

    If the signature is None then the type hints on the function
    are checked instead.

    :param func: the function to check, if None decorator usage is
        assumed
    :param signature: the signature to check, if empty the type
        hints on the function decorate checked instead
    :return: The result of the function if verification didn't fail
    """

    @decorator
    def _wrapped(_func, *args, **kwargs):
        if signature is not None:
            sig = Signature(signature)
        else:
            _func = Func(_func)
            sig = _func.signature

        sig.verify_args(*args, **kwargs)

        return _func(*args, **kwargs)

    return _wrapped if func is None else _wrapped(func)


def returns(func=None, return_type=None):
    """
    Verifies that the specified type is returned by the function

    :param func: the change_function to check, if
        None decorator usage is assumed
    :param return_type: the expected return type
    :return: the function return value if the type matches
    """

    @decorator
    def _wrapped(_func, *args, **kwargs):
        func_instance = Func(_func)
        result = func_instance(*args, **kwargs)

        match = (isinstance(result, return_type)
                 or issubclass(type(result), return_type))

        if not match:
            raise ValueError("Return value Mismatch:"
                             f"\n>>> Expected: '{return_type.__name__}',"
                             f" Found: '{type(result).__name__}'"
                             f" with value '{str(result)}'")
        return result

    return _wrapped if func is None else _wrapped(func)


########################################
# Threading Decorators                 #
########################################
@decorator
def threaded(func, *args, **kwargs):
    # noinspection GrazieInspection,PyShadowingNames
    """
    Runs the function in a thread.

    Description:
        - Using standard threading.Thread for creating thread
        - Can pass args and kwargs to the function
        - Will start a thread but will give no control over it

    >>> @threaded
    >>> def display(name, *args, **kwargs):
    >>>     for i in range(5):
    >>>             print('Printing {} from thread'.format(name))
    ...
    >>> display('Siddhesh')
    Printing ('Siddhesh',) from thread
    Thread started for function <function display at 0x7f1d60f7cb90>
    Printing ('Siddhesh',) from thread
    Printing ('Siddhesh',) from thread
    Printing ('Siddhesh',) from thread
    Printing ('Siddhesh',) from thread
    >>>

    :param func: the decorated function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: No Return
    """
    threading.Thread(target=func, args=(args, kwargs)).start()
    logging_logger.debug(f'Thread started for function {func}')


@decorator
def thread_pool(func, executor: ThreadPoolExecutor = None,
                *args, **kwargs) -> Future:
    # noinspection PyProtectedMember
    """
    Runs the function in a thread pool.

    Description:
        - Using ThreadPoolExecutor for creating thread
        - Can pass args and kwargs to the function
        - Will start a thread but will give no control over it,
            but you can call '.result()' on the returned future
            to get the result.

    >>> @threaded
    >>> def waste_time(sleep_time):
    >>>     thread_name = threading.current_thread().name
    >>>     time.sleep(sleep_time)
    >>>     print(f"{thread_name} woke up after {sleep_time}s!")
    >>>     return 42
    >>>
    >>> t1 = waste_time(5)
    >>> t2 = waste_time(2)
    >>>
    >>> print(t1)           # <Future at 0x104130a90 state=running>
    >>> print(t1._result())  # 42
    ThreadPoolExecutor-0_1 woke up after 2s!
    ThreadPoolExecutor-0_0 woke up after 5s!
    >>>

    :param func: the decorated function
    :param executor: the executor pool to use,
        'None' creates a new instance
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: a future object that can be used to obtain the
        result by calling '.result()'
    """
    return (executor or _DEFAULT_POOL).submit(func, *args, **kwargs)


@decorator
def create_threads(func, thread_count=1, *args, **kwargs):
    # noinspection PyShadowingNames
    """
    Creates multiple threads of a single function.

    Description:
        - Using standard threading.Thread for thread creation
        - Can pass args and kwargs to the function
        - Will start number of threads based on the count specified while decorating

    >>> @create_threads(thread_count=2)
    >>> def p(*args, **kwargs):
    >>>     pass
    >>>
    >>> p()
    Thread started for function <function p at 0x7f6725ecccf8>
    Thread started for function <function p at 0x7f6725ecccf8>
    >>>

    :param func: the decorated function
    :param thread_count: the number of threads to create
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: No Return
    """
    for _ in range(thread_count):
        threading.Thread(target=func, args=(args, kwargs)).start()
        logging.info(f'Thread started for function {func}')


########################################
# Manipulation Decorators              #
########################################
def change_args(func=None, *args, **kwargs):
    """
    Injects the specified arguments into the function.

    :param func: the function to run, if None
        decorator usage is assumed
    :param args: the positional arguments to inject
    :param kwargs: run_in_thread keyword arguments to inject
    :return: the function return value
    """

    # noinspection PyUnusedLocal
    @decorator
    def _wrapper(_func, *unneeded_args, **unneeded_kwargs):
        return _func(*args, **kwargs)

    return _wrapper if func is None else _wrapper(func)


def change_function(func=None):
    """
    Hijacks the function call and runs the specified function instead.

    :param func: the function to run, if None
        decorator usage is assumed
    :return: the function return value
    """

    # noinspection PyUnusedLocal
    @decorator
    def _wrapper(unneeded_func, *args, **kwargs):
        """
        Hijacks the function call and runs the
        specified function instead.

        :param unneeded_func: the function to ignore
        :param args: the positional arguments
        :param kwargs: the keyword arguments
        :return: the decorated function
        """
        return func(*args, **kwargs)

    return _wrapper if func is None else _wrapper(func)


########################################
# Repeat/Retry Decorators              #
########################################
@decorator
def repeat(func, num: int = 1, *args, **kwargs):
    """
    Repeats execution of the function consecutively,
    as many times as specified and returns the result
    of the last run.

    :param func: the decorated function
    :param num: the number of times to run the function
    :param args: the positional args of the function
    :param kwargs: the keyword args of the function
    :return: the function return value of the last time the
        function was run
    """
    result = None
    for _ in range(num):
        result = func(*args, **kwargs)
    return result


def __retry_internal(func, exceptions=Exception, tries=-1, delay=0,
                     max_delay=None, backoff=1, jitter=0,
                     logger=logging_logger):
    """
    Executes a function and retries it if it failed.

    :param func: the function to execute
    :param exceptions: an exception or a tuple of exceptions to catch
    :param tries: the maximum number of attempts
    :param delay: initial delay between attempts
    :param max_delay: the maximum value of delay
    :param backoff: multiplier applied to delay between attempts
        (1 = no backoff)
    :param jitter: extra seconds added to delay between attempts.
        (fixed if a number, random if a range tuple (min, max))
    :param logger: logger.warning(fmt, error, delay) will be called on
        failed attempts. If None, logging is disabled.
    :returns: the function return value
    """
    _tries, _delay = tries, delay
    while _tries:
        try:
            return func()
        except exceptions as exc:
            _tries -= 1
            if not _tries:
                raise

            if logger is not None:
                logger.warning(f"{exc}, retrying in {_delay} seconds...")

            time.sleep(_delay)
            _delay *= backoff

            if isinstance(jitter, tuple):
                _delay += random.uniform(*jitter)
            else:
                _delay += jitter

            if max_delay is not None:
                _delay = min(_delay, max_delay)


def retry(func=None, exceptions=Exception, tries=-1, delay=0, max_delay=None,
          backoff=1, jitter=0, logger=logging_logger):
    """
    Returns a retry decorator.

    :param func: the function, if None decorator usage is assumed
    :param exceptions: catch all exceptions, a specific exception,
        or an iterable of exceptions.
    :param tries: the maximum number of attempts.
    :param delay: initial delay between attempts.
    :param max_delay: the maximum value of delay. (None = no limit).
    :param backoff: multiplier applied to delay between attempts.
        (1 = no backoff).
    :param jitter: extra seconds added to delay between attempts.
        (fixed if a number, random if a range tuple (min, max))
    :param logger: logger.warning(fmt, error, delay) will be called on
        failed attempts. If None, logging is disabled.
    :returns: the function return value
    """

    @decorator
    def _wrapper(_func, *args, **kwargs):
        _args = args if args else []
        _kwargs = kwargs if kwargs else {}
        return __retry_internal(partial(_func, *_args, **_kwargs), exceptions, tries,
                                delay, max_delay, backoff, jitter, logger)

    return _wrapper if func is None else _wrapper(func)


def retry_call(func, args=None, kwargs=None, exceptions=Exception, tries=-1,
               delay=0, max_delay=None, backoff=1, jitter=0,
               logger=logging_logger):
    """
    Calls a function and re-executes it if it failed.

    :param func: the function to execute.
    :param args: the positional arguments of the function to execute.
    :param kwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch.
    :param tries: the maximum number of attempts.
    :param delay: initial delay between attempts.
    :param max_delay: the maximum value of delay. (None = no limit).
    :param backoff: multiplier applied to delay between attempts.
        (1 = no backoff).
    :param jitter: extra seconds added to delay between attempts.
        (fixed if a number, random if a range tuple (min, max))
    :param logger: logger.warning(fmt, error, delay) will be called on
        failed attempts. If None, logging is disabled.
    :returns: the function return value
    """
    _args = args if args else []
    _kwargs = kwargs if kwargs else {}
    return __retry_internal(partial(func, *_args, **_kwargs), exceptions, tries,
                            delay, max_delay, backoff, jitter, logger)
