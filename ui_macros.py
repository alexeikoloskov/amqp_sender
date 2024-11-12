# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'macros.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QListWidget, QListWidgetItem,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(461, 541)
        Dialog.setStyleSheet(u"#Dialog {\n"
"	background-color: rgb(255, 255, 255);\n"
"}\n"
"QListWidget{\n"
"	padding: 5px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setGeometry(QRect(10, 10, 441, 521))
        self.listWidget.setMinimumSize(QSize(441, 521))
        self.listWidget.setMaximumSize(QSize(441, 521))
        self.listWidget.setSortingEnabled(True)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
    # retranslateUi

