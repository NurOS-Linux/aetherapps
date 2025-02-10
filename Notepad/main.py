import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, 
    QFileDialog, QPushButton, QToolBar, QStatusBar, QMessageBox, 
    QFontDialog, QColorDialog, QMenu, QMenuBar, QFrame
)
from PyQt6.QtGui import QAction, QTextCharFormat, QSyntaxHighlighter, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QRegularExpression

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        formats = {
            'keyword': (QColor("#5c90ff"), 700, r"\b(def|class|if|else|for|while|return|import|from)\b"),
            'string': (QColor("#4a7ae0"), 400, r'\".*?\"'),
            'comment': (QColor("#666666"), 400, r'\#.*'),
            'number': (QColor("#3e68c7"), 400, r'\b\d+\b')
        }
        for name, (color, weight, pattern) in formats.items():
            text_format = QTextCharFormat()
            text_format.setForeground(color)
            text_format.setFontWeight(weight)
            self.highlighting_rules.append((QRegularExpression(pattern), text_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            for match in pattern.globalMatch(text):
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

class NotePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NurOS Dark NotePad")
        self.setMinimumSize(800, 600)
        self.current_file = None

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Создаем карточку для текстового редактора
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)

        # Текстовый редактор
        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("editor")
        card_layout.addWidget(self.text_edit)

        # Добавляем карточку в основной layout
        main_layout.addWidget(card)

        # Подсветка синтаксиса
        self.highlighter = SyntaxHighlighter(self.text_edit.document())

        # Создаем интерфейс
        self.create_ui()
        self.apply_NurOS_dark_theme()

    def create_ui(self):
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        toolbar.setObjectName("toolbar")

        actions = {
            "Открыть": ("📂", "Ctrl+O", self.open_file),
            "Сохранить": ("💾", "Ctrl+S", self.save_file),
            "Сохранить как": ("📋", "Ctrl+Shift+S", self.save_file_as),
            "Шрифт": ("🔤", "Ctrl+F", self.choose_font),
            "Цвет": ("🎨", "Ctrl+T", self.choose_text_color),
            "Выход": ("❌", "Ctrl+Q", self.close)
        }

        for name, (icon, shortcut, slot) in actions.items():
            action = QAction(name, self)
            action.setText(icon)
            action.setToolTip(name)
            action.setShortcut(shortcut)
            action.triggered.connect(slot)
            toolbar.addAction(action)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setObjectName("statusbar")
        self.status_bar.showMessage("Готово")

        # Menu
        menu_bar = self.menuBar()
        menu_bar.setObjectName("menubar")
        
        file_menu = menu_bar.addMenu("Файл")
        view_menu = menu_bar.addMenu("Вид")

        file_actions = [
            ("Открыть", self.open_file),
            ("Сохранить", self.save_file),
            ("Сохранить как", self.save_file_as),
            (None, None),
            ("Выход", self.close)
        ]

        theme_actions = [
            ("Тёмная тема", self.apply_NurOS_dark_theme),
            ("Светлая тема", self.apply_NurOS_light_theme)
        ]

        for menu, actions in [(file_menu, file_actions), (view_menu, theme_actions)]:
            for text, slot in actions:
                if text is None:
                    menu.addSeparator()
                else:
                    menu.addAction(text, slot)

    def apply_NurOS_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            #card {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
            }
            
            #editor {
                background-color: #3d3d3d;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
            }
            
            #editor:focus {
                background-color: #454545;
                border: 2px solid #5c90ff;
            }
            
            #toolbar {
                background-color: #2d2d2d;
                border: none;
                padding: 10px;
                spacing: 5px;
            }
            
            QToolButton {
                background-color: #3d3d3d;
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            
            QToolButton:hover {
                background-color: #4a7ae0;
            }
            
            #menubar {
                background-color: #2d2d2d;
                color: white;
            }
            
            QMenu {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #3d3d3d;
            }
            
            QMenu::item:selected {
                background-color: #5c90ff;
            }
            
            #statusbar {
                background-color: #2d2d2d;
                color: white;
            }
        """)

    def apply_NurOS_light_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            
            #card {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin: 20px;
            }
            
            #editor {
                background-color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #333333;
                font-size: 14px;
            }
            
            #editor:focus {
                border: 2px solid #5c90ff;
            }
            
            #toolbar {
                background-color: white;
                border: none;
                padding: 10px;
                spacing: 5px;
            }
            
            QToolButton {
                background-color: #f5f5f5;
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: #333333;
            }
            
            QToolButton:hover {
                background-color: #e0e0e0;
            }
            
            #menubar {
                background-color: white;
                color: #333333;
            }
            
            QMenu {
                background-color: white;
                color: #333333;
                border: 1px solid #e0e0e0;
            }
            
            QMenu::item:selected {
                background-color: #5c90ff;
                color: white;
            }
            
            #statusbar {
                background-color: white;
                color: #333333;
            }
        """)

    # Остальные методы остаются без изменений
    def file_dialog(self, save=False):
        dialog = QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName
        return dialog(self, "Сохранить файл" if save else "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")[0]

    def open_file(self):
        if path := self.file_dialog():
            try:
                with open(path, "r", encoding="utf-8") as file:
                    self.text_edit.setPlainText(file.read())
                    self.current_file = path
                    self.status_bar.showMessage(f"Файл открыт: {path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {e}")

    def save_file(self):
        if not self.current_file:
            self.save_file_as()
        else:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toPlainText())
                    self.status_bar.showMessage(f"Файл сохранён: {self.current_file}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")

    def save_file_as(self):
        if path := self.file_dialog(save=True):
            self.current_file = path
            self.save_file()

    def choose_font(self):
        if (font := QFontDialog.getFont(self.text_edit.currentFont(), self))[1]:
            self.text_edit.setCurrentFont(font[0])

    def choose_text_color(self):
        if (color := QColorDialog.getColor(self.text_edit.textColor(), self)).isValid():
            self.text_edit.setTextColor(color)

    def closeEvent(self, event):
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(self, "Выход", 
                "У вас есть несохранённые изменения. Сохранить?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel)
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
                event.accept()
            elif reply == QMessageBox.StandardButton.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notepad = NotePad()
    notepad.show()
    sys.exit(app.exec())