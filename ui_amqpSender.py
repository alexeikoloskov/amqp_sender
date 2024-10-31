# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'amqpSender.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QProgressBar,
    QPushButton, QSizePolicy, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1050, 860)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(1050, 860))
        MainWindow.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        MainWindow.setStyleSheet(u"#centralwidget {\n"
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
"QTreeWidget{\n"
"	padding: 5px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}\n"
"QInputDialog{\n"
"	padding: 5px;\n"
"	background-color: rgb(255, 255, 255);\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"}\n"
# "QTreeWidget::item {\n"
# "                border: 1px solid;\n"
# "            }\n"
# "            QTreeView::branch {\n"
# "                background-color: transparent;\n"
# "                border: 1px solid;\n"
# "            }\n"
                        "QProgressBar{\n"
"	padding: 3px;\n"
"	border: 1px solid ;\n"
"	color: rgb(0, 0, 0);\n"
"   	border-radius: 7px;\n"
"    text-align: center;\n"
"}")
        MainWindow.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(430, 80, 91, 16))
        self.exchange_entry = QLineEdit(self.centralwidget)
        self.exchange_entry.setObjectName(u"exchange_entry")
        self.exchange_entry.setGeometry(QRect(430, 100, 281, 31))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(430, 280, 81, 16))
        self.message_entry = QLineEdit(self.centralwidget)
        self.message_entry.setObjectName(u"message_entry")
        self.message_entry.setGeometry(QRect(430, 300, 591, 501))
        self.message_entry.setCursorPosition(0)
        self.message_entry.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(430, 20, 81, 16))
        self.choose_host = QLineEdit(self.centralwidget)
        self.choose_host.setObjectName(u"choose_host")
        self.choose_host.setGeometry(QRect(430, 40, 281, 31))
        self.choose_host.setReadOnly(True)
        self.count_yn = QCheckBox(self.centralwidget)
        self.count_yn.setObjectName(u"count_yn")
        self.count_yn.setGeometry(QRect(765, 18, 16, 21))
        self.count = QLineEdit(self.centralwidget)
        self.count.setObjectName(u"count")
        self.count.setGeometry(QRect(730, 40, 161, 31))
        self.count.setAutoFillBackground(False)
        self.count.setReadOnly(False)
        self.send = QPushButton(self.centralwidget)
        self.send.setObjectName(u"send")
        self.send.setGeometry(QRect(830, 810, 191, 31))
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend))
        self.send.setIcon(icon1)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(730, 20, 41, 16))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(900, 40, 118, 31))
        font = QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.progressBar.setFont(font)
        self.progressBar.setValue(0)
        self.null_value = QLabel(self.centralwidget)
        self.null_value.setObjectName(u"null_value")
        self.null_value.setGeometry(QRect(880, 10, 161, 16))
        self.error_count = QLabel(self.centralwidget)
        self.error_count.setObjectName(u"error_count")
        self.error_count.setEnabled(True)
        self.error_count.setGeometry(QRect(780, 20, 111, 16))
        font1 = QFont()
        font1.setBold(True)
        font1.setItalic(True)
        font1.setUnderline(True)
        self.error_count.setFont(font1)
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(730, 80, 71, 16))
        self.rk_entry = QLineEdit(self.centralwidget)
        self.rk_entry.setObjectName(u"rk_entry")
        self.rk_entry.setGeometry(QRect(730, 100, 291, 31))
        self.preset_tree = QTreeWidget(self.centralwidget)
        self.preset_tree.setObjectName(u"preset_tree")
        self.preset_tree.setGeometry(QRect(10, 300, 371, 501))
        self.preset_tree.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.preset_tree.setColumnCount(0)
        self.connection_tree = QTreeWidget(self.centralwidget)
        self.connection_tree.setObjectName(u"connection_tree")
        self.connection_tree.setGeometry(QRect(10, 10, 371, 281))
        self.connection_tree.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.connection_tree.setColumnCount(1)
        self.connection_tree.setHeaderLabels(["Name"])
        self.headers_entry = QTextEdit(self.centralwidget)
        self.headers_entry.setObjectName(u"headers_entry")
        self.headers_entry.setGeometry(QRect(430, 160, 281, 111))
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(430, 140, 51, 16))
        self.props_entry = QTextEdit(self.centralwidget)
        self.props_entry.setObjectName(u"props_entry")
        self.props_entry.setGeometry(QRect(730, 160, 291, 111))
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(730, 140, 61, 16))
        self.save_preset_button = QPushButton(self.centralwidget)
        self.save_preset_button.setObjectName(u"save_preset_button")
        self.save_preset_button.setGeometry(QRect(430, 810, 111, 31))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave))
        self.save_preset_button.setIcon(icon)
        self.null_value.hide()
        self.error_count.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.save_preset_button.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Exchange name</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Message</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Choose host</span></p></body></html>", None))
        self.count_yn.setText("")
        self.send.setText(QCoreApplication.translate("MainWindow", u"Send", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Count</span></p></body></html>", None))
        self.null_value.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic; text-decoration: underline; color:#ff0000;\">The value can not be empty</span></p></body></html>", None))
        self.error_count.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ff0000;\">must be an integer</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Routing key</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Headers</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; font-style:italic;\">Properties</span></p></body></html>", None))
    # retranslateUi

