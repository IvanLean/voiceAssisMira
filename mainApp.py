from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon,QColor
from functionsWidget import create_custom_functions_widget
from settingWidget import create_settings_widget
from startProgrammWidget import create_launch_program_widget
import startProgrammWidget, getWether
from helpFIle import HelpDialog, startOptText,settingsOptText,functionsOptText
import commandFile

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



           
        self.settings = QSettings('BotAssistant', 'NIDco',self)

        self.load_global_data()

  

        # устанавливаем фиксированный размер окна
        self.setFixedSize(800, 600)
        self.setWindowTitle("Bot Assistant")
        # устанавливаем серый фон всех окон
        self.setStyleSheet("background-color:#24153d; color:white; font-size:18px;")


        # создаем стек виджет и добавляем в него виджеты
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(create_launch_program_widget())
        self.stacked_widget.addWidget(create_settings_widget())
        self.stacked_widget.addWidget(create_custom_functions_widget())
        
    
        # создаем кнопки для переключения между виджетами
        self.btn_menu = QPushButton()
        self.btn_menu.setIcon(QIcon("resources\menu.png"))
        self.btn_menu.setIconSize(QSize(30,30))
        self.btn_launch_program = QPushButton()
        self.btn_launch_program.setIcon(QIcon("resources\microphone.png"))
        self.btn_launch_program.setIconSize(QSize(30,30))
        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(QIcon("resources\settings.png"))
        self.btn_settings.setIconSize(QSize(30,30))
        self.btn_user_functions = QPushButton()
        self.btn_user_functions.setIcon(QIcon("resources\list.png"))
        self.btn_user_functions.setIconSize(QSize(30,30))
        
        # устанавливаем фоновый цвет для кнопок и шрифт
        #buttons_widget_style="background-color: rgb(29,43,77); color: white; font-size: 20px;height:80px; "
        buttons_widget_style = '''
            QPushButton {
                background-color: qlineargradient(x1: -3, y1: 0, x2: 1, y2: 0,
                stop: 0 #00ced1, stop: 1 #8a2be2);
                color: white;
                border: none;
                font-size: 20px;
                height: 200px;
                
            }
            QPushButton:hover {
                background-color: rgb(53,80,142);
            }
            QPushButton:pressed {
                background-color: rgb(73,100,162);
            }
        '''
        self.btn_menu.setStyleSheet(buttons_widget_style)
        self.btn_launch_program.setStyleSheet(buttons_widget_style)
        self.btn_settings.setStyleSheet(buttons_widget_style)
        self.btn_user_functions.setStyleSheet(buttons_widget_style)

        # устанавливаем обработчики нажатий на кнопки
        self.btn_menu.clicked.connect(lambda: self.toggle_menu())
        self.btn_launch_program.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_user_functions.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # создаем главный виджет, на котором разместим кнопки и стек виджет
        main_widget = QWidget(self)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        main_layout.addWidget(self.create_buttons_widget())
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(main_widget)




        # Создание справки и ее параметров
        self.help_dialog = HelpDialog()
        self.help_dialog.set_help_text(startOptText)
        self.settings_dialog = HelpDialog()
        self.settings_dialog.set_settings_text(settingsOptText)
        self.functions_dialog = HelpDialog()
        self.functions_dialog.set_functions_text(functionsOptText)
        self.help_programm = QAction("Работа с программой", self)
        self.help_settings = QAction("Настройки", self)
        self.help_functions = QAction("Функции", self)
        self.help_programm.triggered.connect(self.show_help_dialog)
        self.help_settings.triggered.connect(self.show_settings_dialog)
        self.help_functions.triggered.connect(self.show_functions_dialog)

        # Настройка меню справки
        self.menu_bar = self.menuBar()
        self.help_menu = self.menu_bar.addMenu("Справка")
        self.help_menu.addAction(self.help_programm)
        self.help_menu.addAction(self.help_settings)
        self.help_menu.addAction(self.help_functions)

    def show_help_dialog(self):
        """
        Показывает диалоговое окно справки.
        """
        self.help_dialog.exec_()
    def show_settings_dialog(self):
        """
        Показывает диалоговое окно справки.
        """
        self.settings_dialog.exec_()
    def show_functions_dialog(self):
        """
        Показывает диалоговое окно справки.
        """
        self.functions_dialog.exec_()





    #сворачивание виджета с кнопками по клику
    def toggle_menu(self):
        if self.buttons_widget.width() == self.width() // 4:
            new_width = self.width() // 16
            self.btn_launch_program.setText("")
            self.btn_menu.setText("")
            self.btn_settings.setText("")
            self.btn_user_functions.setText("")
            
            self.btn_menu.setIcon(QIcon("resources\menu.png"))
            self.btn_menu.setIconSize(QSize(30,30))
            self.btn_launch_program.setIcon(QIcon("resources\microphone.png"))
            self.btn_launch_program.setIconSize(QSize(30,30))
            self.btn_settings.setIcon(QIcon("resources\settings.png"))
            self.btn_settings.setIconSize(QSize(30,30))
            self.btn_user_functions.setIcon(QIcon("resources\list.png"))
            self.btn_user_functions.setIconSize(QSize(30,30))
        else:
            new_width = self.width() // 4
            self.btn_launch_program.setText("Запуск программы")
            self.btn_settings.setText("Настройки")
            self.btn_user_functions.setText("Функции")

            self.btn_launch_program.setIcon(QIcon())
            self.btn_settings.setIcon(QIcon())
            self.btn_user_functions.setIcon(QIcon())
        self.buttons_widget.setFixedWidth(new_width)






        

    def create_buttons_widget(self):
        # создаем виджет с кнопками и задаем ему размеры
        buttons_widget = QWidget(self)
        buttons_widget.setFixedWidth(self.width() // 16)
        shadow = QGraphicsDropShadowEffect(blurRadius=50, xOffset=0, yOffset=0)
        shadow.setColor(QColor(48, 213, 200))

        # добавляем кнопки на виджет
        layout = QVBoxLayout(buttons_widget)
        layout.setAlignment(Qt.AlignTop)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.btn_menu,0)
        layout.addWidget(self.btn_launch_program,0)
        layout.addWidget(self.btn_settings,0)
        layout.addWidget(self.btn_user_functions,0)
        self.buttons_widget = buttons_widget # сохраняем ссылку на виджет, чтобы иметь возможность изменять его свойства
        
  
        layout.setSpacing(0)

        # растягиваем кнопки по высоте
        layout.addStretch()

        return buttons_widget


    def load_global_data(self):# загрузка сохраненных данных
        '''''
        text = self.settings.value("text", "")
        self.text_edit.setPlainText(text)

        checked = self.settings.value("checked", False, type=bool)
        self.checkbox.setChecked(checked)
        '''
        startProgrammWidget.hot_word = self.settings.value("hot_word", "мира")
        startProgrammWidget.phrase_time_limit_hotword = self.settings.value("phrase_time_limit_hotword",3)
        startProgrammWidget.phrase_time_limit_command = self.settings.value("phrase_time_limit_command",5)
        startProgrammWidget.dynamic_threshold = self.settings.value("dynamic_threshold",True, type=bool)
        startProgrammWidget.energy_threshold = self.settings.value("energy_threshold",300)
        startProgrammWidget.pause_threshold = self.settings.value("pause_threshold",0.8)
        getWether.city = self.settings.value("city_name","Volgograd")
        startProgrammWidget.recognizerType = self.settings.value("hotRecType", "Google")
        startProgrammWidget.commandrecognizerType = self.settings.value("comRecType", "Google")
        '''''
        commandFile.app_dict = self.settings.value("app_dict", defaultValue={})
        commandFile.site_dict = self.settings.value("site_dict", defaultValue={})
        print(commandFile.site_dict)
        '''
        print("LOAD")

    def save_global_data(self): # сохранение данных
        '''''
        text = self.text_edit.toPlainText()
        self.settings.setValue("text", text)

        checked = self.checkbox.isChecked()
        self.settings.setValue("checked", checked)
        '''
        hot_word = startProgrammWidget.hot_word
        self.settings.setValue("hot_word",hot_word)

        phrase_time_limit_hotword = startProgrammWidget.phrase_time_limit_hotword
        self.settings.setValue("phrase_time_limit_hotword",phrase_time_limit_hotword)

        phrase_time_limit_command = startProgrammWidget.phrase_time_limit_command
        self.settings.setValue("phrase_time_limit_command",phrase_time_limit_command)

        dynamic_threshold = startProgrammWidget.dynamic_threshold
        self.settings.setValue("dynamic_threshold",dynamic_threshold)

        energy_threshold = startProgrammWidget.energy_threshold
        self.settings.setValue("energy_threshold",energy_threshold)

        pause_threshold = startProgrammWidget.pause_threshold
        self.settings.setValue("pause_threshold",pause_threshold)

        city_name = getWether.city
        self.settings.setValue("city_name",city_name)

        recognizerType =  startProgrammWidget.recognizerType
        self.settings.setValue("hotRecType",recognizerType)

        commandrecognizerType =  startProgrammWidget.commandrecognizerType
        self.settings.setValue("comRecType",commandrecognizerType)
        '''''
        app_dict = commandFile.app_dict
        site_dict = commandFile.site_dict
        print(site_dict)
        print(commandFile.site_dict)
        self.settings.setValue("app_dict",app_dict)
        self.settings.setValue("site_dict",site_dict)
        print(site_dict)
        '''
        print("save")

        
    def closeEvent(self, e):
        self.save_global_data()
        e.accept()    
        
        

    
        #----------------------------------------------СТАРТ ПРОГРАММЫ
    


if __name__ == '__main__':
    
    app = QApplication([])
    thread = QThread()
    thread.start()

    timer = QBasicTimer()
    timer.start(1000, thread)  # Здесь 1000 - интервал времени в миллисекундах
    window = MainWindow()
    window.setAttribute(Qt.WA_DeleteOnClose)
    window.show()
    app.exec_()

