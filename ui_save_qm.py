from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtWidgets import (QLabel, QLineEdit, QPushButton)
from PySide6.QtGui import (QIcon)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(411, 112)
        Dialog.setStyleSheet(u"QDialog{\n"
"background-color: rgb(255, 255, 255);\n"
"}\n"
"#save {\n"
"	background-color: rgb(223, 237, 245);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"	border-radius: 7px;\n"
"    padding: 1px 7px 2px;\n"
"    text-rendering: auto;\n"
"    color: initial;\n"
"    text-align: start;\n"
"    margin: 0em;\n"
"    font: 400 11px system-ui;\n"
"}\n"
"#save:hover {\n"
"	background-color: rgb(149, 190, 214);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}\n"
"#save:focus {\n"
"	background-color: rgb(75, 180, 240);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}\n"
"QLineEdit{\n"
"	padding: 5px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}")

        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 30, 371, 31))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 10, 71, 16))
        self.null_value = QLabel(Dialog)
        self.null_value.setObjectName(u"null_value")
        self.null_value.setGeometry(QRect(260, 10, 141, 16))
        self.null_value.hide()
        self.save = QPushButton(Dialog)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(294, 70, 101, 24))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save.setIcon(icon)
        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Preset name", None))
        self.save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Name preset</span></p></body></html>", None))
        self.null_value.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic; text-decoration: underline; color:#ff0000;\">Name can not be empty!</span></p></body></html>", None))
