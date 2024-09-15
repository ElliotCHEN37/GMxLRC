# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(637, 602)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Token_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Token_lab.setFont(font)
        self.Token_lab.setObjectName("Token_lab")
        self.gridLayout.addWidget(self.Token_lab, 9, 0, 1, 1)
        self.bfs_chk = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.bfs_chk.setFont(font)
        self.bfs_chk.setAccessibleDescription("")
        self.bfs_chk.setObjectName("bfs_chk")
        self.gridLayout.addWidget(self.bfs_chk, 5, 0, 1, 2)
        self.Token_in = QtWidgets.QLineEdit(self.centralwidget)
        self.Token_in.setObjectName("Token_in")
        self.gridLayout.addWidget(self.Token_in, 9, 1, 1, 1)
        self.info = QtWidgets.QTextEdit(self.centralwidget)
        self.info.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("JetBrains Mono Light")
        font.setPointSize(9)
        self.info.setFont(font)
        self.info.setStyleSheet("")
        self.info.setReadOnly(True)
        self.info.setObjectName("info")
        self.gridLayout.addWidget(self.info, 10, 0, 1, 2)
        self.Output_in = QtWidgets.QLineEdit(self.centralwidget)
        self.Output_in.setObjectName("Output_in")
        self.gridLayout.addWidget(self.Output_in, 1, 1, 1, 1)
        self.Quiet_chk = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Quiet_chk.setFont(font)
        self.Quiet_chk.setAccessibleDescription("")
        self.Quiet_chk.setObjectName("Quiet_chk")
        self.gridLayout.addWidget(self.Quiet_chk, 7, 0, 1, 2)
        self.bfs_des = QtWidgets.QLabel(self.centralwidget)
        self.bfs_des.setObjectName("bfs_des")
        self.gridLayout.addWidget(self.bfs_des, 6, 0, 1, 2)
        self.Quiet_des = QtWidgets.QLabel(self.centralwidget)
        self.Quiet_des.setObjectName("Quiet_des")
        self.gridLayout.addWidget(self.Quiet_des, 8, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 11, 0, 1, 2)
        self.Update_chk = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Update_chk.setFont(font)
        self.Update_chk.setAccessibleDescription("")
        self.Update_chk.setObjectName("Update_chk")
        self.gridLayout.addWidget(self.Update_chk, 3, 0, 1, 2)
        self.Output_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Output_lab.setFont(font)
        self.Output_lab.setObjectName("Output_lab")
        self.gridLayout.addWidget(self.Output_lab, 1, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.Sleep_lab = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Sleep_lab.setFont(font)
        self.Sleep_lab.setObjectName("Sleep_lab")
        self.Sleep_in = QtWidgets.QLineEdit(self.splitter_2)
        self.Sleep_in.setObjectName("Sleep_in")
        self.Depth_lab = QtWidgets.QLabel(self.splitter_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Depth_lab.setFont(font)
        self.Depth_lab.setObjectName("Depth_lab")
        self.Depth_in = QtWidgets.QLineEdit(self.splitter_2)
        self.Depth_in.setObjectName("Depth_in")
        self.gridLayout.addWidget(self.splitter_2, 2, 0, 1, 2)
        self.Update_des = QtWidgets.QLabel(self.centralwidget)
        self.Update_des.setObjectName("Update_des")
        self.gridLayout.addWidget(self.Update_des, 4, 0, 1, 2)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Artist_lab = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Artist_lab.setFont(font)
        self.Artist_lab.setObjectName("Artist_lab")
        self.Artist_in = QtWidgets.QLineEdit(self.splitter)
        self.Artist_in.setObjectName("Artist_in")
        self.Title_lab = QtWidgets.QLabel(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.Title_lab.setFont(font)
        self.Title_lab.setObjectName("Title_lab")
        self.Title_in = QtWidgets.QLineEdit(self.splitter)
        self.Title_in.setText("")
        self.Title_in.setObjectName("Title_in")
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 637, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuAction = QtWidgets.QMenu(self.menuBar)
        self.menuAction.setObjectName("menuAction")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen_Folder = QtWidgets.QAction(MainWindow)
        self.actionOpen_Folder.setObjectName("actionOpen_Folder")
        self.actionOpen_File = QtWidgets.QAction(MainWindow)
        self.actionOpen_File.setObjectName("actionOpen_File")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionUpdate = QtWidgets.QAction(MainWindow)
        self.actionUpdate.setObjectName("actionUpdate")
        self.actionBd = QtWidgets.QAction(MainWindow)
        self.actionBd.setObjectName("actionBd")
        self.actionLicense = QtWidgets.QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.actionChangelog = QtWidgets.QAction(MainWindow)
        self.actionChangelog.setObjectName("actionChangelog")
        self.actionDarkT = QtWidgets.QAction(MainWindow)
        self.actionDarkT.setObjectName("actionDarkT")
        self.actionSaveConfig = QtWidgets.QAction(MainWindow)
        self.actionSaveConfig.setObjectName("actionSaveConfig")
        self.menuFile.addAction(self.actionExit)
        self.menuAction.addAction(self.actionOpen_Folder)
        self.menuAction.addAction(self.actionBd)
        self.menuAction.addAction(self.actionOpen_File)
        self.menuAction.addAction(self.actionSaveConfig)
        self.menuAction.addAction(self.actionDarkT)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionChangelog)
        self.menuAbout.addAction(self.actionUpdate)
        self.menuAbout.addAction(self.actionLicense)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuAction.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GMxLRC"))
        self.Token_lab.setText(_translate("MainWindow", "*Token:"))
        self.bfs_chk.setText(_translate("MainWindow", "Breadth-first Search"))
        self.Token_in.setPlaceholderText(_translate("MainWindow", "Musximatch User Token"))
        self.info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'JetBrains Mono Light\',\'Arial\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:6px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono 54\',\'JetBrains Mono Light\'; font-size:7pt;\">GMxLRC v1.5 by ElliotCHEN37</span></p>\n"
"<p style=\" margin-top:6px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono 54\',\'JetBrains Mono Light\'; font-size:7pt;\">* Means REQUIRED</span></p>\n"
"<p style=\" margin-top:6px; margin-bottom:6px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'JetBrains Mono 54\',\'JetBrains Mono Light\'; font-size:7pt;\">&gt;&gt;Output Window</span></p></body></html>"))
        self.Output_in.setText(_translate("MainWindow", "lyrics"))
        self.Output_in.setPlaceholderText(_translate("MainWindow", "Output directory, default: lyrics"))
        self.Quiet_chk.setText(_translate("MainWindow", "Quiet Mode"))
        self.bfs_des.setText(_translate("MainWindow", "ⓘ use breadth first search for scanning directory (Only Effect Directory Mode)"))
        self.Quiet_des.setText(_translate("MainWindow", "ⓘ This will hide console output and debug information"))
        self.pushButton.setText(_translate("MainWindow", "Start"))
        self.Update_chk.setText(_translate("MainWindow", "Update Mode"))
        self.Output_lab.setText(_translate("MainWindow", "Output:"))
        self.Sleep_lab.setText(_translate("MainWindow", "Sleep:"))
        self.Sleep_in.setText(_translate("MainWindow", "30"))
        self.Sleep_in.setPlaceholderText(_translate("MainWindow", "Sleep time between requests, default: 30 (second)"))
        self.Depth_lab.setText(_translate("MainWindow", "Depth:"))
        self.Depth_in.setText(_translate("MainWindow", "100"))
        self.Depth_in.setPlaceholderText(_translate("MainWindow", "Max recursion depth, default: 100 (Only Effect Directory Mode)"))
        self.Update_des.setText(_translate("MainWindow", "ⓘ This will overwrite existing .lrc files (Only Effect Directory Mode)"))
        self.Artist_lab.setText(_translate("MainWindow", "*Artist:"))
        self.Artist_in.setPlaceholderText(_translate("MainWindow", "Artist Name (One at a time)"))
        self.Title_lab.setText(_translate("MainWindow", "*Title:"))
        self.Title_in.setPlaceholderText(_translate("MainWindow", "Song Title (One at a time)"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAction.setTitle(_translate("MainWindow", "Action"))
        self.menuAbout.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Alt+F4"))
        self.actionOpen_Folder.setText(_translate("MainWindow", "Directory Mode"))
        self.actionOpen_Folder.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionOpen_File.setText(_translate("MainWindow", "Open Audio File"))
        self.actionOpen_File.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Alt+A"))
        self.actionUpdate.setText(_translate("MainWindow", "Check for Update"))
        self.actionUpdate.setShortcut(_translate("MainWindow", "Ctrl+U"))
        self.actionBd.setText(_translate("MainWindow", "Open Song List"))
        self.actionBd.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.actionLicense.setText(_translate("MainWindow", "License"))
        self.actionLicense.setShortcut(_translate("MainWindow", "Alt+L"))
        self.action1.setText(_translate("MainWindow", "1"))
        self.actionChangelog.setText(_translate("MainWindow", "Changelog"))
        self.actionChangelog.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.actionDarkT.setText(_translate("MainWindow", "Toggle Theme"))
        self.actionDarkT.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionSaveConfig.setText(_translate("MainWindow", "Save Config"))
        self.actionSaveConfig.setShortcut(_translate("MainWindow", "Ctrl+S"))
import resource_rc
