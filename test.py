from PySide6.QtWidgets import QTextEdit, QMenu, QDialog, QListWidgetItem
from PySide6.QtGui import QAction
from PySide6.QtCore import QPoint, Qt
from ui_macros import Ui_Dialog as macros_ui
from ui_macros_edit import Ui_Dialog as macros_edit
import json
import os
import importlib.util

MACROS_FILE = "macros.json"
macros = {}

def save_macros(macros):
    with open(MACROS_FILE, "wb") as f:
        f.write(json.dumps(macros).encode())


def load_macros():
    if not os.path.exists(MACROS_FILE):
        return {}
    with open(MACROS_FILE, "rb") as f:
        data = f.read()
    return json.loads(data)





def check_null_value(text) -> bool:
    if text == '':
        return True
    else:
        return False


class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.macros = load_macros()
        self.list_macros = (list(self.macros.keys()))

    def contextMenuEvent(self, event):
        # Получаем стандартное контекстное меню
        context_menu = self.createStandardContextMenu()

        # Добавляем новое действие в меню
        custom_action = QAction("Edit macros", self)
        custom_action.triggered.connect(self.custom_action_triggered)
        context_menu.addAction(custom_action)

        # Показываем обновленное меню
        context_menu.exec(event.globalPos())

    def custom_action_triggered(self):
        dialog = QDialog(self)
        dialog_ui = macros_ui()
        dialog_ui.setupUi(dialog)

        for one_macros in self.list_macros:
            item = QListWidgetItem(one_macros)
            item.setToolTip(self.macros.get(one_macros, "empty"))
            dialog_ui.listWidget.addItem(item)

        dialog_ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        dialog_ui.listWidget.customContextMenuRequested.connect(lambda x: self.contextMenuEventMacros(x, dialog_ui))

        dialog.exec()

    def contextMenuEventMacros(self, position: QPoint, dialog):
        clicked_item = dialog.listWidget.itemAt(position)
        if clicked_item:
            # Контекстное меню для элемента
            menu = QMenu(self)
            edit_action = QAction("Edit macros", self)
            delete_action = QAction("Delete macros", self)

            menu.addAction(edit_action)
            menu.addAction(delete_action)

            edit_action.triggered.connect(lambda: self.edit_macros(clicked_item, dialog))
            delete_action.triggered.connect(lambda: self.delete_macros(clicked_item, dialog))
        else:
            # Контекстное меню для пустой области
            menu = QMenu(self)
            add_action = QAction("Add new macros", self)
            menu.addAction(add_action)

            menu.addSeparator()

            import_action = QAction("Import list connections", self)
            menu.addAction(import_action)
            export_action = QAction("Export list connections", self)
            menu.addAction(export_action)

            add_action.triggered.connect(lambda: self.add_new_macros(dialog))
        # Отображаем меню в позиции клика
        menu.exec(dialog.listWidget.viewport().mapToGlobal(position))

    def edit_macros(self, clicked_item, dialog_list):
        dialog = QDialog(self)
        dialog_ui = macros_edit()
        dialog_ui.setupUi(dialog)

        old_name = clicked_item.text()
        old_code = clicked_item.toolTip()

        dialog_ui.variable.setText(old_name)
        dialog_ui.code.setText(old_code)

        def save():
            if check_null_value(dialog_ui.variable.text()) or check_null_value(dialog_ui.code.toPlainText()):
                dialog_ui.null_value.show()
                dialog_ui.save.clearFocus()
                return
            if dialog_ui.null_value.isVisible():
                dialog_ui.null_value.hide()

            new_name = dialog_ui.variable.text()
            new_code = dialog_ui.code.toPlainText()

            if old_name != new_name:
                del self.macros[old_name]
                dialog_list.listWidget.takeItem(dialog_list.listWidget.currentRow())

                item = QListWidgetItem(new_name)
                item.setToolTip(new_code)
                dialog_list.listWidget.addItem(item)
            elif old_code != new_code:
                clicked_item.setToolTip(new_code)

            if old_name != new_name or old_code != new_code:
                self.macros[new_name] = new_code
                save_macros(self.macros)
            dialog_ui.save.clearFocus()
            dialog.close()

        dialog_ui.save.clicked.connect(save)
        dialog.exec()

    def delete_macros(self, clicked_item, dialog_list):
        if clicked_item.text() in self.macros:
            del self.macros[clicked_item.text()]
            save_macros(self.macros)
            dialog_list.listWidget.takeItem(dialog_list.listWidget.currentRow())

    def add_new_macros(self, dialog_list):
        dialog = QDialog(self)
        dialog_ui = macros_edit()
        dialog_ui.setupUi(dialog)

        def save():
            if check_null_value(dialog_ui.variable.text()) or check_null_value(dialog_ui.code.toPlainText()):
                dialog_ui.null_value.show()
                dialog_ui.save.clearFocus()
                return
            if dialog_ui.null_value.isVisible():
                dialog_ui.null_value.hide()

            self.macros[dialog_ui.variable.text()] = dialog_ui.code.toPlainText()
            save_macros(self.macros)

            item = QListWidgetItem(dialog_ui.variable.text())
            item.setToolTip(dialog_ui.code.toPlainText())
            dialog_list.listWidget.addItem(item)

            dialog_ui.save.clearFocus()
            dialog.close()

        dialog_ui.save.clicked.connect(save)
        dialog.exec()

