from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import startProgrammWidget
def create_settings_widget():
    widget = QWidget()

    # создаем вертикальный layout
    layout = QVBoxLayout(widget)
    layout.setAlignment(Qt.AlignTop)
    layout.setSpacing(20)

    # создаем горизонтальный layout
    leftBox = QVBoxLayout()
    rightBox = QVBoxLayout()
    publicBox = QHBoxLayout()

    leftBox.setAlignment(Qt.AlignLeft)
    rightBox.setAlignment(Qt.AlignLeft)
    # создаем несколько обычных параметров


    dynamicLabel = QLabel("Динамическое шумоподавление:")
    dynamicLabel.setCursor(Qt.WhatsThisCursor)
    dynamicLabel.setToolTip("<font color='black'>Динамическое распознование шумов при начале прослушивания</font>")
    threshould = QCheckBox()
    threshould.setChecked(startProgrammWidget.dynamic_threshold)
    energythresholdLabel = QLabel("Пороговое значение чувствительности")
    energythresholdLabel.setToolTip("<font color='black'>Задает пороговое значение чувствительности микрофона. Меньшие значения позволяют лучше распознавать тихие звуки, но могут также распознавать фоновый шум</font>")
    energythresholdLabel.setCursor(Qt.WhatsThisCursor)
    energythresholdEdit = QLineEdit(str(startProgrammWidget.energy_threshold))
    energythresholdEdit.setMaximumWidth(50)

    pausethresholdLabel = QLabel("Минимальная продолжительность тишины (в секундах)")
    pausethresholdLabel.setCursor(Qt.WhatsThisCursor)
    pausethresholdLabel.setToolTip("<font color='black'>Представляет минимальную продолжительность тишины (в секундах), которая будет регистрироваться как конец фразы.</font>")
    pausethresholdEdit = QLineEdit(str(startProgrammWidget.pause_threshold))
    pausethresholdEdit.setMaximumWidth(50)

    phrasetimeLabelHotword = QLabel("Ограничение времени при прослушивании горячего слова")
    phrasetimeLabelHotword.setCursor(Qt.WhatsThisCursor)
    phrasetimeLabelHotword.setToolTip("<font color='black'>Представляет минимальную продолжительность тишины (в секундах), которая будет регистрироваться как конец фразы.</font>")
    phrasetimeEditHotword = QLineEdit(str(startProgrammWidget.phrase_time_limit_hotword))
    phrasetimeEditHotword.setMaximumWidth(50)

    phrasetimeLabelCommand = QLabel("Ограничение времени при прослушивании команды")
    phrasetimeLabelCommand.setCursor(Qt.WhatsThisCursor)
    phrasetimeLabelCommand.setToolTip("<font color='black'>Представляет минимальную продолжительность тишины (в секундах), которая будет регистрироваться как конец фразы.</font>")
    phrasetimeEditCommand = QLineEdit(str(startProgrammWidget.phrase_time_limit_command))
    phrasetimeEditCommand.setMaximumWidth(50)
    
    save_but=QPushButton("Сохранить")
    save_but.setStyleSheet("max-width:100px")
    
    # добавляем параметры на виджет

    # добавляем параметры на виджет

    leftBox.addWidget(dynamicLabel)
    leftBox.addWidget(energythresholdLabel)
    leftBox.addWidget(pausethresholdLabel)
    leftBox.addWidget(phrasetimeLabelHotword)
    leftBox.addWidget(phrasetimeLabelCommand)
    rightBox.addWidget(threshould)
    rightBox.addWidget(energythresholdEdit)
    rightBox.addWidget(pausethresholdEdit)
    rightBox.addWidget(phrasetimeEditHotword)
    rightBox.addWidget(phrasetimeEditCommand)
    # добавляем горизонтальные layout на вертикальный layout
    
    publicBox.addLayout(leftBox)
    publicBox.addLayout(rightBox)
    publicBox.setStretchFactor(leftBox, 1)
    publicBox.setStretchFactor(rightBox, 1)
    
    layout.addLayout(publicBox)
    layout.addWidget(save_but)

    save_but.clicked.connect(lambda: save_data())

    def save_data():
        startProgrammWidget.energy_threshold=int(energythresholdEdit.text())
        startProgrammWidget.pause_threshold=float(pausethresholdEdit.text())
        startProgrammWidget.phrase_time_limit_command=int(phrasetimeEditCommand.text())
        startProgrammWidget.phrase_time_limit_hotword=int(phrasetimeEditHotword.text())
        print(startProgrammWidget.energy_threshold,startProgrammWidget.pause_threshold,startProgrammWidget.phrase_time_limit_command,startProgrammWidget.phrase_time_limit_hotword)





    return widget


    
