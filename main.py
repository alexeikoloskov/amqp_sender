import json
import os
import uuid

import pika
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMenu, QMessageBox, QDialog, QTreeWidgetItem
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction, QIcon
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor, QFont, QBrush
import sys
import ui_amqpSender as design
from cryptography.fernet import Fernet
from ui_dialog import Ui_Dialog
from ui_save_qm import Ui_Dialog as QM
from ui_input_dialog import Ui_Dialog as InputDialog
import webbrowser
import copy
import re
import random
import string
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
import webbrowser
import traceback
import importlib

import ctypes
myappid = 'akoloskov.amqpsender.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

basedir = os.path.dirname(__file__)

SETTINGS_FILE = "settings.enc"
key = ''
cipher = Fernet(key)


PRESET_FILE = "preset.json"

git_use = False

pattern = r"\$INT-(\d+)\$"


def replace_match(match):
    x = match.group(1)  # Получаем значение X из шаблона
    result = generate_random_int(lenght=int(x))  # Вызываем функцию с этим значением
    return str(result)  # Возвращаем результат в виде строки


def generate_random_string(length=10):
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _+-", k=length))

def generate_random_int(lenght=9,msisdn=False):
    return random.randint(9000000000, 9999999999) if msisdn else random.randint(10 ** (lenght - 1), (10 ** lenght) - 1)

def get_iso_datetime(utc=False):
    if utc:
        now_iso = datetime.now(ZoneInfo("UTC"))
    else:
        now_iso = datetime.now(ZoneInfo("Europe/Moscow"))
    return now_iso.isoformat()

def get_depth(node, data, cache={}):
    if node in cache:
        return cache[node]
    parent = data[node]["parent"]
    if parent is None:
        depth = 0
    else:
        depth = 1 + get_depth(parent, data, cache)
    cache[node] = depth
    return depth


def save_settings(settings):
    # Определение глубины для каждого узла
    depths = {node: get_depth(node, settings) for node in settings}

    # Сортировка узлов по глубине
    sorted_nodes = sorted(settings.keys(), key=lambda x: depths[x])
    sorted_settings = {node: settings[node] for node in sorted_nodes}
    encrypted_data = cipher.encrypt(json.dumps(sorted_settings).encode())
    with open(SETTINGS_FILE, "wb") as f:
        f.write(encrypted_data)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)


def toggleVisibility(ui_dialog):
    try:
        if ui_dialog.password.echoMode() == QLineEdit.Normal:
            ui_dialog.password.setEchoMode(QLineEdit.Password)
            ui_dialog.show_hide_pass.setText('Show')
        else:
            ui_dialog.password.setEchoMode(QLineEdit.Normal)
            ui_dialog.show_hide_pass.setText('Hide')
    finally:
        ui_dialog.show_hide_pass.clearFocus()


def save_preset(preset):
    depths = {node: get_depth(node, preset) for node in preset}

    # Сортировка узлов по глубине
    sorted_nodes = sorted(preset.keys(), key=lambda x: depths[x])
    sorted_preset = {node: preset[node] for node in sorted_nodes}
    with open(PRESET_FILE, "wb") as f:
        f.write(json.dumps(sorted_preset).encode())


def load_preset():
    if not os.path.exists(PRESET_FILE):
        return {}
    with open(PRESET_FILE, "rb") as f:
        data = f.read()
    return json.loads(data)


def check_int(text) -> bool:
    try:
        _ = int(text)
        return True
    except ValueError:
        return False


def check_null_value(text) -> bool:
    if text == '':
        return True
    else:
        return False


def search_tree(widget, text):
    def recursive_search(item):
        # Проверяем текст текущего элемента
        if item.text(0) == text:  # Предполагается, что текст находится в первой колонке
            return True
        # Проходим по всем дочерним элементам
        for i in range(item.childCount()):
            if recursive_search(item.child(i)):
                return True
        return False

    # Проверяем все верхние уровни дерева
    for i in range(widget.topLevelItemCount()):
        if recursive_search(widget.topLevelItem(i)):
            return True
    return False


def find_children(data, element, children = set()):
    for key, value in data.items():
        if value['parent'] == element:
            children.add(key)
            find_children(data, key)
    return children

