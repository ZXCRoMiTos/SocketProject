from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QComboBox, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, qApp, QMessageBox
from PyQt5.QtCore import Qt, pyqtSlot
import logging
import sys
sys.path.append('../')
from errors import ServerError


logger = logging.getLogger('client_dist')


class Ui_MainClientWindow(object):
    def setupUi(self, MainClientWindow):
        MainClientWindow.setObjectName("MainClientWindow")
        MainClientWindow.resize(756, 534)
        MainClientWindow.setMinimumSize(QtCore.QSize(756, 534))
        self.centralwidget = QtWidgets.QWidget(MainClientWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_contacts = QtWidgets.QLabel(self.centralwidget)
        self.label_contacts.setGeometry(QtCore.QRect(10, 0, 101, 16))
        self.label_contacts.setObjectName("label_contacts")
        self.btn_add_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_add_contact.setGeometry(QtCore.QRect(10, 450, 121, 31))
        self.btn_add_contact.setObjectName("btn_add_contact")
        self.btn_remove_contact = QtWidgets.QPushButton(self.centralwidget)
        self.btn_remove_contact.setGeometry(QtCore.QRect(140, 450, 121, 31))
        self.btn_remove_contact.setObjectName("btn_remove_contact")
        self.label_history = QtWidgets.QLabel(self.centralwidget)
        self.label_history.setGeometry(QtCore.QRect(300, 0, 391, 21))
        self.label_history.setObjectName("label_history")
        self.text_message = QtWidgets.QTextEdit(self.centralwidget)
        self.text_message.setGeometry(QtCore.QRect(300, 360, 441, 71))
        self.text_message.setObjectName("text_message")
        self.label_new_message = QtWidgets.QLabel(self.centralwidget)
        self.label_new_message.setGeometry(QtCore.QRect(300, 330, 450, 16)) # Правка тут
        self.label_new_message.setObjectName("label_new_message")
        self.list_contacts = QtWidgets.QListView(self.centralwidget)
        self.list_contacts.setGeometry(QtCore.QRect(10, 20, 251, 411))
        self.list_contacts.setObjectName("list_contacts")
        self.list_messages = QtWidgets.QListView(self.centralwidget)
        self.list_messages.setGeometry(QtCore.QRect(300, 20, 441, 301))
        self.list_messages.setObjectName("list_messages")
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(610, 450, 131, 31))
        self.btn_send.setObjectName("btn_send")
        self.btn_clear = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear.setGeometry(QtCore.QRect(460, 450, 131, 31))
        self.btn_clear.setObjectName("btn_clear")
        MainClientWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainClientWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 756, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainClientWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainClientWindow)
        self.statusBar.setObjectName("statusBar")
        MainClientWindow.setStatusBar(self.statusBar)
        self.menu_exit = QtWidgets.QAction(MainClientWindow)
        self.menu_exit.setObjectName("menu_exit")
        self.menu_add_contact = QtWidgets.QAction(MainClientWindow)
        self.menu_add_contact.setObjectName("menu_add_contact")
        self.menu_del_contact = QtWidgets.QAction(MainClientWindow)
        self.menu_del_contact.setObjectName("menu_del_contact")
        self.menu.addAction(self.menu_exit)
        self.menu_2.addAction(self.menu_add_contact)
        self.menu_2.addAction(self.menu_del_contact)
        self.menu_2.addSeparator()
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainClientWindow)
        self.btn_clear.clicked.connect(self.text_message.clear)
        QtCore.QMetaObject.connectSlotsByName(MainClientWindow)

    def retranslateUi(self, MainClientWindow):
        _translate = QtCore.QCoreApplication.translate
        MainClientWindow.setWindowTitle(_translate("MainClientWindow", "Чат Программа alpha release"))
        self.label_contacts.setText(_translate("MainClientWindow", "Список контактов:"))
        self.btn_add_contact.setText(_translate("MainClientWindow", "Добавить контакт"))
        self.btn_remove_contact.setText(_translate("MainClientWindow", "Удалить контакт"))
        self.label_history.setText(_translate("MainClientWindow", "История сообщений:"))
        self.label_new_message.setText(_translate("MainClientWindow", "Введите новое сообщение:"))
        self.btn_send.setText(_translate("MainClientWindow", "Отправить сообщение"))
        self.btn_clear.setText(_translate("MainClientWindow", "Очистить поле"))
        self.menu.setTitle(_translate("MainClientWindow", "Файл"))
        self.menu_2.setTitle(_translate("MainClientWindow", "Контакты"))
        self.menu_exit.setText(_translate("MainClientWindow", "Выход"))
        self.menu_add_contact.setText(_translate("MainClientWindow", "Добавить контакт"))
        self.menu_del_contact.setText(_translate("MainClientWindow", "Удалить контакт"))


class StartDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Добро пожаловать')
        self.setFixedSize(470, 280)

        self.bold_font = QFont('Times', 18, QFont.Bold)
        self.normal_font = QFont('Times', 18)
        self.reduced_font = QFont('Times', 16)

        self.label = QLabel('Введите имя пользователя: ', self)
        self.label.setFont(self.bold_font)
        self.label.setFixedSize(450, 50)
        self.label.move(10, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFont(self.reduced_font)
        self.client_name.setFixedSize(450, 40)
        self.client_name.move(10, 60)

        self.label_password = QLabel('Введите пароль: ', self)
        self.label_password.setFont(self.bold_font)
        self.label_password.setFixedSize(450, 50)
        self.label_password.move(10, 100)

        self.client_password = QLineEdit(self)
        self.client_password.setFont(self.reduced_font)
        self.client_password.setFixedSize(450, 40)
        self.client_password.move(10, 150)
        self.client_password.setEchoMode(QLineEdit.Password)

        self.ok_pressed = False
        self.ok_btn = QPushButton('Начать', self)
        self.ok_btn.setFont(self.normal_font)
        self.ok_btn.setFixedSize(220, 60)
        self.ok_btn.move(10, 210)
        self.ok_btn.clicked.connect(self.click)

        self.cancel_btn = QPushButton('Выход', self)
        self.cancel_btn.setFixedSize(220, 60)
        self.cancel_btn.setFont(self.normal_font)
        self.cancel_btn.move(240, 210)
        self.cancel_btn.clicked.connect(qApp.exit)

        self.show()

    def click(self):
        if self.client_name.text() and self.client_password.text():
            self.ok_pressed = True
            qApp.exit()


class AddContactDialog(QDialog):
    def __init__(self, transport, database):
        super().__init__()
        self.transport = transport
        self.database = database
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Выберите контакт для добавления: ')
        self.setFixedSize(350, 120)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для добавления: ', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.refresh_btn = QPushButton('Обновить список', self)
        self.refresh_btn.setFixedSize(100, 30)
        self.refresh_btn.move(60, 60)
        self.refresh_btn.clicked.connect(self.update_possible_contacts)

        self.ok_btn = QPushButton('Добавить', self)
        self.ok_btn.setFixedSize(100, 30)
        self.ok_btn.move(230, 20)

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.setFixedSize(100, 30)
        self.cancel_btn.move(230, 60)
        self.cancel_btn.clicked.connect(self.close)

        self.add_possible_contacts()

    def add_possible_contacts(self):
        self.selector.clear()
        contacts_list = set(self.database.get_contacts())
        users_list = set(self.database.get_users())
        users_list.remove(self.transport.username)
        self.selector.addItems(users_list - contacts_list)

    def update_possible_contacts(self):
        try:
            self.transport.user_list_update()
        except OSError:
            pass
        else:
            logger.debug('Обновление списка пользователей выполнено')
            self.add_possible_contacts()


class DeleteContactDialog(QDialog):
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('Удаление контакта')
        self.setFixedSize(350, 120)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setModal(True)

        self.selector_label = QLabel('Выберите контакт для удаления', self)
        self.selector_label.setFixedSize(200, 20)
        self.selector_label.move(10, 0)

        self.selector = QComboBox(self)
        self.selector.setFixedSize(200, 20)
        self.selector.move(10, 30)

        self.selector.addItems(sorted(self.database.get_contacts()))

        self.ok_btn = QPushButton('Удалить', self)
        self.ok_btn.setFixedSize(100, 30)
        self.ok_btn.move(230, 20)

        self.cancel_btn = QPushButton('Отмена', self)
        self.cancel_btn.setFixedSize(100, 30)
        self.cancel_btn.move(230, 60)
        self.cancel_btn.clicked.connect(self.close)


class ClientMainWindow(QMainWindow):
    def __init__(self, database, transport):
        super(ClientMainWindow, self).__init__()
        self.database = database
        self.transport = transport
        self.init_UI()

    def init_UI(self):
        self.ui = Ui_MainClientWindow()
        self.ui.setupUi(self)

        self.ui.menu_exit.triggered.connect(qApp.exit)
        self.ui.btn_send.clicked.connect(self.send_message)
        self.ui.btn_add_contact.clicked.connect(self.add_contact_window)
        self.ui.menu_add_contact.triggered.connect(self.add_contact_window)
        self.ui.btn_remove_contact.clicked.connect(self.delete_contact_window)
        self.ui.menu_del_contact.triggered.connect(self.delete_contact_window)
        self.ui.list_contacts.doubleClicked.connect(self.select_active_user)

        self.messages = QMessageBox()
        self.current_chat = None
        self.history_model = None
        self.contacts_model = None

        self.ui.list_messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.list_messages.setWordWrap(True)

        self.clients_list_update()
        self.history_list_update()

        self.show()

    def send_message(self):
        message_text = self.ui.text_message.toPlainText()
        self.ui.text_message.clear()
        if not message_text:
            return
        try:
            self.transport.send_message(self.current_chat, message_text)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            else:
                self.database.save_message(self.current_chat, 'out', message_text)
                logger.debug(f'Отправлено сообщение для {self.current_chat}: {message_text}')
                self.history_list_update()

    def history_list_update(self):
        list_messages = self.database.get_history(self.current_chat)
        list_messages = sorted(list_messages, key=lambda item: item[3])
        if not self.history_model:
            self.history_model = QStandardItemModel()
            self.ui.list_messages.setModel(self.history_model)
        self.history_model.clear()

        length = len(list_messages)
        start_index = 0
        if length > 20:
            start_index = length - 20

        for i in range(start_index, length):
            item = list_messages[i]
            if item[1] == 'in':
                msg = QStandardItem(f'Входящее от {item[3]}:\n {item[2]}')
                msg.setEditable(False)
                msg.setBackground(QBrush(QColor(255, 213, 213)))
                msg.setTextAlignment(Qt.AlignLeft)
                self.history_model.appendRow(msg)
            else:
                msg = QStandardItem(f'Исходящее от {item[3]}:\n {item[2]}')
                msg.setEditable(False)
                msg.setBackground(QBrush(QColor(204, 255, 204)))
                msg.setTextAlignment(Qt.AlignRight)
                self.history_model.appendRow(msg)
        self.ui.list_messages.scrollToBottom()

    def add_contact_window(self):
        global select_dialog
        select_dialog = AddContactDialog(self.transport, self.database)
        select_dialog.ok_btn.clicked.connect(lambda: self.add_contact_action(select_dialog))
        select_dialog.show()

    def add_contact_action(self, item):
        new_contact = item.selector.currentText()
        self.add_contact(new_contact)
        item.close()

    def add_contact(self, new_contact):
        try:
            self.transport.add_contact(new_contact)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаует соединения')
        else:
            self.database.add_contact(new_contact)
            new_contact = QStandardItem(new_contact)
            new_contact.setEditable(False)
            self.contacts_model.appendRow(new_contact)
            logger.info(f'Успешно добавлен контакт {new_contact}')
            self.messages.information(self, 'Успешно', 'Контакт успешно добавлен')

    def delete_contact_window(self):
        global remove_dialog
        remove_dialog = DeleteContactDialog(self.database)
        remove_dialog.ok_btn.clicked.connect(lambda: self.delete_contact(remove_dialog))
        remove_dialog.show()

    def delete_contact(self, contact):
        selected = contact.selector.currentText()
        try:
            self.transport.remove_contact(selected)
        except ServerError as err:
            self.messages.critical(self, 'Ошибка сервера', err.text)
        except OSError as err:
            if err.errno:
                self.messages.critical(self, 'Ошибка', 'Потеряно соединение с сервером')
                self.close()
            self.messages.critical(self, 'Ошибка', 'Таймаут соединения')
        else:
            self.database.del_contact(selected)
            self.clients_list_update()
            logger.info(f'Успешно удален контакт {contact}')
            self.messages.information(self, 'Успех', 'Контакт успешно удален')
            contact.close()
            if selected == self.current_chat:
                self.current_chat = None
                self.set_disabled_input()

    def clients_list_update(self):
        contacts_list = self.database.get_contacts()
        self.contacts_model = QStandardItemModel()
        for item in sorted(contacts_list):
            item = QStandardItem(item)
            item.setEditable(False)
            self.contacts_model.appendRow(item)
        self.ui.list_contacts.setModel(self.contacts_model)

    def set_disabled_input(self):
        self.ui.label_new_message.setText('Для выбора получателя '
                                          'дважды кликните на него в окне контактов')
        self.ui.text_message.clear()
        if self.history_model:
            self.history_model.clear()

        self.ui.btn_clear.setDisabled(True)
        self.ui.btn_send.setDisabled(True)
        self.ui.text_message.setDisabled(True)

    def select_active_user(self):
        self.current_chat = self.ui.list_contacts.currentIndex().data()
        self.set_active_user()

    def set_active_user(self):
        self.ui.label_new_message.setText(f'Введите сообщение для {self.current_chat}')
        self.ui.btn_clear.setDisabled(False)
        self.ui.btn_send.setDisabled(False)
        self.ui.text_message.setDisabled(False)
        self.history_list_update()

    @pyqtSlot(str)
    def message(self, sender):
        if sender == self.current_chat:
            self.history_list_update()
        else:
            if self.database.check_contact(sender):
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}'
                                          f'открыть чат с ним?', QMessageBox.Yes,
                                          QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()
            else:
                if self.messages.question(self, 'Новое сообщение',
                                          f'Получено новое сообщение от {sender}.\n '
                                          f'Данного пользователя нет в вашем контакт-листе.\n'
                                          f' Добавить в контакты и открыть чат с ним?',
                                          QMessageBox.Yes, QMessageBox.No) == QMessageBox.Yes:
                    self.add_contact(sender)
                    self.current_chat = sender
                    self.set_active_user()

    @pyqtSlot()
    def connection_lost(self):
        self.messages.warning(self, 'Сбой соединения', 'Потеряно соединение с сервером')
        self.close()

    def make_connection(self, trans_obj):
        trans_obj.new_message.connect(self.message)
        trans_obj.connection_lost.connect(self.connection_lost)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = StartDialog()
    app.exec_()
