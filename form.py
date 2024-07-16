from PySide6 import QtWidgets
from PySide6.QtCore import QRect, QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QCursor, QPixmap, QPalette, QBrush
import os
import glob

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(350, 180)
        Widget.setStyleSheet(u"#Widget {\n"
                                "	background-color: #EFF396;\n"
                                "    border: 1px solid black;\n"
                                "    border-radius: 3px;\n"
                                "    font-weight: 600;\n"
                                "}")

        root_path = os.path.dirname(os.path.abspath(__file__))
        cover_files = glob.glob(os.path.join(root_path, 'cover.*'))

        if cover_files:
            cover_file = cover_files[0].replace('\\', '/')
            pixmap = QPixmap(cover_file)
            palette = Widget.palette()
            palette.setBrush(QPalette.Window, QBrush(pixmap))
            Widget.setPalette(palette)

        self.Widget = Widget
        
        self.key = QtWidgets.QLineEdit(Widget)
        self.key.setObjectName(u"key")
        self.key.setGeometry(QRect(70, 50, 221, 31))
        self.key.setAlignment(Qt.AlignCenter)
        self.key.setEchoMode(QtWidgets.QLineEdit.Password)
        self.key.setStyleSheet(u"#key {\n"
                            "	background-color: #EFF396;\n"
                            "    border: 1px solid black;\n"
                            "    border-radius: 3px;\n"
                            "    font-weight: 600;\n"
                            "}")
        
        self.login_button = QtWidgets.QPushButton(Widget)
        self.login_button.setObjectName(u"login_button")
        self.login_button.setStyleSheet(u"#login_button {\n"
                                    "	background-color: #74E291;\n"
                                    "	border: 1px solid black;\n"
                                    "    border-radius: 3px;\n"
                                    "    font-weight: 600;\n"
                                    "}")
        
        self.login_button.setGeometry(QRect(118, 100, 121, 31))
        self.login_button.setCursor(QCursor(Qt.PointingHandCursor))
        
        self.lineEdit1 = QtWidgets.QLineEdit(Widget)
        self.lineEdit1.setObjectName(u"lineEdit1")
        self.lineEdit1.setGeometry(QRect(70, 30, 221, 31))
        self.lineEdit1.setAlignment(Qt.AlignCenter)
        self.lineEdit1.setStyleSheet(u"#lineEdit1 {\n"
                            "	background-color: #EFF396;\n"
                            "    border: 1px solid black;\n"
                            "    border-radius: 3px;\n"
                            "    font-weight: 600;\n"
                            "}")
        self.lineEdit1.hide()
        
        self.lineEdit2 = QtWidgets.QLineEdit(Widget)
        self.lineEdit2.setObjectName(u"lineEdit2")
        self.lineEdit2.setGeometry(QRect(70, 80, 221, 31))
        self.lineEdit2.setAlignment(Qt.AlignCenter)
        self.lineEdit2.setStyleSheet(u"#lineEdit2 {\n"
                            "	background-color: #EFF396;\n"
                            "    border: 1px solid black;\n"
                            "    border-radius: 3px;\n"
                            "    font-weight: 600;\n"
                            "}")
        self.lineEdit2.hide()

        self.is_active = QtWidgets.QCheckBox(Widget)
        self.is_active.setObjectName(u"is_active")
        self.is_active.setGeometry(QRect(300, 88, 15, 15))
        self.is_active.setStyleSheet(u"#is_active {\n"
                                     "	border: none;\n"
                                     "}")
        self.is_active.hide()

        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
                                    "	background-color: #74E291;\n"
                                    "	border: 1px solid black;\n"
                                    "    border-radius: 3px;\n"
                                    "    font-weight: 600;\n"
                                    "}")
        self.pushButton.setGeometry(QRect(120, 130, 121, 31))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.hide()

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Save Paper", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Send", None))
        self.login_button.setText(QCoreApplication.translate("Widget", u"Login", None))
