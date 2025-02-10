import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette, QFontDatabase

class NurOSCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setMinimumSize(400, 600)
        self.setMaximumSize(400, 600)  # Фиксированный размер окна
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Карточка калькулятора
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        
        # Дисплеи калькулятора
        display_frame = QFrame()
        display_frame.setObjectName("displayFrame")
        display_layout = QVBoxLayout()
        display_frame.setLayout(display_layout)
        
        # История вычислений
        self.history = QLabel("")
        self.history.setObjectName("history")
        self.history.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # Основной дисплей
        self.display = QLabel("0")
        self.display.setObjectName("display")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        display_layout.addWidget(self.history)
        display_layout.addWidget(self.display)
        
        # Сетка кнопок
        buttons_grid = QGridLayout()
        buttons_grid.setSpacing(8)  # Пространство между кнопками
        
        # Кнопки калькулятора
        buttons = [
            ('CE', 0, 0, "clear"), ('C', 0, 1, "clear"), ('⌫', 0, 2, "clear"), ('÷', 0, 3, "operator"),
            ('7', 1, 0, "num"), ('8', 1, 1, "num"), ('9', 1, 2, "num"), ('×', 1, 3, "operator"),
            ('4', 2, 0, "num"), ('5', 2, 1, "num"), ('6', 2, 2, "num"), ('−', 2, 3, "operator"),
            ('1', 3, 0, "num"), ('2', 3, 1, "num"), ('3', 3, 2, "num"), ('+', 3, 3, "operator"),
            ('±', 4, 0, "num"), ('0', 4, 1, "num"), ('.', 4, 2, "num"), ('=', 4, 3, "equal")
        ]
        
        for btn_text, row, col, btn_type in buttons:
            button = QPushButton(btn_text)
            button.setObjectName(f"{btn_type}Button")
            button.clicked.connect(lambda checked, text=btn_text: self.button_clicked(text))
            buttons_grid.addWidget(button, row, col)
        
        # Добавляем элементы в основной layout
        card_layout.addWidget(display_frame)
        card_layout.addLayout(buttons_grid)
        main_layout.addWidget(card)
        
        # Инициализация переменных калькулятора
        self.reset_calculator()
        
        # Применяем стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            #card {
                background-color: #2d2d2d;
                border-radius: 15px;
                padding: 20px;
            }
            
            #displayFrame {
                background-color: #1a1a1a;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 15px;
            }
            
            #display {
                color: #ffffff;
                font-size: 42px;
                font-weight: bold;
                margin: 5px;
                padding: 5px;
            }
            
            #history {
                color: #888888;
                font-size: 16px;
                margin: 5px;
                min-height: 20px;
            }
            
            QPushButton {
                font-size: 18px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                min-width: 70px;
                min-height: 70px;
            }
            
            #numButton {
                background-color: #3d3d3d;
                color: white;
            }
            
            #numButton:hover {
                background-color: #454545;
            }
            
            #numButton:pressed {
                background-color: #2d2d2d;
            }
            
            #operatorButton {
                background-color: #5c90ff;
                color: white;
            }
            
            #operatorButton:hover {
                background-color: #4a7ae0;
            }
            
            #operatorButton:pressed {
                background-color: #3e68c7;
            }
            
            #equalButton {
                background-color: #00b894;
                color: white;
            }
            
            #equalButton:hover {
                background-color: #00a383;
            }
            
            #equalButton:pressed {
                background-color: #008f72;
            }
            
            #clearButton {
                background-color: #ff5252;
                color: white;
            }
            
            #clearButton:hover {
                background-color: #ff3838;
            }
            
            #clearButton:pressed {
                background-color: #ff1f1f;
            }
        """)

    def reset_calculator(self):
        """Сброс всех переменных калькулятора"""
        self.current_number = '0'
        self.previous_number = ''
        self.operation = ''
        self.reset_next = False
        self.last_button_was_operator = False
        self.decimal_point_added = False

    def format_number(self, number_str):
        """Форматирование чисел для отображения"""
        try:
            number = float(number_str)
            if number.is_integer():
                return str(int(number))
            return f"{number:g}"  # Убирает лишние нули после точки
        except:
            return number_str

    def calculate_result(self):
        """Выполнение вычислений"""
        try:
            num1 = float(self.previous_number)
            num2 = float(self.current_number)
            
            if self.operation == '+':
                result = num1 + num2
            elif self.operation == '−':
                result = num1 - num2
            elif self.operation == '×':
                result = num1 * num2
            elif self.operation == '÷':
                if num2 == 0:
                    return 'Error'
                result = num1 / num2
            
            return self.format_number(str(result))
        except:
            return 'Error'

    def button_clicked(self, text):
        # Обработка цифр
        if text in '0123456789':
            if self.reset_next or self.current_number == '0':
                self.current_number = text
                self.reset_next = False
            else:
                self.current_number += text
            self.last_button_was_operator = False

        # Обработка десятичной точки
        elif text == '.':
            if not self.decimal_point_added:
                self.current_number += '.' if self.current_number else '0.'
                self.decimal_point_added = True
                self.last_button_was_operator = False

        # Обработка операторов
        elif text in '+-×÷−':
            if not self.last_button_was_operator:
                if self.previous_number and self.operation:
                    self.current_number = self.calculate_result()
                self.previous_number = self.current_number
                self.operation = text
                self.reset_next = True
                self.decimal_point_added = False
                self.last_button_was_operator = True
            self.history.setText(f"{self.previous_number} {self.operation}")

        # Обработка равно
        elif text == '=':
            if self.previous_number and self.operation and not self.last_button_was_operator:
                self.history.setText(f"{self.previous_number} {self.operation} {self.current_number} =")
                self.current_number = self.calculate_result()
                self.previous_number = ''
                self.operation = ''
                self.reset_next = True
                self.decimal_point_added = '.' in self.current_number

        # Обработка очистки
        elif text in ['C', 'CE']:
            self.reset_calculator()
            self.history.setText('')

        # Обработка backspace
        elif text == '⌫':
            if len(self.current_number) > 1:
                if self.current_number[-1] == '.':
                    self.decimal_point_added = False
                self.current_number = self.current_number[:-1]
            else:
                self.current_number = '0'

        # Обработка смены знака
        elif text == '±':
            if self.current_number != '0':
                if self.current_number.startswith('-'):
                    self.current_number = self.current_number[1:]
                else:
                    self.current_number = '-' + self.current_number

        # Обновление дисплея
        self.display.setText(self.current_number)

def main():
    # Проверка на Linux
    if sys.platform != 'linux':
        print("This application is designed to run only on Linux!")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    
    # Установка темной темы
    app.setStyle('Fusion')
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(26, 26, 26))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Link, QColor(92, 144, 255))
    app.setPalette(palette)
    
    calculator = NurOSCalculator()
    calculator.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()