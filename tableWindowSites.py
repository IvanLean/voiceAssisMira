from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, \
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox,QHeaderView
from PyQt5.QtCore import Qt
from commandFile import site_dict, startGame,sitesArray,comsSitesArray

def open_table_window_sites():
    # создаем новое окно с таблицей
    table_window = TableWindow()
    table_window.show()


class TableWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # создаем таблицу и заполняем ее данными
        table = QTableWidget()
        
        table.setColumnCount(2)
        table.setRowCount(len(site_dict))
        table.setHorizontalHeaderLabels(['Путь к сайту', 'Команда для выполнения'])
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
        col1_label = QLabel('Путь к сайту:')
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
        add_button.clicked.connect(lambda: self.add_data(table, col1_edit.toPlainText(), col2_edit.toPlainText(),col1_edit,col2_edit))
        
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


        

    def add_data(self, table, col1_text, col2_text,col1_edit,col2_edit):
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
        col1_edit.clear()
        col2_edit.clear()




    def del_data(self, table):
        # получаем выбранную строку и ее номер
        selected_row = table.currentRow()
        if selected_row == -1:  # если строка не выбрана, то выходим из функции
            return
        print("Удаленный элемент")
        print(site_dict)
        del sitesArray[selected_row-1]
        del site_dict[comsSitesArray[selected_row-1]]
        # Перебрать все пары ключ-значение

        table.removeRow(selected_row)  # удаляем выбранную строку из таблицы

        

    def save_data(self, table):
        data = {}
        sitesArray.clear()
        comsSitesArray.clear()
        site_dict.clear()
        print(site_dict)
        for i in range(table.rowCount()):
            site_item = table.item(i, 0)
            command_item = table.item(i, 1)
            if site_item is not None and command_item is not None:
                sitesArray.append(site_item.text())
                comsSitesArray.append(command_item.text())
                data[command_item.text()] = lambda site=site_item.text(): startGame(site)
        # сохранение данных в словарь
        site_dict.update(data)
        print(site_dict)



def update_data(table):
    for i, (key, value) in enumerate(site_dict.items()):
        command_item = QTableWidgetItem(str(key))
        siteArr = QTableWidgetItem(str(sitesArray[i]))
        print(sitesArray)
        table.setItem(i, 0, siteArr)
        table.setItem(i, 1, command_item)