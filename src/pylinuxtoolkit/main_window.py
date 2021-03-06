# PyLinuxToolkit
# Copyright (C) 2022 JWCompDev
#
# MainWindow.py
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

"""
Contains the Ui_MainWindow class and defines all the GUI
base objects.
"""
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from typing import NoReturn

from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow:
    """This class defines all the GUI base objects."""

    def setupUi(self, window) -> NoReturn:  # type: ignore
        """
        This defines all the GUI base objects.

        :param window: the main window
        """
        window.setObjectName("MainWindow")
        window.resize(758, 600)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.tabViewMain = QtWidgets.QTabWidget(self.centralwidget)
        self.tabViewMain.setGeometry(QtCore.QRect(0, 0, 584, 551))
        self.tabViewMain.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabViewMain.setElideMode(QtCore.Qt.ElideNone)
        self.tabViewMain.setObjectName("tabViewMain")
        self.tabGeneralInfo = QtWidgets.QWidget()
        self.tabGeneralInfo.setObjectName("tabGeneralInfo")
        self.tabViewMain.addTab(self.tabGeneralInfo, "")
        self.tabTerminal = QtWidgets.QWidget()
        self.tabTerminal.setObjectName("tabTerminal")
        self.lstOutput = QtWidgets.QListView(self.tabTerminal)
        self.lstOutput.setGeometry(QtCore.QRect(10, 10, 561, 466))
        self.lstOutput.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lstOutput.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lstOutput.setObjectName("lstOutput")
        self.txtCommand = QtWidgets.QLineEdit(self.tabTerminal)
        self.txtCommand.setGeometry(QtCore.QRect(10, 485, 461, 25))
        self.txtCommand.setObjectName("txtCommand")
        self.btnSubmit = QtWidgets.QPushButton(self.tabTerminal)
        self.btnSubmit.setGeometry(QtCore.QRect(481, 485, 89, 25))
        self.btnSubmit.setObjectName("btnSubmit")
        self.tabViewMain.addTab(self.tabTerminal, "")
        self.txtDescription = QtWidgets.QTextEdit(self.centralwidget)
        self.txtDescription.setGeometry(QtCore.QRect(588, 27, 161, 523))
        self.txtDescription.setObjectName("txtDescription")
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 758, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.mnuQuit = QtWidgets.QAction(window)
        self.mnuQuit.setObjectName("mnuQuit")
        self.mnuAbout = QtWidgets.QAction(window)
        self.mnuAbout.setObjectName("mnuAbout")
        self.menuFile.addAction(self.mnuQuit)
        self.menuHelp.addAction(self.mnuAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(window)
        self.tabViewMain.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, MainWindow):
        """
        This re-translates all text on the GUI.

        :param MainWindow: the main window
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Ultimate Linux Toolkit"))
        self.tabViewMain.setTabText(
            self.tabViewMain.indexOf(self.tabGeneralInfo),
            _translate("MainWindow", "General Info"),
        )
        self.btnSubmit.setText(_translate("MainWindow", "Submit"))
        self.tabViewMain.setTabText(
            self.tabViewMain.indexOf(self.tabTerminal),
            _translate("MainWindow", "Terminal"),
        )
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.mnuQuit.setText(_translate("MainWindow", "Quit"))
        self.mnuAbout.setText(_translate("MainWindow", "About"))
