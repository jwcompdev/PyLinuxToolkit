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
Contains the CommandEvent class, an event that is triggered
when a new BashCommand is created.
"""
from typing import Callable, Any

from pystdlib.bash import BashCommand
from pystdlib.event import Event, Namespace


class CommandEvent:
    """An event that is triggered when a new BashCommand is created."""

    NEW_COMMAND = Namespace("command.new")

    def __init__(self):
        self._root_event = Event(_wildcard=True)
        self._new_command_event = Event(_wildcard=True, command=BashCommand)

        self._on_command = None

    def on_new_command(self, handler: Callable[[BashCommand], Any] = None, ttl: int = -1):
        """
        Registers a function to the 'command.new' event.

        NOTE: type hinting on parameters is not required but,
        if used, is enforced to match the event signature.

        :param handler: the function to add as handler
        :param ttl: the amount of times to listen. Negative values mean
            infinity.
        """
        if handler is not None:
            self._on_command = handler
            self._new_command_event.on(self.NEW_COMMAND, self._on_command, ttl)
        else:
            self._new_command_event.off(self.NEW_COMMAND, self._on_command)

    def fire(self, namespace: Namespace, **kwargs):
        """
        Fires an *event*. All functions of events that match *event*
        are invoked with *kwargs* in the exact order of
        their registration. Wildcards might be applied.

        :param namespace: the event to fire
        :param kwargs: keyword args to pass to handlers
        """

        if namespace == self.NEW_COMMAND:
            self._new_command_event.fire(namespace, **kwargs)
        else:
            self._root_event.fire(namespace, **kwargs)
