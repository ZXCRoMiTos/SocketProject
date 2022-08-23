from PyQt5.QtWidgets import qApp, QApplication, QMainWindow, QAction, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys


def create_gui_model(database):
    active_users = database.active_users_list()
    list_table = QStandardItemModel()
    headers = ['Имя клиента', 'IP-адрес', 'Порт', 'Дата и время']
    list_table.setHorizontalHeaderLabels(headers)
    for row in active_users:
        row_into_table = []
        variables = ['user', 'ip', 'port', 'date']
        for name, value in zip(variables, row):
            locals()[name] = QStandardItem(str(value))
            locals()[name].setEditable(False)
            row_into_table.append(locals()[name])
        list_table.appendRow(row_into_table)
    return list_table


def create_stat_model(database):
    history_list = database.show_history()
    list_table = QStandardItemModel()
    headers = ['Имя клиента', 'Время последнего входа', 'Отпрпавлено', 'Полученор']
    list_table.setHorizontalHeaderLabels(headers)
    for row in history_list:
        row_into_table = []
        variables = ['user', 'last_seen', 'sent', 'recieve']
        for name, value in zip(variables, row):
            locals()[name] = QStandardItem(str(value))
            locals()[name].setEditable(False)
            row_into_table.append(locals()[name])
        list_table.appendRow(row_into_table)
    return list_table


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.exit_btn = QAction('Выход', self)
        self.exit_btn.setShortcut('Ctrl + Q')
        self.exit_btn.triggered.connect(qApp.quit)

        self.refresh_btn = QAction('Обновить список', self)
        self.history_btn = QAction('История клиентов', self)
        self.config_btn = QAction('Настройки сервера', self)

        self.statusBar()

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exit_btn)
        self.toolbar.addAction(self.refresh_btn)
        self.toolbar.addAction(self.history_btn)
        self.toolbar.addAction(self.config_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('SERVER || Messenger v1.0')

        self.label = QLabel('Список подключенных клиентов', self)
        self.label.setFixedSize(400, 15)
        self.label.move(10, 35)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 55)
        self.active_clients_table.setFixedSize(780, 400)

        self.show()


class HistoryWindow(QDialog):
    def __init__(self):
        super(HistoryWindow, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.setWindowTitle('История клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.close_button = QPushButton('Закрыть', self)
        self.close_button.move(250, 650)
        self.close_button.clicked.connect(self.close)

        self.history_table = QTableView(self)
        self.history_table.move(10, 10)
        self.history_table.setFixedSize(580, 620)

        self.show()


class ConfigWindow(QDialog):
    def __init__(self):
        super(ConfigWindow, self).__init__()
        self.init_UI()

    def init_UI(self):
        self.setFixedSize(365, 260)
        self.setWindowTitle('Настройки сервера')

        self.db_path_label = QLabel('Путь до файла базы данных', self)
        self.db_path_label.move(10, 20)
        self.db_path_label.setFixedSize(250, 15)

        self.db_path = QLineEdit(self)
        self.db_path.setFixedSize(250, 20)
        self.db_path.move(10, 40)
        self.db_path.setReadOnly(True)

        self.db_path_select = QPushButton('Обзор...', self)
        self.db_path_select.move(265, 38)

        def open_file_dialog():
            global dialog
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.db_path.insert(path)

        self.db_path_select.clicked.connect(open_file_dialog)

        self.db_file_label = QLabel('Имя файла базы данных: ', self)
        self.db_file_label.move(10, 78)
        self.db_file_label.setFixedSize(180, 15)

        self.db_file = QLineEdit(self)
        self.db_file.move(200, 76)
        self.db_file.setFixedSize(150, 20)

        self.port_label = QLabel('Номер порта для соединения: ', self)
        self.port_label.move(10, 118)
        self.port_label.setFixedSize(180, 15)

        self.port = QLineEdit(self)
        self.port.move(200, 118)
        self.port.setFixedSize(150, 20)

        self.ip_lable = QLabel('IP-адрес для соединения: ', self)
        self.ip_lable.move(10, 158)
        self.ip_lable.setFixedSize(180, 15)

        self.ip = QLineEdit(self)
        self.ip.move(200, 158)
        self.ip.setFixedSize(150, 20)

        self.save_btn = QPushButton('Сохранить', self)
        self.save_btn.move(90, 200)

        self.close_btn = QPushButton('Закрыть', self)
        self.close_btn.move(175, 200)
        self.close_btn.clicked.connect(self.close)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    history_window = HistoryWindow()
    config_window = ConfigWindow()
    test_list = QStandardItemModel(main_window)
    test_list.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    test_list.appendRow(
        [QStandardItem('test1'), QStandardItem('192.198.0.5'), QStandardItem('23544'), QStandardItem('16:20:34')])
    test_list.appendRow(
        [QStandardItem('test2'), QStandardItem('192.198.0.8'), QStandardItem('33245'), QStandardItem('16:22:11')])
    main_window.active_clients_table.setModel(test_list)
    main_window.active_clients_table.resizeColumnsToContents()
    app.exec_()
