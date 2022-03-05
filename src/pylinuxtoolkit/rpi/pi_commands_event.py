# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# command_event.py
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
Contains the PiCommandsEvent class, an event that is triggered
when a RaspberryPi command is run.
"""
from __future__ import annotations

from typing import Callable, Any

from pystdlib.bash.bash_command import BashCommand
from pystdlib.event import Namespace, Event


class PiCommandsEvent:
    """An event that is triggered when a RaspberryPi command is run."""

    ROOT = Namespace("pi.commands")
    IS_PI0 = Namespace(ROOT.name + ".is_pizero")
    IS_PI1 = Namespace(ROOT.name + ".is_pione")
    IS_PI2 = Namespace(ROOT.name + ".is_pitwo")
    IS_PI4 = Namespace(ROOT.name + ".is_pifour")

    def __init__(self):
        self._root_event = Event(_wildcard=True, command=BashCommand)

        self._on_command = None

    def on_command(self, namespace: Namespace,
                   handler: Callable[[BashCommand], Any] = None, ttl: int = -1):
        """
        Registers a function to the 'new_handler' event.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param namespace: the event namespace to register
        :param handler: the function to add as handler. When *None*,
            decorator usage is assumed. Returns the function.
        :param ttl: the amount of times to listen. Negative values mean
            infinity.
        """
        if handler is not None:
            self._on_command = handler
            self._root_event.on(namespace, self._on_command, ttl)
        else:
            self._root_event.off(namespace, self._on_command)

    def fire(self, namespace: Namespace, **kwargs):
        """
        Fires an *event*. All functions of events that match *event*
        are invoked with *kwargs* in the exact order of
        their registration. Wildcards might be applied.

        :param namespace: the event to fire
        :param kwargs: keyword args to pass to handlers
        """
        self._root_event.fire(namespace, **kwargs)
