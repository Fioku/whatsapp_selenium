from PySide6 import QtWidgets
from PySide6.QtCore import QRect, QCoreApplication, QMetaObject, Qt
from PySide6.QtGui import QCursor, QPixmap, QPalette, QBrush
import os
import glob

class UI_Send_To_All(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(250, 350)
        Widget.setStyleSheet(u"#Widget {\n"
                                "	background-color: #fffff2;\n"
                                "   border: 1px solid #6ec007;\n"
                                "   border-radius: 3px;\n"
                                "   font-weight: 600;\n"
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

        self.selectAll = QtWidgets.QCheckBox(Widget)
        self.selectAll.setObjectName(u"selectAll")
        self.selectAll.setGeometry(QRect(15, 3, 15, 15))
        self.selectAll.setStyleSheet(u"#selectAll {\n"
                                     "  background-color: transparent;\n"
                                     "	border: 1px solid #C7C8CC;\n"
                                     "   border-radius: 3px;\n"
                                     "}")
        self.selectAllLabel = QtWidgets.QLabel(Widget)
        self.selectAllLabel.setObjectName(u"selectAllLabel")
        self.selectAllLabel.setGeometry(QRect(100, 2, 100, 15))
        self.selectAllLabel.setStyleSheet(u"#selectAllLabel {\n"
                                     "  color: #000;\n"
                                     "  font-weight: 600;\n"
                                     "}")

        self.scroll_area = QtWidgets.QScrollArea(parent=self.Widget)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setStyleSheet(u"#scroll_area{\n"
                                        "	background-color: transparent;\n"
                                        "   border: 1px solid #C7C8CC;\n"
                                        "   border-radius: 3px;\n"
                                        "   font-weight: 600;\n"
                                        "}")
        self.scroll_area.setGeometry(QRect(5, 20, 240, 290))

        self.number_table = QtWidgets.QWidget(parent=self.scroll_area)

        self.number_table_layout = QtWidgets.QVBoxLayout()
        self.number_table.setLayout(self.number_table_layout)

        self.scroll_area.setWidget(self.number_table)

        self.number_table_layout.setAlignment(Qt.AlignTop)
        self.number_table.setObjectName("number_table")
        self.number_table.setStyleSheet("background-color: transparent;")

        self.sendButton = QtWidgets.QPushButton(Widget)
        self.sendButton.setObjectName(u"sendButton")
        self.sendButton.setStyleSheet(u"#sendButton {\n"
                                    "	background-color: #6ec007;\n"
                                    "   color: #fffff2;\n"
                                    "   border-radius: 3px;\n"
                                    "   font-weight: 600;\n"
                                    "}")
        self.sendButton.setGeometry(QRect(70, 315, 121, 31))
        self.sendButton.setCursor(QCursor(Qt.PointingHandCursor))

        self.retranslateUi(Widget)
        QMetaObject.connectSlotsByName(Widget)
    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Send To All", None))
        self.selectAllLabel.setText(QCoreApplication.translate("Widget", u"Select All", None))
        self.sendButton.setText(QCoreApplication.translate("Widget", u"Send To All", None))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    main_window = QtWidgets.QWidget()
    ui = UI_Send_To_All()
    ui.setupUi(main_window)
    
    main_window.show()
    sys.exit(app.exec())