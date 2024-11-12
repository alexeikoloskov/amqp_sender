# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'macros_edit.ui'
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
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(612, 508)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setStyleSheet(u"#Dialog {\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton {\n"
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
"QPushButton:hover {\n"
"	background-color: rgb(149, 190, 214);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}\n"
"QPushButton:focus {\n"
"	background-color: rgb(75, 180, 240);\n"
"	border: 1px  solid rgb(255, 255, 255);\n"
"	cursor: pointer;\n"
"}\n"
"\n"
"QLineEdit{\n"
"	padding: 5px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}\n"
"QTextEdit{\n"
"	padding: 5px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}\n"
"")
        self.variable = QLineEdit(Dialog)
        self.variable.setObjectName(u"variable")
        self.variable.setGeometry(QRect(10, 40, 591, 31))
        self.code = QTextEdit(Dialog)
        self.code.setObjectName(u"code")
        self.code.setGeometry(QRect(10, 110, 591, 351))
        self.save = QPushButton(Dialog)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(500, 470, 101, 31))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save.setIcon(icon)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 49, 16))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 90, 71, 16))
        self.null_value = QLabel(Dialog)
        self.null_value.setObjectName(u"null_value")
        self.null_value.setGeometry(QRect(460, 10, 141, 20))
        self.null_value.hide()

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Variable</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Python code</span></p></body></html>", None))
        self.null_value.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic; color:#ff0000;\">Fields can not be empty!</span></p></body></html>", None))
    # retranslateUi

