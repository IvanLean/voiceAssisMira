from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox,QHeaderView
from PyQt5.QtCore import Qt
from commandFile import app_dict, startGame, pathArray,comsAppsArray
import functools
def open_table_window():
    # создаем новое окно с таблицей
    table_window = TableWindow()
    table_window.show()


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # создаем таблицу и заполняем ее данными
        table = QTableWidget()
        
        table.setColumnCount(2)
        table.setRowCount(len(app_dict))
        table.setHorizontalHeaderLabels(['Путь к исполняемому файлу', 'Команда для выполнения'])
        table.horizontalHeader().setStretchLastSection(True)
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # создаем вертикальный layout для добавления таблицы
        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.setSpacing(10)
        # создаем horizontal layout для добавления текстовых полей и кнопок
        mainBox = QHBoxLayout()
        
        # создаем label и textEdit для добавления данных в первый столбец таблицы
        col1_label = QLabel('Путь к исполняемому файлу:')
        col1_edit = QTextEdit()
        col1_edit.setStyleSheet("max-height: 20px")
        mainBox.addWidget(col1_label)
        mainBox.addWidget(col1_edit)

        # создаем label и textEdit для добавления данных во второй столбец таблицы
        col2_label = QLabel('Команда для выполнения:')
        col2_edit = QTextEdit()
        col2_edit.setStyleSheet("max-height: 20px")
        mainBox.addWidget(col2_label)
        mainBox.addWidget(col2_edit)

        # создаем кнопку для добавления данных в таблицу
        add_button = QPushButton('Добавить')
        add_button.clicked.connect(lambda: self.add_data(table, col1_edit.toPlainText(), col2_edit.toPlainText()))
        mainBox.addWidget(add_button)

        # создаем кнопку для удаления выбранной строки из таблицы
        del_button = QPushButton('Удалить')
        del_button.clicked.connect(lambda: self.del_data(table))
        mainBox.addWidget(del_button)

        # создаем кнопку для сохранения данных
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(lambda: self.save_data(table))
        mainBox.addWidget(save_button)

        # добавляем horizontal layout в вертикальный layout
        layout.addLayout(mainBox)

        # устанавливаем layout для виджета окна
        self.setLayout(layout)
        self.setWindowTitle('Добавление файлов')
        update_data(table)


        

    def add_data(self, table, col1_text, col2_text):
        # получаем количество строк в таблице и добавляем новую строку
        row_count = table.rowCount()
        table.insertRow(row_count)

        # добавляем данные в первый столбец таблицы
        item1 = QTableWidgetItem(col1_text)
        item1.setFlags(item1.flags() & ~Qt.ItemIsEditable) # делаем ячейку не редактируемой
        table.setItem(row_count, 0, item1)

        # добавляем данные во второй столбец таблицы
        item2 = QTableWidgetItem(col2_text)
        item2.setFlags(item2.flags() & ~Qt.ItemIsEditable) # делаем ячейку не редактируемой
        table.setItem(row_count, 1, item2)

    def del_data(self, table):
        # получаем выбранную строку и ее номер

        selected_row = table.currentRow()
        if selected_row == -1:  # если строка не выбрана, то выходим из функции
            return
        print("Удаленный элемент")
        print(app_dict)
        del pathArray[selected_row]
        del comsAppsArray[selected_row]
        del app_dict[comsAppsArray[selected_row]]
        table.removeRow(selected_row)  # удаляем выбранную строку из таблицы

    def save_data(self, table):
        data = {}
        pathArray.clear()
        comsAppsArray.clear()
        app_dict.clear()
        print("TABLE ROWCOUNT", table.rowCount())
        for i in range(table.rowCount()):
            path_item = table.item(i, 0)
            command_item = table.item(i, 1)
            if path_item is not None and command_item is not None:
                pathArray.append(path_item.text())
                print(path_item.text())
                comsAppsArray.append(command_item.text())
                print(command_item.text())
                data[command_item.text()] = lambda site=path_item.text(): startGame(site)
        # сохранение данных в словарь
        app_dict.update(data)
        print(app_dict)
        #app_dict.update(data)
        



def update_data(table):
    for i, (key, value) in enumerate(app_dict.items()):
        command_item = QTableWidgetItem(str(key))
        path_item = QTableWidgetItem(str(value))
        pathArr = QTableWidgetItem(str(pathArray[i]))
        table.setItem(i, 0, pathArr)
        table.setItem(i, 1, command_item)