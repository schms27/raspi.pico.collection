# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_config_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1026, 821)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/makro_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(3.0)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1011, 701))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_layout = QtWidgets.QWidget()
        self.tab_layout.setObjectName("tab_layout")
        self.layoutWidget = QtWidgets.QWidget(self.tab_layout)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 80, 621, 581))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_0 = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_0.sizePolicy().hasHeightForWidth())
        self.pushButton_0.setSizePolicy(sizePolicy)
        self.pushButton_0.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_0.setObjectName("pushButton_0")
        self.gridLayout_2.addWidget(self.pushButton_0, 0, 0, 1, 1)
        self.pushButton_1 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_1.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_1.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_2.addWidget(self.pushButton_1, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_3.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_4.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 1, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_5.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_6.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 1, 2, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 1, 3, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_2.addWidget(self.pushButton_8, 2, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_9.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_2.addWidget(self.pushButton_9, 2, 1, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_10.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_10.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_2.addWidget(self.pushButton_10, 2, 2, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_11.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_11.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_2.addWidget(self.pushButton_11, 2, 3, 1, 1)
        self.pushButton_12 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_12.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_12.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_12.setObjectName("pushButton_12")
        self.gridLayout_2.addWidget(self.pushButton_12, 3, 0, 1, 1)
        self.pushButton_13 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_13.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_13.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_13.setObjectName("pushButton_13")
        self.gridLayout_2.addWidget(self.pushButton_13, 3, 1, 1, 1)
        self.pushButton_14 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_14.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_14.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_14.setObjectName("pushButton_14")
        self.gridLayout_2.addWidget(self.pushButton_14, 3, 2, 1, 1)
        self.pushButton_15 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_15.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton_15.setMaximumSize(QtCore.QSize(100, 100))
        self.pushButton_15.setObjectName("pushButton_15")
        self.gridLayout_2.addWidget(self.pushButton_15, 3, 3, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab_layout)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 621, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_prev_layout = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_prev_layout.sizePolicy().hasHeightForWidth())
        self.pushButton_prev_layout.setSizePolicy(sizePolicy)
        self.pushButton_prev_layout.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_prev_layout.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_prev_layout.setObjectName("pushButton_prev_layout")
        self.horizontalLayout_2.addWidget(self.pushButton_prev_layout)
        self.lineEdit_layout_name = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lineEdit_layout_name.setFont(font)
        self.lineEdit_layout_name.setObjectName("lineEdit_layout_name")
        self.horizontalLayout_2.addWidget(self.lineEdit_layout_name)
        self.pushButton_next_layout = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_next_layout.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_next_layout.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_next_layout.setObjectName("pushButton_next_layout")
        self.horizontalLayout_2.addWidget(self.pushButton_next_layout)
        self.pushButton_new_layout = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_new_layout.setMaximumSize(QtCore.QSize(50, 30))
        self.pushButton_new_layout.setObjectName("pushButton_new_layout")
        self.horizontalLayout_2.addWidget(self.pushButton_new_layout)
        self.pushButton_del_layout = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_del_layout.setMaximumSize(QtCore.QSize(70, 30))
        self.pushButton_del_layout.setObjectName("pushButton_del_layout")
        self.horizontalLayout_2.addWidget(self.pushButton_del_layout)
        self.tabWidget.addTab(self.tab_layout, "")
        self.tab_general_settings = QtWidgets.QWidget()
        self.tab_general_settings.setObjectName("tab_general_settings")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_general_settings)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1001, 661))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.com_port_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.com_port_comboBox.setObjectName("com_port_comboBox")
        self.verticalLayout.addWidget(self.com_port_comboBox)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.password_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.horizontalLayout_3.addWidget(self.password_lineEdit)
        self.label_icon_password_set = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_icon_password_set.setText("")
        self.label_icon_password_set.setObjectName("label_icon_password_set")
        self.horizontalLayout_3.addWidget(self.label_icon_password_set)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.sound_device_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.sound_device_comboBox.setObjectName("sound_device_comboBox")
        self.verticalLayout.addWidget(self.sound_device_comboBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_5.addWidget(self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 2, 1, 1)
        self.tabWidget.addTab(self.tab_general_settings, "")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(780, 720, 235, 36))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.reset_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.reset_pushButton.setObjectName("reset_pushButton")
        self.horizontalLayout.addWidget(self.reset_pushButton)
        self.save_pushButton = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_pushButton.sizePolicy().hasHeightForWidth())
        self.save_pushButton.setSizePolicy(sizePolicy)
        self.save_pushButton.setObjectName("save_pushButton")
        self.horizontalLayout.addWidget(self.save_pushButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1026, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton_new_layout.clicked.connect(MainWindow.onNewLayoutButtonClicked)
        self.pushButton_prev_layout.clicked.connect(MainWindow.onPrevLayoutButtonClicked)
        self.pushButton_next_layout.clicked.connect(MainWindow.onNextLayoutButtonClicked)
        self.reset_pushButton.clicked.connect(MainWindow.onResetButtonClicked)
        self.save_pushButton.clicked.connect(MainWindow.onSaveButtonClicked)
        self.pushButton_del_layout.clicked.connect(MainWindow.onDeleteLayoutButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MacroPad Configuration"))
        self.pushButton_0.setText(_translate("MainWindow", "0"))
        self.pushButton_1.setText(_translate("MainWindow", "1"))
        self.pushButton_2.setText(_translate("MainWindow", "2"))
        self.pushButton_3.setText(_translate("MainWindow", "3"))
        self.pushButton_4.setText(_translate("MainWindow", "4"))
        self.pushButton_5.setText(_translate("MainWindow", "5"))
        self.pushButton_6.setText(_translate("MainWindow", "6"))
        self.pushButton_7.setText(_translate("MainWindow", "7"))
        self.pushButton_8.setText(_translate("MainWindow", "8"))
        self.pushButton_9.setText(_translate("MainWindow", "9"))
        self.pushButton_10.setText(_translate("MainWindow", "10"))
        self.pushButton_11.setText(_translate("MainWindow", "11"))
        self.pushButton_12.setText(_translate("MainWindow", "12"))
        self.pushButton_13.setText(_translate("MainWindow", "13"))
        self.pushButton_14.setText(_translate("MainWindow", "14"))
        self.pushButton_15.setText(_translate("MainWindow", "15"))
        self.pushButton_prev_layout.setText(_translate("MainWindow", "<"))
        self.pushButton_next_layout.setText(_translate("MainWindow", ">"))
        self.pushButton_new_layout.setText(_translate("MainWindow", "New"))
        self.pushButton_del_layout.setText(_translate("MainWindow", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_layout), _translate("MainWindow", "Layout"))
        self.label.setText(_translate("MainWindow", "COM-Port"))
        self.label_2.setText(_translate("MainWindow", "Password (Unlock Sensitive Data)"))
        self.label_3.setText(_translate("MainWindow", "Sound Device (Soundboard Playback)"))
        self.label_4.setText(_translate("MainWindow", "placeholder column 2 ... ... ... .... ... ... ..."))
        self.label_6.setText(_translate("MainWindow", "placeholder column 3 .... ... ... ... ... ... .."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_general_settings), _translate("MainWindow", "General Settings"))
        self.reset_pushButton.setText(_translate("MainWindow", "Reset Device"))
        self.save_pushButton.setText(_translate("MainWindow", "Save"))
from . import resources_rc
