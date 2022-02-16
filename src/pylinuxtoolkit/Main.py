# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# Main.py
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
This file contains the Window class and the main entrypoint of the GUI program.
"""
import atexit
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAbstractItemView

from pylinuxtoolkit.Main_Window import Ui_MainWindow
from pylinuxtoolkit.bash.LinuxBash import LinuxBash
from pylinuxtoolkit.bash.OutputData import OutputData


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


# noinspection PyPep8Naming
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.connect_signal_slots()
        self.lstOutput_model = QtGui.QStandardItemModel()
        self.lstOutput.setModel(self.lstOutput_model)

        self.bash = LinuxBash(
            directory="~",
            output_function=self.on_output,
            remote_ssh=True,
            print_ssh_connection_msgs=True,
            print_prompt=True,
        )
        self.bash.set_ssh_login_info(
            hostname="raspberrypi.local", username="pi", password="jwcompdev", port=22
        )
        self.bash.enable_threaded_worker()
        self.bash.enable_wait_for_locks()
        # self.bash.enable_raise_error_on_lock_wait()

        atexit.register(self.exit_handler)

        if self.bash.is_remote:
            self.bash.ssh_connect(print_ssh_login_success=True, print_prompt=True)
        elif self.bash.is_print_prompt_enabled():
            self.bash.print_prompt()

    def connect_signal_slots(self):
        self.mnuQuit.triggered.connect(self.close)
        self.mnuAbout.triggered.connect(self.about)
        self.btnSubmit.clicked.connect(self.btnSubmit_clicked)
        self.txtCommand.returnPressed.connect(self.txtCommand_return_pressed)

    def about(self):
        QMessageBox.about(
            self,
            "About Ultimate Linux Toolkit",
            "A program to make tasks in linux easier.",
        )

    def print_to_lst(self, text: str):
        self.lstOutput_model.appendRow(QtGui.QStandardItem(text))
        # Scrolls the listview to the bottom
        index = self.lstOutput_model.index(self.lstOutput_model.rowCount() - 1, 0)
        self.lstOutput.scrollTo(index, QAbstractItemView.PositionAtBottom)

    def exit_handler(self):
        self.bash.ssh_close()

    def on_output(self, output_data: OutputData):
        try:
            line = output_data.current_line

            self.print_to_lst(line.get())
            print(">> " + repr(line))

            if "[Y/n]" in line:
                if (
                    "apt upgrade" in output_data.current_command
                    or "apt-get upgrade" in output_data.current_command
                ):
                    output_data.client.sendline("n")
                    print(">> Canceled upgrade!")
        except Exception as e:
            raise e

    def txtCommand_return_pressed(self):
        self.btnSubmit_clicked()

    def btnSubmit_clicked(self):
        if self.txtCommand.text() != "":
            command = self.txtCommand.text().strip()
            self.txtCommand.setText("")

            if command.lower() == "exit":
                self.bash.ssh_close()
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
