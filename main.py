import json
import os
import pika
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem,QLineEdit, QMenu, QMessageBox,QDialog
from PySide6.QtCore import Qt, QPoint
import sys
import ui_amqpSender as design
from cryptography.fernet import Fernet
from ui_dialog import Ui_Dialog
from ui_save_qm import Ui_Dialog as QM

SETTINGS_FILE = "settings.enc"
PRESET_FILE = "preset.json"

key = '<insert your key>'
cipher = Fernet(key)


def save_settings(settings):
    encrypted_data = cipher.encrypt(json.dumps(settings).encode())
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
    with open(PRESET_FILE, "wb") as f:
        f.write(json.dumps(preset).encode())


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


class SenderApp(QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()

        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.name_preset = ''
        # Список коннектов
        self.connections = load_settings()
        self.preset = load_preset()
        self.list_connection = ['Create new connection'] + (list(self.connections.keys()) if self.connections else ["There are no connections"])
        for con in self.list_connection:
            if con == 'Create new connection':
                item = QListWidgetItem(con)
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                self.list_con.addItem(item)
            else:
                self.list_con.addItem(con)

        # Список пресетов
        self.list_presets = (list(self.preset.keys()) if self.preset else ["There are no presets"])
        for preset in self.list_presets:
            self.list_preset.addItem(preset)

        # Заполнение выбранного хоста
        self.list_con.itemDoubleClicked.connect(lambda x: self.set_choose_host(x))
        # self.edit_con_button.clicked.connect(self.on_click)

        # Создание и реагирование на меню правой кнопкой мыши в list_con
        self.list_con.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_con.customContextMenuRequested.connect(self.show_context_menu)

        # Создание и реагирование на меню правой кнопкой мыши в list_preset
        self.list_preset.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_preset.customContextMenuRequested.connect(self.show_context_menu_preset)

        self.save_preset_button.clicked.connect(self.save_preset)

        self.count_yn.stateChanged.connect(self.checkbox_changed)

        self.send.clicked.connect(self.send_message)

        # Заполнение пресета
        self.list_preset.itemDoubleClicked.connect(lambda x: self.set_preset(x))

    def set_choose_host(self, host):
        text = host.text()
        if text == 'Create new connection':
            self.create_new_con()
        elif text == 'There are no connections':
            pass
        else:
            self.choose_host.setText(text)

    def checkbox_changed(self, state):
        if state == 2:
            self.count.setReadOnly(False)
            # print("чекбокс установлен")
        elif state == 0:
            self.count.setReadOnly(True)
            # print("чекбокс снят")

    def set_preset(self, preset_name):
        if preset_name.text() != 'There are no presets':
            preset = self.preset[preset_name.text()]
            self.choose_host.setText(preset['host'])
            self.exchange_entry.setText(preset['exchange_entry'])
            self.rk_entry.setText(preset['routing_key'])
            self.message_entry.setText(preset['message'])

    def save_preset(self):
        self.get_name_preset()

        for item in [self.choose_host, self.exchange_entry, self.rk_entry, self.message_entry]:
            if check_null_value(item.text()):
                self.null_value.show()
                self.save_preset_button.clearFocus()
                return
        if self.null_value.isVisible():
            self.null_value.hide()

        self.preset[self.name_preset] = {
            'host':  self.choose_host.text(),
            'exchange_entry': self.exchange_entry.text(),
            'routing_key': self.rk_entry.text(),
            'message': self.message_entry.text()
        }
        self.list_preset.addItem(self.name_preset)
        save_preset(self.preset)

        if self.list_preset.item(0).text() == 'There are no presets':
            self.list_preset.takeItem(0)

        QMessageBox.information(self, "Save", f"Successfully saved preset - {self.name_preset}")

        self.save_preset_button.clearFocus()

    def get_name_preset(self):
        self.name_preset = ''
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

            if self.name_preset in self.list_presets:
                QMessageBox.warning(self, "Error", "This name is already in the list of presets.")
                dialog_ui.save.clearFocus()
                return

            self.name_preset = dialog_ui.lineEdit.text()
            dialog.close()

        dialog_ui.save.clicked.connect(save)
        dialog.exec()

    def create_new_con(self):
        dialog = QDialog(self)
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog)
        dialog_ui.show_hide_pass.clicked.connect(lambda: toggleVisibility(dialog_ui))

        def save_connection():
            if dialog_ui.con_name.text() in self.connections:
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
                'host': dialog_ui.hostname.text(),
                'port': int(dialog_ui.port.text()),
                'vhost': dialog_ui.vhost.text(),
                'username': dialog_ui.username.text(),
                'password': dialog_ui.password.text()
            }
            self.list_con.addItem(dialog_ui.con_name.text())
            save_settings(self.connections)

            if self.list_con.item(1).text() == 'There are no connections':
                self.list_con.takeItem(1)

            QMessageBox.information(self, "Save", f"Successfully saved connection - {dialog_ui.con_name.text()}")
            dialog_ui.save.clearFocus()
            dialog.close()

        dialog_ui.save.clicked.connect(save_connection)
        dialog.exec()

    def show_context_menu_preset(self, position: QPoint):
        # Создаем меню
        menu = QMenu()
        delete_action = menu.addAction("Delete")

        # Показываем меню в позиции курсора
        action = menu.exec(self.list_preset.mapToGlobal(position))

        # Обработка выбранного действия
        if action == delete_action:
            self.delete_item_preset()

    def delete_item_preset(self):
        item = self.list_preset.currentItem()
        if item.text() in self.preset:
            del self.preset[item.text()]
            save_preset(self.preset)
            self.list_preset.takeItem(self.list_preset.currentRow())
            QMessageBox.information(self, "Success", f"Preset {item.text()} deleted.")
        else:
            QMessageBox.information(self, "Error", f"Preset {item.text()} is not exist.")

    def show_context_menu(self, position: QPoint):
        # Создаем меню
        menu = QMenu()

        # Добавляем действия в меню
        info_action = menu.addAction("Info")
        menu.addSeparator()  # Разделитель
        edit_action = menu.addAction("Edit")
        menu.addSeparator()  # Разделитель
        delete_action = menu.addAction("Delete")

        # Показываем меню в позиции курсора
        action = menu.exec(self.list_con.mapToGlobal(position))

        # Обработка выбранного действия
        if action == edit_action and self.list_con.currentItem().text() != 'Create new connection':
            self.edit_action()
        elif action == delete_action and self.list_con.currentItem().text() != 'Create new connection':
            self.delete_item()
        elif action == info_action and self.list_con.currentItem().text() != 'Create new connection':
            self.show_info()

    def edit_action(self):
        item = self.list_con.currentItem()

        if item:
            dialog = QDialog(self)
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog)
            info_item = self.connections[item.text()]
            # Заполняем инфо о хосте
            original_name = item.text()
            dialog_ui.con_name.setText(original_name)
            dialog_ui.hostname.setText(info_item['host'])
            dialog_ui.port.setText(str(info_item['port']))
            dialog_ui.vhost.setText(info_item['vhost'])
            dialog_ui.username.setText(info_item['username'])
            dialog_ui.password.setText(info_item['password'])
            dialog_ui.show_hide_pass.clicked.connect(lambda: toggleVisibility(dialog_ui))

            def save_connection():
                modified_name = dialog_ui.con_name.text()
                if modified_name in self.connections and modified_name != original_name:
                    QMessageBox.warning(self, "Error", "A connection with this name already exists.")
                    dialog_ui.save.clearFocus()
                    return

                for each in [dialog_ui.con_name, dialog_ui.hostname, dialog_ui.port, dialog_ui.vhost,
                             dialog_ui.username, dialog_ui.password]:
                    if each.text() == '':
                        QMessageBox.warning(self, "Error", "Необходимо заполнить все поля.")
                        dialog_ui.save.clearFocus()
                        return

                self.connections[modified_name] = {
                    'host': dialog_ui.hostname.text(),
                    'port': int(dialog_ui.port.text()),
                    'vhost': dialog_ui.vhost.text(),
                    'username': dialog_ui.username.text(),
                    'password': dialog_ui.password.text()
                }
                if modified_name != original_name:
                    del self.connections[original_name]
                    self.list_con.takeItem(self.list_con.currentRow())
                    self.list_con.addItem(modified_name)
                save_settings(self.connections)

                QMessageBox.information(self, "Save", f"Successfully saved connection - {modified_name}")
                dialog_ui.save.clearFocus()
                dialog.close()

            dialog_ui.save.clicked.connect(save_connection)
            dialog.exec()

    def delete_item(self):
        item = self.list_con.currentItem()
        if item.text() in self.connections:
            del self.connections[item.text()]
            save_settings(self.connections)
            self.list_con.takeItem(self.list_con.currentRow())
            QMessageBox.information(self, "Success", f"Connection {item.text()} deleted.")
        else:
            QMessageBox.warning(self, "Error", f"Connection {item.text()} is not exist.")

    def show_info(self):
        item = self.list_con.currentItem()
        if item:
            dialog = QDialog(self)
            dialog.setWindowTitle('INFO')
            dialog_ui = Ui_Dialog()
            dialog_ui.setupUi(dialog)
            info_item = self.connections[item.text()]
            # Заполняем инфо о хосте
            dialog_ui.con_name.setText(item.text())
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

    def send_message(self):
        message = self.message_entry.text()
        exchange_name = self.exchange_entry.text()
        rk = self.rk_entry.text()
        conn_params = self.connections[self.choose_host.text()]

        for item in [self.choose_host, self.exchange_entry, self.message_entry]:
            if check_null_value(item.text()):
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

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=conn_params['host'],
                port=conn_params['port'],
                credentials=pika.PlainCredentials(conn_params['username'], conn_params['password'])
            ))
            channel = connection.channel()

            for _ in range(int(self.count.text())):
                channel.basic_publish(exchange=exchange_name,
                                      routing_key=rk,
                                      body=message)

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
            QMessageBox.critical(self, "Critical", f"The message could not be sent {e}")


def main():
    app = QApplication(sys.argv)
    window = SenderApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
