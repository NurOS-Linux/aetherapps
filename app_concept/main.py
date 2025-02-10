import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLabel, QLineEdit, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette

class NurOSDarkWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NurOS Dark App")
        self.setMinimumSize(800, 600)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Создаем карточку
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)
        
        # Добавляем элементы в карточку
        title = QLabel("Welcome to NurOS Dark")
        title.setObjectName("title")
        
        input_field = QLineEdit()
        input_field.setPlaceholderText("Enter something...")
        input_field.setObjectName("input")
        
        action_button = QPushButton("Perform Action")
        action_button.setObjectName("actionButton")
        
        # Добавляем виджеты в layout карточки
        card_layout.addWidget(title)
        card_layout.addWidget(input_field)
        card_layout.addWidget(action_button)
        
        # Добавляем карточку в основной layout
        layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Применяем стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            #card {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                min-width: 400px;
                max-width: 400px;
            }
            
            #title {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            
            QLineEdit {
                background-color: #3d3d3d;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
                margin: 10px 0;
            }
            
            QLineEdit:focus {
                background-color: #454545;
                border: 2px solid #5c90ff;
            }
            
            QPushButton#actionButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            
            QPushButton#actionButton:hover {
                background-color: #4a7ae0;
            }
            
            QPushButton#actionButton:pressed {
                background-color: #3e68c7;
            }
        """)

def main():
    # Проверяем, что мы на Linux
    if sys.platform != 'linux':
        print("This application is designed to run only on Linux!")
        sys.exit(1)
        
    app = QApplication(sys.argv)
    
    # Устанавливаем темную тему для всего приложения
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
    
    window = NurOSDarkWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()