from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from tableWindowApps import open_table_window
from tableWindowSites import open_table_window_sites
import startProgrammWidget, getWether
def create_custom_functions_widget():
    widget = QWidget()

    # создаем вертикальный layout
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignTop)
    layout.setSpacing(20)

    leftBox = QVBoxLayout()
    rightBox = QVBoxLayout()
    publicBox = QHBoxLayout()



    leftBox.setAlignment(Qt.AlignLeft)
    rightBox.setAlignment(Qt.AlignLeft)

    title=QLabel("Функции")
    font = QFont("Times New Roman", weight=50)
    title.setFont(font)

    autostart = QLabel("Автозапуск программы:")
    autostart.setCursor(Qt.WhatsThisCursor)
    autostart.setToolTip("<font color='black'>Программа будет запускаться при старте операционной системы</font>")
    autostartCheck = QCheckBox()


    hotwordLabel = QLabel("Ключевое слово:")
    hotwordLabel.setToolTip("<font color='black'>После этого слова, программа будет ожидать команду</font>")
    hotwordLabel.setCursor(Qt.WhatsThisCursor)
    hotwordLabel.setStyleSheet("max-width: 150px;")
    hotwordEdit = QLineEdit(startProgrammWidget.hot_word)
    hotwordEdit.setStyleSheet("max-width: 100px;")

    cityLabel = QLabel("Ваш город:")
    cityLabel.setToolTip("<font color='black'>Требуется, чтобы отслеживать погоду и другие параметры вашего города.</font>")
    cityLabel.setCursor(Qt.WhatsThisCursor)
    cityLabel.setStyleSheet("max-width: 150px;")
    cityEdit = QLineEdit(getWether.city)
    cityEdit.setStyleSheet("max-width: 100px;")



    recognizerTypeLabel = QLabel("Распознаватель ключевого слова")
    recognizerTypeLabel.setToolTip("<font color='black'>То что будет распознавать ваше ключевое слово</font>")
    recognizerTypeLabel.setCursor(Qt.WhatsThisCursor)
    #recognizerTypeLabel.setStyleSheet("max-width: 150px;")
    recognizerTypeEdit = QComboBox()
    recognizerTypeEdit.setStyleSheet("max-width: 100px;")
    recognizerTypeEdit.addItem("Google")
    recognizerTypeEdit.addItem("Vosk")
    recognizerTypeEdit.setCurrentText(startProgrammWidget.recognizerType)# неверно работает исправить!!!
    commandrecognizerTypeLabel = QLabel("Распознаватель комманды")
    commandrecognizerTypeLabel.setToolTip("<font color='black'>То что будет распознавать вашу команду</font>")
    commandrecognizerTypeLabel.setCursor(Qt.WhatsThisCursor)
    #commandrecognizerTypeLabel.setStyleSheet("max-width: 150px;")
    commandrecognizerTypeEdit = QComboBox()
    commandrecognizerTypeEdit.setStyleSheet("max-width: 100px;")
    commandrecognizerTypeEdit.addItem("Google")
    commandrecognizerTypeEdit.addItem("Vosk")
    commandrecognizerTypeEdit.setCurrentText(startProgrammWidget.commandrecognizerType)# неверно работает исправить!!!


    filesLabel = QLabel("Файлы для запуска и их вызов:")
    filesLabel.setToolTip("<font color='black'>Файлы которые будут запускать по вашей команде</font>")
    filesLabel.setCursor(Qt.WhatsThisCursor)

    sitesLabel = QLabel("Ссылки для поиска и их вызов:")
    sitesLabel.setToolTip("<font color='black'>Сайты которые будут открываться по вашей команде</font>")
    sitesLabel.setCursor(Qt.WhatsThisCursor)

    # Создаем кнопку "Добавить файл"
    add_file_button = QPushButton("Добавить файл")
    add_file_button.clicked.connect(lambda: open_table_window())

        # Создаем кнопку "Добавить файл"
    add_site_button = QPushButton("Добавить сайт")
    add_site_button.clicked.connect(lambda: open_table_window_sites())

    save_but=QPushButton("Сохранить")
    save_but.setStyleSheet("max-width:100px")

    # добавляем параметры на виджет
    leftBox.addWidget(autostart)
    leftBox.addWidget(hotwordLabel)
    leftBox.addWidget(cityLabel)
    leftBox.addWidget(filesLabel)
    leftBox.addWidget(sitesLabel)
    leftBox.addWidget(recognizerTypeLabel)
    leftBox.addWidget(commandrecognizerTypeLabel)
    rightBox.addWidget(autostartCheck)
    rightBox.addWidget(hotwordEdit)
    rightBox.addWidget(cityEdit)
    rightBox.addWidget(add_file_button)
    rightBox.addWidget(add_site_button)
    rightBox.addWidget(recognizerTypeEdit)
    rightBox.addWidget(commandrecognizerTypeEdit)
    publicBox.addLayout(leftBox)
    publicBox.addLayout(rightBox)
    

    publicBox.setStretchFactor(leftBox, 1)
    publicBox.setStretchFactor(rightBox, 1)


    layout.addLayout(publicBox)
    #layout.addWidget(table)
    layout.addWidget(save_but)

    save_but.clicked.connect(lambda: save_data())
    
    def save_data():
        startProgrammWidget.hot_word=hotwordEdit.text()
        getWether.city=cityEdit.text()
        startProgrammWidget.recognizerType = str(recognizerTypeEdit.currentText())
        startProgrammWidget.commandrecognizerType = str(commandrecognizerTypeEdit.currentText())
        print(startProgrammWidget.hot_word)

    return widget




# Функция для добавления файла в таблицу
def add_file_to_table(table):
    row_position = table.rowCount()
    table.insertRow(row_position)
    table.setItem(row_position, 0, QTableWidgetItem(""))
    table.setItem(row_position, 1, QTableWidgetItem(""))


