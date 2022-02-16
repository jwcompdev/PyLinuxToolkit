# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# CustomQTWorker.py
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
This file contains the CustomQTWorker class, a handler that safely
updates the GUI from another thread.
"""
from typing import NoReturn

from PyQt5 import QtCore

from pylinuxtoolkit.bash.OutputData import OutputData


class CustomQTWorker(QtCore.QObject):
    """
    Handles safely updating the GUI from another thread.
    """

    _on_output_signal = QtCore.pyqtSignal(OutputData, name="on_output")

    def __init__(self):
        super().__init__()

    def set_on_output_function(self, function) -> NoReturn:
        """
        Sets the function that will update the GUI from the GUI thread.

        :param function: the function to run to update
        """

        self._on_output_signal.connect(function)

    def run_on_output_function(self, output_data: OutputData) -> NoReturn:
        """
        Runs the function and passes in the specified data.

        :param output_data: an object containing bash output data
        """

        self._on_output_signal.emit(output_data)
