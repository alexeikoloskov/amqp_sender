import json
import os
import uuid

import pika
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QMenu, QMessageBox, QDialog, QTreeWidgetItem
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QAction
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
from datetime import date, datetime
import webbrowser


SETTINGS_FILE = "settings.enc"
PRESET_FILE = "preset.json"

key = '***'
cipher = Fernet(key)

git_use = False
pattern = r"\$INT-(\d+)\$"

def replace_match(match):
    x = match.group(1)  # Получаем значение X из шаблона
    result = generate_random_int(lenght=int(x))  # Вызываем функцию с этим значением
    return str(result)  # Возвращаем результат в виде строки


def generate_random_string():
    """
    Генерирует случайную строку случайной длины (от 10 до 30 символов).

    :return: Случайная строка
    """
    length = random.randint(10, 30)
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k=length))
    return random_string


def generate_random_int(lenght=9, msisdn=False):
    """
        Генерирует случайное число определённой длины.

        :return: Случайное число
        """
    range_start = 10 ** (lenght - 1)
    range_end = (10 ** lenght) - 1
    if msisdn:
        return '9'+str(random.randint(range_start, range_end))
    else:

        return random.randint(range_start, range_end)


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


def find_children(data, element):
    children = set()
    for key, value in data.items():
        if value['parent'] == element:
            children.add(key)
            find_children(data, key)
    return children


class SenderApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

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

    def set_choose_host(self, item, column):
        if item.text(1) == '+':
            self.choose_host.setText(item.text(0))

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
            delete_action.triggered.connect(lambda: print("delete"))
            rename_action.triggered.connect(lambda: print("rename"))
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
                    QMessageBox.warning(self, "Error", "This name is already in the connection tree.")
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
                for item in [self.choose_host, self.exchange_entry, self.rk_entry]:
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
                        'host': self.choose_host.text(),
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

    def set_preset(self, item, column):
        if column == 0:
            if self.preset[item.text(0)].get("params"):
                preset = self.preset[item.text(0)]['params']
                if self.connections.get(item.text(0)):
                    self.choose_host.setText(preset['host'])
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
            json.loads(text)
            self.send.clearFocus()
            return True
        except json.JSONDecodeError as e:
            # Подсвечиваем ошибочную позицию
            line, column = e.lineno, e.colno
            absolute_position = self.get_absolute_position(text, line, column)
            self.highlight_error(absolute_position, entry)
            QMessageBox.warning(self, 'Ошибка', f'Некорректный JSON: {e}')
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
            print(self.connections[item.text(0)]["params"]["host"])
            webbrowser.open(f'http://{self.connections[item.text(0)]["params"]["host"]}:15672')

    def send_message(self):
        message = self.message_entry.toPlainText()

        message = message.replace('$UUID$', str(uuid.uuid4()))
        message = message.replace('$STR$', str(generate_random_string()))
        message = message.replace('$MSISDN$', str(generate_random_int(msisdn=True)))
        message = message.replace('$DATE$', str(date.today()))
        message = message.replace('$DATE_TIME$', str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        message = re.sub(pattern, replace_match, message)

        print(message)

        if not self.validate_json(message, self.message_entry):
            return

        json_message = json.loads(message)

        # for key, value in json_message.items():
        #     for macro_name in macros:
        #         if f"${macro_name}$" in value:
        #             result = macros[macro_name].process_macro(value)
        #             json_message[key] = value.replace(f"${macro_name}$", str(result))

        print(json_message)

def main():
    app = QApplication(sys.argv)
    window = SenderApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