def create_client_props():
    client_props = {
        'product': 'AMQP Semder',
        'information': 'Sender AMQP message manual'
    }
    return client_props


class SenderApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.json_valid = []

        self.font_tree = QFont()
        self.font_tree.setBold(True)
        self.font_tree.setItalic(True)

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.parent_name = ''
        # Список коннектов
        self.connections = load_settings()
        self.preset = load_preset()

        self.load_tree(self.connections, self.connection_tree)
        self.load_tree(self.preset, self.preset_tree)

        self.connection_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connection_tree.customContextMenuRequested.connect(self.contextMenuEventConnection)
        self.connection_tree.itemDoubleClicked.connect(self.open_ui)
        self.connection_tree.itemClicked.connect(self.set_choose_host)

        self.preset_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.preset_tree.customContextMenuRequested.connect(self.contextMenuEventPreset)
        self.preset_tree.itemDoubleClicked.connect(self.set_preset)

        self.count_yn.stateChanged.connect(self.checkbox_changed)

        self.send.clicked.connect(self.send_message)

        # Создаем главное меню
        help_action = QAction("Справка", self)
        help_action.triggered.connect(self.show_help)

        self.menu.addAction(help_action)

    def show_help(self):
        # Создаем и показываем окно справки
        self.help_window = design.HelpWindow()
        self.help_window.show()

    def load_tree(self, data, tree):
        # Словарь для хранения ссылок на элементы по их именам
        items = {}

        # Создаем элементы дерева
        for key, value in data.items():
            parent_name = value.get("parent")

            # Создаем новый элемент
            item = QTreeWidgetItem([key])

            # Добавляем дополнительные данные (например, params) в элемент

            if value.get("url"):
                item.setText(2, value.get("url"))
                item.setData(2, Qt.UserRole, value.get("url"))

            params = value.get("params")
            if params:
                params_copy = copy.deepcopy(params)
                if tree.objectName() == 'connection_tree':
                    params_copy['password'] = "***"
                else:
                    params_copy['message'] = "***"
                item.setToolTip(0, str(params_copy))
                item.setText(1, "+")

                item.setFont(0, self.font_tree)

            # Если у элемента нет родителя, то это корневой элемент
            if parent_name is None:
                tree.addTopLevelItem(item)
            else:
                # Если есть родитель, добавляем элемент как дочерний к родительскому элементу
                parent_item = items.get(parent_name)
                if parent_item:
                    parent_item.addChild(item)

            # Сохраняем элемент в словарь
            items[key] = item
        tree.expandAll()

    def contextMenuEventConnection(self, position: QPoint):
        # Проверяем, был ли клик на элементе
        clicked_item = self.connection_tree.itemAt(position)
        if clicked_item:
            # Контекстное меню для элемента
            menu = QMenu(self)
            info_action = QAction("Show Info", self)
            add_child_action = QAction("Add chapter", self)
            add_connection_action = QAction("Add connect", self)
            rename_action = QAction("Rename", self)
            delete_action = QAction("Delete", self)

            menu.addAction(info_action)
            info_action.triggered.connect(lambda: self.show_info_connect(clicked_item))

            if clicked_item.text(1) == "+":
                edit_action = QAction("Edit connect", self)
                menu.addAction(edit_action)
                menu.addSeparator()
                edit_action.triggered.connect(lambda: self.edit_connect(clicked_item))

            menu.addAction(add_child_action)
            menu.addAction(add_connection_action)

            add_child_action.triggered.connect(lambda: self.add_chapter_connection(clicked_item))
            add_connection_action.triggered.connect(lambda: self.create_new_con(clicked_item))

            menu.addSeparator()
            menu.addAction(rename_action)
            menu.addAction(delete_action)
            rename_action.triggered.connect(lambda: self.rename_item(clicked_item))
            delete_action.triggered.connect(lambda: self.delete_item_connection(clicked_item))
        else:
            # Контекстное меню для пустой области
            menu = QMenu(self)
            add_action = QAction("Add chapter", self)
            add_connection_action = QAction("Add connect", self)
            menu.addAction(add_action)
            menu.addAction(add_connection_action)
            add_action.triggered.connect(lambda: self.add_chapter_connection(clicked_item))
            add_connection_action.triggered.connect(lambda: self.create_new_con(clicked_item))

            if git_use:
                menu.addSeparator()

                import_action = QAction("Import list connections", self)
                menu.addAction(import_action)
                export_action = QAction("Export list connections", self)
                menu.addAction(export_action)

                import_action.triggered.connect(lambda: print("import"))
                export_action.triggered.connect(lambda: print("export"))

        # Отображаем меню в позиции клика
        menu.exec(self.connection_tree.viewport().mapToGlobal(position))

    def delete_item_connection(self, item):
        index = self.connection_tree.indexOfTopLevelItem(item)

        to_remove = find_children(self.connections, item.text(0))

        if to_remove:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete this item?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        if index != -1:
            self.connection_tree.takeTopLevelItem(index)
        else:
            parent = item.parent()
            if parent:
                parent.takeChild(parent.indexOfChild(item))

        to_remove.add(item.text(0))

        for item in to_remove:
            self.connections.pop(item, None)
        save_settings(self.connections)

    def add_chapter_connection(self, clicked_item):
        dialog = QDialog(self)
        dialog_ui = InputDialog()
        dialog_ui.setupUi(dialog)

        def save():
            if dialog_ui.lineEdit.text() == '':
                dialog_ui.null_value.show()
                dialog_ui.save.clearFocus()
                return
            if dialog_ui.null_value.isVisible():
                dialog_ui.null_value.hide()
            if search_tree(self.connection_tree, dialog_ui.lineEdit.text()):
                QMessageBox.warning(self, "Error", "This name is already in the connection tree.")
                dialog_ui.save.clearFocus()
                return

            if clicked_item:
                item = QTreeWidgetItem(clicked_item)
                item.setText(0, dialog_ui.lineEdit.text())
                # Добавляем дополнительные данные (например, params) в элемент

                self.connections[dialog_ui.lineEdit.text()] = {
                    "parent": clicked_item.text(0),
                    "params": None
                }
                clicked_item.addChild(item)
            else:
                self.parent_name = dialog_ui.lineEdit.text()
                new_item = QTreeWidgetItem(self.connection_tree)
                new_item.setText(0, self.parent_name)

                self.connections[self.parent_name] = {
                    "parent": None,
                    "params": None
                }
                self.connection_tree.addTopLevelItem(new_item)

            save_settings(self.connections)
            dialog.close()
        dialog_ui.save.clicked.connect(save)
        dialog.exec()

    def create_new_con(self, clicked_item):
        if not clicked_item or clicked_item.text(1) != '+':
            dialog = QDialog(self)
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog)
            dialog_ui.show_hide_pass.clicked.connect(lambda: toggleVisibility(dialog_ui))

            def save_connection():
                if search_tree(self.connection_tree, dialog_ui.con_name.text()):
                    QMessageBox.warning(self, "Error", "A connection with this name already exists.")
                    dialog_ui.save.clearFocus()
                    return

                for item in [dialog_ui.con_name, dialog_ui.hostname, dialog_ui.port, dialog_ui.vhost,
                             dialog_ui.username, dialog_ui.password]:
                    if check_null_value(item.text()):
                        dialog_ui.null_value.show()
                        dialog_ui.save.clearFocus()
                        return
                if dialog_ui.null_value.isVisible():
                    dialog_ui.null_value.hide()

                if not check_int(dialog_ui.port.text()):
                    dialog_ui.error_port.show()
                    dialog_ui.save.clearFocus()
                    return
                if dialog_ui.error_port.isVisible():
                    dialog_ui.error_port.hide()

                self.connections[dialog_ui.con_name.text()] = {
                        "parent": clicked_item.text(0) if clicked_item else None,
                        "params": {
                                'host': dialog_ui.hostname.text(),
                                'port': int(dialog_ui.port.text()),
                                'vhost': dialog_ui.vhost.text(),
                                'username': dialog_ui.username.text(),
                                'password': dialog_ui.password.text()
                            }
                }

                new_item = QTreeWidgetItem(clicked_item) if clicked_item else QTreeWidgetItem(self.connection_tree)
                new_item.setText(0, dialog_ui.con_name.text())
                new_item.setText(1, '+')
                params = self.connections[dialog_ui.con_name.text()].get("params")
                if params:
                    params_copy = copy.deepcopy(params)
                    params_copy['password'] = "***"
                    new_item.setToolTip(0, str(params_copy))
                    new_item.setFont(0, self.font_tree)
                clicked_item.addChild(new_item) if clicked_item else self.connection_tree.addTopLevelItem(new_item)
                save_settings(self.connections)

                QMessageBox.information(self, "Save", f"Successfully saved connection - {dialog_ui.con_name.text()}")
                dialog_ui.save.clearFocus()
                dialog.close()

            dialog_ui.save.clicked.connect(save_connection)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "Can not create connection for connection.")

    def rename_item(self, clicked_item):
        dialog = QDialog(self)
        dialog_ui = InputDialog()
        dialog_ui.setupUi(dialog)

        def save():
            if dialog_ui.lineEdit.text() == '':
                dialog_ui.null_value.show()
                dialog_ui.save.clearFocus()
                return
            if dialog_ui.null_value.isVisible():
                dialog_ui.null_value.hide()
            if search_tree(self.connection_tree, dialog_ui.lineEdit.text()):
                QMessageBox.warning(self, "Error", "This name is already in the connection tree.")
                dialog_ui.save.clearFocus()
                return

            old_name = clicked_item.text(0)
            new_name = dialog_ui.lineEdit.text()

            self.connections[new_name] = self.connections.pop(old_name)
            for key in self.connections.keys():
                if self.connections[key]['parent'] == old_name:
                    self.connections[key]['parent'] = new_name

            clicked_item.setText(0, new_name)

            save_settings(self.connections)
            dialog.close()

        dialog_ui.save.clicked.connect(save)
        dialog.exec()

    def edit_connect(self, clicked_item):
        if clicked_item:
            dialog = QDialog(self)
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog)
            info_item = self.connections[clicked_item.text(0)]['params']
            # Заполняем инфо о хосте
            original_name = clicked_item.text(0)
            dialog_ui.con_name.setText(original_name)
            dialog_ui.hostname.setText(info_item['host'])
            dialog_ui.port.setText(str(info_item['port']))
            dialog_ui.vhost.setText(info_item['vhost'])
            dialog_ui.username.setText(info_item['username'])
            dialog_ui.password.setText(info_item['password'])
            dialog_ui.show_hide_pass.clicked.connect(lambda: toggleVisibility(dialog_ui))

            def save_connection():
                modified_name = dialog_ui.con_name.text()
                if search_tree(self.connection_tree, modified_name) and modified_name != original_name:
                    QMessageBox.warning(self, "Error", "A connection with this name already exists.")
                    dialog_ui.save.clearFocus()
                    return

                for each in [dialog_ui.con_name, dialog_ui.hostname, dialog_ui.port, dialog_ui.vhost,
                             dialog_ui.username, dialog_ui.password]:
                    if each.text() == '':
                        QMessageBox.warning(self, "Error", "Value can not be null.")
                        dialog_ui.save.clearFocus()
                        return

                self.connections[modified_name] = {
                    "parent": clicked_item.text(0) if clicked_item else None,
                    "params": {
                        'host': dialog_ui.hostname.text(),
                        'port': int(dialog_ui.port.text()),
                        'vhost': dialog_ui.vhost.text(),
                        'username': dialog_ui.username.text(),
                        'password': dialog_ui.password.text()
                    }
                }
                if modified_name != original_name:
                    self.connections[modified_name] = self.connections.pop(original_name)
                    for key in self.connections.keys():
                        if self.connections[key]['parent'] == original_name:
                            self.connections[key]['parent'] = modified_name

                    clicked_item.setText(0, modified_name)

                save_settings(self.connections)

                QMessageBox.information(self, "Save", f"Successfully saved connection - {modified_name}")
                dialog_ui.save.clearFocus()
                dialog.close()

            dialog_ui.save.clicked.connect(save_connection)
            dialog.exec()

    def show_info_connect(self, clicked_item):
        if clicked_item.text(1) == '+':
            dialog = QDialog(self)
            dialog.setWindowTitle('INFO')
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog)
            info_item = self.connections[clicked_item.text(0)]['params']
            # Заполняем инфо о хосте
            dialog_ui.con_name.setText(clicked_item.text(0))
            dialog_ui.hostname.setText(info_item['host'])
            dialog_ui.port.setText(str(info_item['port']))
            dialog_ui.vhost.setText(info_item['vhost'])
            dialog_ui.username.setText(info_item['username'])
            dialog_ui.password.setText(info_item['password'])

            dialog_ui.show_hide_pass.clicked.connect(lambda: toggleVisibility(dialog_ui))

            for item in [dialog_ui.con_name, dialog_ui.hostname, dialog_ui.port,
                         dialog_ui.vhost, dialog_ui.username, dialog_ui.password]:
                item.setReadOnly(True)

            dialog_ui.save.setDisabled(True)
            dialog.exec()

    def set_choose_host(self, item, column):
        if item.text(1) == '+':
            self.choose_host.setText(item.text(0))
