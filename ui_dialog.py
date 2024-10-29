# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(622, 218)
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
"}\n"
"#show_hide_pass{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"	border-radius: 7px;\n"
"    padding: 1px 7px 2px;\n"
"    text-rendering: auto;\n"
"    color: initial;\n"
"    text-align: start;\n"
"    margin: 0"
                        "em;\n"
"    font: 400 11px system-ui;\n"
"}\n"
"#show_hide_pass:hover {\n"
"	background-color: rgb(200, 200, 200);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}\n"
"#show_hide_pass:focus {\n"
"	background-color: rgb(140, 140, 140);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 80, 61, 16))
        font = QFont()
        font.setBold(True)
        font.setItalic(True)
        self.label.setFont(font)
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(130, 150, 61, 16))
        self.label_2.setFont(font)
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(310, 80, 61, 16))
        self.label_3.setFont(font)
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(310, 150, 61, 16))
        self.label_4.setFont(font)
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 150, 61, 16))
        self.label_5.setFont(font)
        self.hostname = QLineEdit(Dialog)
        self.hostname.setObjectName(u"hostname")
        self.hostname.setGeometry(QRect(20, 100, 271, 31))
        self.port = QLineEdit(Dialog)
        self.port.setObjectName(u"port")
        self.port.setGeometry(QRect(130, 170, 161, 31))
        self.port.setEchoMode(QLineEdit.EchoMode.Normal)
        self.vhost = QLineEdit(Dialog)
        self.vhost.setObjectName(u"vhost")
        self.vhost.setGeometry(QRect(20, 170, 101, 31))
        self.username = QLineEdit(Dialog)
        self.username.setObjectName(u"username")
        self.username.setGeometry(QRect(310, 100, 291, 31))
        self.password = QLineEdit(Dialog)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(310, 170, 231, 31))
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.save = QPushButton(Dialog)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(510, 30, 91, 31))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save.setIcon(icon)
        self.error_port = QLabel(Dialog)
        self.error_port.setObjectName(u"error_port")
        self.error_port.setEnabled(True)
        self.error_port.setGeometry(QRect(180, 150, 111, 16))
        self.error_port.hide()
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(True)
        self.error_port.setFont(font1)
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(20, 10, 81, 16))
        self.label_7.setFont(font)
        self.con_name = QLineEdit(Dialog)
        self.con_name.setObjectName(u"con_name")
        self.con_name.setGeometry(QRect(20, 30, 471, 31))
        self.show_hide_pass = QPushButton(Dialog)
        self.show_hide_pass.setObjectName(u"show_hide_pass")
        self.show_hide_pass.setGeometry(QRect(550, 170, 51, 31))
        self.null_value = QLabel(Dialog)
        self.null_value.setObjectName(u"null_value")
        self.null_value.setEnabled(True)
        self.null_value.setGeometry(QRect(470, 0, 141, 20))
        self.null_value.setFont(font1)
        self.null_value.hide()

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Connection", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"hostname", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"port", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"username", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"password", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"vhost", None))
        self.save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.error_port.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#ff0000;\">must be an integer</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"connect name", None))
        self.show_hide_pass.setText(QCoreApplication.translate("Dialog", u"Show", None))
        self.null_value.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" color:#ff0000;\">Values can not be empty!</span></p></body></html>", None))
    # retranslateUi

