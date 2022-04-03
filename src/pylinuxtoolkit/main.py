# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# main.py
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
Contains the Window class and the main entrypoint
of the GUI program.
"""
import atexit
import logging
import sys
from time import sleep
from typing import NoReturn

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAbstractItemView

from pystdlib.bash.linux_bash import LinuxBash
from pystdlib.bash.output import OutputData
from pystdlib.log_manager import LogManager
from pylinuxtoolkit.main_window import Ui_MainWindow
from pylinuxtoolkit.rpi.settings import SettingMonitor


def main() -> NoReturn:
    """This is the main entry point for this program."""
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


# noinspection PyPep8Naming
class Window(QMainWindow, Ui_MainWindow):
    """This is the main GUI window class for this application."""

    def __init__(self, parent=None):
        """
        Initializes the window object.

        :param parent: the QWidget parent object
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.connect_signal_slots()
        self.lstOutput_model = QtGui.QStandardItemModel()
        self.lstOutput.setModel(self.lstOutput_model)

        LogManager().enable_logging(logging.DEBUG)

        self.bash = LinuxBash(
            directory="~",
            output_function=self.on_output,
            remote_ssh=True,
            print_ssh_connection_msgs=True,
            print_prompt=True,
        )
        self.bash.set_ssh_login_info(
            hostname="raspberrypi.local",
            username="pi",
            password="jwcompdev",
            port=22
        )
        self.bash.enable_threaded_worker()
        self.bash.enable_wait_for_locks()
        # self.bash.enable_raise_error_on_lock_wait()

        atexit.register(self.exit_handler)

        commands = self.bash.get_past_commands()

        self.monitor = SettingMonitor(commands)
        self.monitor.start_monitoring()

        if self.bash.is_remote:
            self.bash.ssh_connect(print_ssh_login_success=True, print_prompt=True)
        elif self.bash.is_print_prompt_enabled():
            self.bash.print_prompt()

    def connect_signal_slots(self) -> NoReturn:
        """
        This method connects all the GUI items to their
        signal triggers.
        """
        self.mnuQuit.triggered.connect(self.close)
        self.mnuAbout.triggered.connect(self.mnuAbout_clicked)
        self.btnSubmit.clicked.connect(self.btnSubmit_clicked)
        self.txtCommand.returnPressed.connect(self.txtCommand_return_pressed)

    def mnuAbout_clicked(self) -> NoReturn:
        """Opens the 'about' dialog."""
        QMessageBox.about(
            self,
            "About Ultimate Linux Toolkit",
            "A program to make tasks in linux administration easier.",
        )

    def print_to_lst(self, text: str) -> NoReturn:
        """
        Prints the specified text to the GUI terminal and stdout.

        :param text: the text to print
        """
        self.lstOutput_model.appendRow(QtGui.QStandardItem(text))
        # Scrolls the listview to the bottom
        index = self.lstOutput_model.index(self.lstOutput_model.rowCount() - 1, 0)
        self.lstOutput.scrollTo(index, QAbstractItemView.PositionAtBottom)

    def exit_handler(self) -> NoReturn:
        """This runs when the program exits."""
        self.bash.ssh_close()

    def on_output(self, output_data: OutputData) -> NoReturn:
        """
        This function is run each time the output writer is written to.

        :param output_data: the output data
        """
        try:
            line = output_data.current_line

            self.print_to_lst(line.get())

            if "[Y/n]" in line and (
                "apt upgrade" in output_data.current_command
                or "apt-get upgrade" in output_data.current_command
            ):
                output_data.client.sendline("n")
                print(">> Canceled upgrade!")
        except Exception as ex:
            raise ex

    def txtCommand_return_pressed(self) -> NoReturn:
        """
        This runs when the enter key is pressed inside the
        txtCommand text box.
        """
        self.btnSubmit_clicked()

    def btnSubmit_clicked(self) -> NoReturn:
        """This runs when the btnSubmit button is clicked."""
        if self.txtCommand.text() != "":
            command = self.txtCommand.text().strip()
            self.txtCommand.setText("")

            if command.lower() == "exit":
                self.bash.ssh_close()
            elif command.lower().startswith("mon "):
                if command.lower() in ("mon -print", "mon -p"):
                    if command.lower() == "mon -p":
                        self.bash.get_output_writer().write_bypass("mon -p")
                    else:
                        self.bash.get_output_writer().write_bypass("mon -print")
                    self.monitor.request_processed_list()
                    self.bash.get_output_writer().write_bypass("Printed to console!")
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())
                elif command.lower() == "mon -start":
                    self.bash.get_output_writer().write_bypass("mon -start")
                    self.monitor.start_monitoring()
                    self.bash.get_output_writer().write_bypass("Monitoring Started!")
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())
                elif command.lower() == "mon -stop":
                    self.bash.get_output_writer().write_bypass("mon -stop")
                    self.monitor.request_termination()
                    self.bash.get_output_writer().write_bypass("Monitoring Stopped!")
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())
                elif command.lower() in ("mon -restart", "mon -r"):
                    if command.lower() == "mon -r":
                        self.bash.get_output_writer().write_bypass("mon -r")
                    else:
                        self.bash.get_output_writer().write_bypass("mon -restart")
                    self.bash.get_output_writer().write_bypass("Monitoring Restarting!")
                    self.monitor.request_termination()
                    while self.monitor.is_running():
                        sleep(0.09)
                    self.monitor.start_monitoring()
                    self.bash.get_output_writer().write_bypass("Monitoring Restarted!")
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())
                elif command.lower() == "mon -help":
                    self.bash.get_output_writer().write_bypass("mon -help")
                    self.bash.get_output_writer().write_bypass("Usage: mon [OPTION]")
                    self.bash.get_output_writer().write_bypass(
                        "Monitor the PyLinuxToolkit past "
                        "commands to update the GUI."
                    )
                    self.bash.get_output_writer().write_bypass(
                        "This is not a real program on the system "
                        "and will not run on"
                    )
                    self.bash.get_output_writer().write_bypass(
                        "the command line. "
                        "This is a simulated command."
                    )
                    self.bash.get_output_writer().write_bypass("\n")
                    self.bash.get_output_writer().write_bypass(
                        "  -p, -print                 "
                        "Prints the processed list."
                    )
                    self.bash.get_output_writer().write_bypass(
                        "  -start                     "
                        "Starts the monitor."
                    )
                    self.bash.get_output_writer().write_bypass(
                        "  -r, -restart               "
                        "Restarts the monitor."
                    )
                    self.bash.get_output_writer().write_bypass(
                        "  -help                     "
                        "Prints this info screen."
                    )
                    self.bash.get_output_writer().write_bypass("\n")
                    self.bash.get_output_writer().write_bypass(
                        "This MON has Super Cow Powers."
                    )
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())

                    # """
                    # Usage: mon [OPTION]
                    # Monitor the PyLinuxToolkit past commands to update the GUI.
                    # This is not a real program on the system and will not run on the
                    # command line. This is a simulated command.
                    #
                    #     -p, -print                Prints the processed list.
                    #     -start                    Starts the monitor.
                    #     -stop                     Stops the monitor.
                    #     -r, -restart              Restarts the monitor.
                    #     --help                    Prints this info screen.
                    #
                    #                             This MON has Super Cow Powers.
                    # """
                else:
                    self.bash.get_output_writer().write_bypass(
                        "mon: invalid option "
                        f"-- '{command.lower().removeprefix('mon -')}'"
                    )
                    self.bash.get_output_writer().write_bypass(
                        "Try 'mon -help' for more information."
                    )
                    self.bash.get_output_writer().write_bypass(self.bash.get_prompt())
            else:
                self.bash.run_terminal_command(
                    command=command,
                    print_prompt=True,
                    print_command=True,
                    print_exit_code=False,
                    timeout=None,
                )

                # bash.run_terminal_command(command="sudo apt upgrade",
                #                           print_prompt=True,
                #                           print_command=True,
                #                           reconnect_ssh_if_closed=True,
                #                           create_temp_connection_if_closed=False
                #                           )

                # bash.run_terminal_command(command="sudo apt-get --just-print upgrade",
                #                           print_prompt=True,
                #                           print_command=True,
                #                           reconnect_ssh_if_closed=True,
                #                           create_temp_connection_if_closed=False
                #                           )


if __name__ == "__main__":
    main()