###
###        Preset 
###
    def contextMenuEventPreset(self, position: QPoint):
        # Проверяем, был ли клик на элементе
        clicked_item = self.preset_tree.itemAt(position)
        if clicked_item:
            # Контекстное меню для элемента
            menu = QMenu(self)
            add_child_action = QAction("Add chapter", self)
            add_preset_action = QAction("Add preset", self)
            rename_action = QAction("Rename", self)
            delete_action = QAction("Delete", self)

            menu.addAction(add_child_action)
            menu.addAction(add_preset_action)

            menu.addSeparator()
            menu.addAction(rename_action)
            menu.addAction(delete_action)

            # Связываем действия с функциями
            # rename_action.triggered.connect(lambda: self.rename_item(clicked_item))
            add_preset_action.triggered.connect(lambda: self.save_preset_item(clicked_item))
            delete_action.triggered.connect(lambda: self.delete_item_preset(clicked_item))
            rename_action.triggered.connect(lambda: self.rename_preset(clicked_item))
            add_child_action.triggered.connect(lambda: self.add_chapter_preset(clicked_item))

        else:
            # Контекстное меню для пустой области
            menu = QMenu(self)
            add_action = QAction("Add chapter", self)
            add_preset_action = QAction("Add preset", self)
            menu.addAction(add_action)
            menu.addAction(add_preset_action)
            add_action.triggered.connect(lambda: self.add_chapter_preset(clicked_item))
            add_preset_action.triggered.connect(lambda: self.save_preset_item(clicked_item))

            if git_use:
                menu.addSeparator()

                import_action = QAction("Import list connections", self)
                menu.addAction(import_action)
                export_action = QAction("Export list connections", self)
                menu.addAction(export_action)

                import_action.triggered.connect(lambda: print("import"))
                export_action.triggered.connect(lambda: print("export"))

        # Отображаем меню в позиции клика
        menu.exec(self.preset_tree.viewport().mapToGlobal(position))

    def add_chapter_preset(self, clicked_item):
        if not clicked_item or clicked_item.text(1) != '+':
            dialog = QDialog(self)
            dialog_ui = QM()
            dialog_ui.setupUi(dialog)

            def save():
                if dialog_ui.lineEdit.text() == '':
                    dialog_ui.null_value.show()
                    dialog_ui.save.clearFocus()
                    return
                if dialog_ui.null_value.isVisible():
                    dialog_ui.null_value.hide()
                if search_tree(self.preset_tree, dialog_ui.lineEdit.text()):
                    QMessageBox.warning(self, "Error", "This name is already in the preset tree.")
                    dialog_ui.save.clearFocus()
                    return

                if clicked_item:
                    new_item = QTreeWidgetItem(clicked_item)
                    new_item.setText(0, dialog_ui.lineEdit.text())
                    # Добавляем дополнительные данные (например, params) в элемент

                    self.preset[dialog_ui.lineEdit.text()] = {
                        "parent": clicked_item.text(0),
                        "params": None
                    }
                else:
                    self.parent_name = dialog_ui.lineEdit.text()
                    new_item = QTreeWidgetItem(self.preset_tree)
                    new_item.setText(0, self.parent_name)

                    self.preset[self.parent_name] = {
                        "parent": None,
                        "params": None
                    }

                if dialog_ui.lineEdit_2.text():
                    self.preset[dialog_ui.lineEdit.text()]['url'] = dialog_ui.lineEdit_2.text()
                    new_item.setText(2, dialog_ui.lineEdit_2.text())
                    new_item.setData(2, Qt.UserRole, dialog_ui.lineEdit_2.text())
                clicked_item.addChild(new_item) if clicked_item else self.preset_tree.addTopLevelItem(new_item)
                save_preset(self.preset)
                dialog.close()
            dialog_ui.save.clicked.connect(save)
            dialog.exec()

    def save_preset_item(self, clicked_item):
        if not clicked_item or clicked_item.text(1) != '+':
            dialog = QDialog(self)
            dialog_ui = QM()
            dialog_ui.setupUi(dialog)

            def save():
                preset_name = dialog_ui.lineEdit.text()
                if dialog_ui.lineEdit.text() == '':
                    dialog_ui.null_value.show()
                    dialog_ui.save.clearFocus()
                    return
                if dialog_ui.null_value.isVisible():
                    dialog_ui.null_value.hide()
                if search_tree(self.preset_tree, preset_name):
                    QMessageBox.warning(self, "Error", "A preset with this name already exists.")
                    dialog_ui.save.clearFocus()
                    return
                for item in [self.exchange_entry, self.rk_entry]:
                    if check_null_value(item.text()):
                        self.null_value.show()
                        dialog_ui.save.clearFocus()
                        return
                for item in [self.message_entry, self.headers_entry, self.props_entry]:
                    if check_null_value(item.toPlainText()):
                        self.null_value.show()
                        dialog_ui.save.clearFocus()
                        return
                if self.null_value.isVisible():
                    self.null_value.hide()
                new_item = QTreeWidgetItem(clicked_item) if clicked_item else QTreeWidgetItem(self.preset_tree)
                new_item.setText(0, preset_name)
                new_item.setText(1, "+")

                # Добавляем дополнительные данные (например, params) в элемент

                self.preset[preset_name] = {
                    'parent': clicked_item.text(0) if clicked_item else None,
                    'params': {
                        'exchange_entry': self.exchange_entry.text(),
                        'routing_key': self.rk_entry.text(),
                        'message': self.message_entry.toPlainText(),
                        'headers': self.headers_entry.toPlainText(),
                        'props': self.props_entry.toPlainText()
                    }
                }
                params = self.preset[preset_name].get("params")
                if params:
                    params_copy = copy.deepcopy(params)
                    params_copy['message'] = "***"
                    new_item.setToolTip(0, str(params_copy))
                    new_item.setFont(0, self.font_tree)
                if dialog_ui.lineEdit_2.text():
                    self.preset[dialog_ui.lineEdit.text()]['url'] = dialog_ui.lineEdit_2.text()
                    new_item.setText(2, dialog_ui.lineEdit_2.text())
                    new_item.setData(2, Qt.UserRole, dialog_ui.lineEdit_2.text())
                clicked_item.addChild(new_item) if clicked_item else self.preset_tree.addTopLevelItem(new_item)
                save_preset(self.preset)
                dialog.close()
            dialog_ui.save.clicked.connect(save)
            dialog.exec()

    def delete_item_preset(self, item):
        index = self.preset_tree.indexOfTopLevelItem(item)
        to_remove = find_children(self.preset, item.text(0))

        if to_remove:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                "Are you sure you want to delete this item?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        if index != -1:
            self.preset_tree.takeTopLevelItem(index)
        else:
            parent = item.parent()
            if parent:
                parent.takeChild(parent.indexOfChild(item))

        to_remove.add(item.text(0))

        for item in to_remove:
            self.preset.pop(item, None)
        save_preset(self.preset)

    def rename_preset(self, clicked_item):
        dialog = QDialog(self)
        dialog_ui = QM()
        dialog_ui.setupUi(dialog)

        dialog_ui.lineEdit.setText(clicked_item.text(0))
        dialog_ui.lineEdit_2.setText(clicked_item.text(2))

        old_name = clicked_item.text(0)
        old_url = clicked_item.text(2)

        def save():
            new_name = dialog_ui.lineEdit.text()
            new_url = dialog_ui.lineEdit_2.text()

            if dialog_ui.lineEdit.text() == '':
                dialog_ui.null_value.show()
                dialog_ui.save.clearFocus()
                return
            if dialog_ui.null_value.isVisible():
                dialog_ui.null_value.hide()
            if search_tree(self.preset_tree, new_name) and old_url == new_url:
                QMessageBox.warning(self, "Error", "A preset with this name already exists.")
                dialog_ui.save.clearFocus()
                return
            if self.null_value.isVisible():
                self.null_value.hide()

            self.preset[new_name] = self.preset.pop(old_name)
            self.preset[new_name]['url'] = new_url
            for key in self.preset.keys():
                if self.preset[key]['parent'] == old_name:
                    self.preset[key]['parent'] = new_name

            clicked_item.setText(0, new_name)
            clicked_item.setText(2, new_url)
            clicked_item.setData(2, Qt.UserRole, new_url)

            save_preset(self.preset)
            dialog.close()

        dialog_ui.save.clicked.connect(save)
        dialog.exec()


    def set_preset(self, item, column):
        if column == 0:
            if self.preset[item.text(0)].get("params"):
                preset = self.preset[item.text(0)]['params']
                self.exchange_entry.setText(preset['exchange_entry'])
                self.rk_entry.setText(preset['routing_key'])
                self.message_entry.setText(preset['message'])
                self.headers_entry.setText(preset['headers'])
                self.props_entry.setText(preset['props'])
        elif column == 2:
            url = item.data(2, Qt.UserRole)
            if url:
                webbrowser.open(url)

    def checkbox_changed(self, state):
        if not check_int(self.count.text()):
            self.error_count.show()
            self.count_yn.blockSignals(True)
            self.count_yn.setCheckState(Qt.CheckState.Checked)
            self.count_yn.blockSignals(False)
            return
        
        if self.error_count.isVisible():
            self.error_count.hide()
        
        if state == 2:
            self.count.setReadOnly(False)
            # print("чекбокс установлен")
        elif state == 0:
            self.count.setReadOnly(True)
            # print("чекбокс снят")

    def validate_json(self, text, entry):
        # Сбрасываем форматирование перед проверкой
        self.reset_formatting(entry)
        try:
            json.loads(self.prepare_json(text))
            self.send.clearFocus()
            return True
        except json.decoder.JSONDecodeError as e:
            # Подсвечиваем ошибочную позицию
            line, column = e.lineno, e.colno
            absolute_position = self.get_absolute_position(text, line, column)
            self.highlight_error(absolute_position, entry)
            self.json_valid.append(f'{entry.objectName()}: \n {e} \n\n')
            self.send.clearFocus()
            return False

    def highlight_error(self, pos, entry):
        for position in range(pos-1, pos+1):
            cursor = entry.textCursor()
            cursor.setPosition(position)

            format_e = QTextCharFormat()
            format_e.setBackground(QColor("yellow"))  # Цвет подсветки

            cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format_e)

    def reset_formatting(self, entry):
        cursor = entry.textCursor()
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(QTextCharFormat())

    def get_absolute_position(self, text, line, column):
        """Преобразует номер строки и столбца в абсолютный индекс."""
        lines = text.splitlines()
        absolute_position = sum(len(lines[i]) + 1 for i in range(line - 1)) + (column - 1)
        return absolute_position

    def open_ui(self, item):
        if item.text(1) == '+':
            webbrowser.open(f'http://{self.connections[item.text(0)]["params"]["host"]}:15672')
    
    def process_item(self,item):
        values = {
                "$UUID$": str(uuid.uuid4()),
                "$STR$": generate_random_string(),
                "$DATE$": str(date.today()),
                "$DATE_TIME$": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "$ISO_UTC$": str(get_iso_datetime(utc=True)),
                "$ISO$": str(get_iso_datetime())
            }

        # Замена значений в текущем объекте
        for key, value in item.items():
            if isinstance(value, dict):
                self.process_item(value)
            if isinstance(value, list):
                value = [self.process_item(item) for item in value]
            if isinstance(value, str):  # Проверяем, что значение — строка
                for placeholder, replacement in values.items():
                    value = value.replace(placeholder, replacement)
                # Применяем регулярные выражения, если нужно
                item[key] = value
        return item

    def prepare_json(self, json_string):

        data = re.sub(r'\$INT-(\d+)\$', replace_match, json_string)
        data = json.loads(re.sub(r'\$MSISDN\$', str(generate_random_int(msisdn=True)), data))

        if isinstance(data, list):
            data = [self.process_item(item) for item in data]
        elif isinstance(data, dict):
            data = self.process_item(data)
        return json.dumps(data, indent=4)
    

    def send_message(self):
        self.json_valid.clear()
        for item in [self.choose_host, self.exchange_entry, self.rk_entry, self.message_entry, self.headers_entry]:
            try:
                if check_null_value(item.text()):
                    self.null_value.show()
                    self.send.clearFocus()
                    return
            except AttributeError:
                if check_null_value(item.toPlainText()):
                    self.null_value.show()
                    self.send.clearFocus()
                    return
        if self.null_value.isVisible():
            self.null_value.hide()

        if not check_int(self.count.text()):
            self.error_count.show()
            self.send.clearFocus()
            return
        if self.error_count.isVisible():
            self.error_count.hide()

        self.progressBar.setMaximum(int(self.count.text()))

        conn_params = self.connections[self.choose_host.text()]['params']
        
        properties_valid = True

        if self.props_entry.toPlainText():
            properties_valid = self.validate_json(self.props_entry.toPlainText(), self.props_entry)


        message_valid = self.validate_json(self.message_entry.toPlainText(), self.message_entry)
        headers_valid = self.validate_json(self.headers_entry.toPlainText(), self.headers_entry)
        
        if False in [message_valid,properties_valid,headers_valid]: 
            warn_message = ''.join(str(x) for x in self.json_valid)
            QMessageBox.warning(self, 'Ошибка', f'Некорректный JSON: \n\n {str(warn_message)}')
            return
        else:
            self.json_valid.clear()
        

        if self.props_entry.toPlainText():
            prop = json.loads(self.prepare_json(self.props_entry.toPlainText()))
        else:
            prop = dict()
        heads = json.loads(self.prepare_json(self.headers_entry.toPlainText()))

        try:
            props = pika.BasicProperties(
                content_type=prop.get('content_type'),
                priority=prop.get('priority'),
                reply_to=prop.get('replyTo'),
                message_id=prop.get('messageId'),
                type=prop.get('type'),
                headers=heads
            )

            credentials = pika.PlainCredentials(
                conn_params['username'],
                conn_params['password']
            )

            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = conn_params['host'],
                port=int(conn_params['port']),
                virtual_host=conn_params['vhost'],
                credentials=credentials,
                client_properties=create_client_props()
            ))

            channel = connection.channel()

            for _ in range(int(self.count.text())):
                channel.basic_publish(
                    exchange=self.exchange_entry.text(),
                    routing_key=self.rk_entry.text(),
                    body=self.prepare_json(self.message_entry.toPlainText()),
                    properties=props
                )

                value = self.progressBar.value()
                if value < self.progressBar.maximum():
                    self.progressBar.setValue(value + 1)
                else:
                    break
            connection.close()
            QMessageBox.information(self, "Success", f"Successfully send {self.count.text()} message.")
            self.send.clearFocus()
        
        except Exception as e:
            self.send.clearFocus()
            self.show_traceback()

    def show_traceback(self):
        # Получение информации об ошибке
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        # Отображение в QMessageBox
        QMessageBox.critical(self, "Error", tb_text)


def main():
    if '_PYI_SPLASH_IPC' in os.environ and importlib.util.find_spec("pyi_splash"):
        import pyi_splash
        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir,'amqp_sender_icon.ico')))
    window = SenderApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
