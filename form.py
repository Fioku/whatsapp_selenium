from PySide6 import QtWidgets
from PySide6.QtCore import QRect, QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QCursor

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(350, 150)
        Widget.setStyleSheet(u"QWidget {\n"
                             "	background-color: #fff;\n"
                             "	border: 1px solid black;\n"
                             "	border-radius: 3px;\n"
                             "  font-weight: 600;\n"
                             "}")
        self.lineEdit = QtWidgets.QLineEdit(Widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(70, 30, 221, 31))
        
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.pushButton = QtWidgets.QPushButton(Widget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(120, 80, 121, 31))
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"App", None))
        self.pushButton.setText(QCoreApplication.translate("Widget", u"Send", None))
