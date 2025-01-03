import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QFileDialog,
    QPushButton, QToolBar, QStatusBar, QMessageBox, QFontDialog, QColorDialog,
    QMenu, QMenuBar
)
from PyQt6.QtGui import QAction, QIcon, QTextCharFormat, QSyntaxHighlighter, QTextCursor, QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QRegularExpression

# Define Delta Design Night Theme colors
PRIMARY_DARK = '#121212'
SECONDARY_DARK = '#1E1E1E'
NIGHT_BLUE = '#2D5B9E'
NIGHT_PURPLE = '#6B4BA3'
NIGHT_TEAL = '#1C746C'
SURFACE_LIGHT = '#3A3A3A'
SURFACE_MID = '#2C2C2C'
SURFACE_DARK = '#1A1A1A'

class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Подсветка ключевых слов
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(Qt.GlobalColor.darkBlue)
        keyword_format.setFontWeight(700)
        keywords = ["def", "class", "if", "else", "for", "while", "return", "import", "from"]
        for word in keywords:
            pattern = QRegularExpression(r"\b" + word + r"\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Подсветка строк
        string_format = QTextCharFormat()
        string_format.setForeground(Qt.GlobalColor.darkGreen)
        pattern = QRegularExpression(r'\".*?\"')
        self.highlighting_rules.append((pattern, string_format))

        # Подсветка комментариев
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.GlobalColor.gray)
        pattern = QRegularExpression(r'\#.*')
        self.highlighting_rules.append((pattern, comment_format))

        # Подсветка чисел
        number_format = QTextCharFormat()
        number_format.setForeground(Qt.GlobalColor.darkMagenta)
        pattern = QRegularExpression(r'\b\d+\b')
        self.highlighting_rules.append((pattern, number_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlighting_rules:
            match = pattern.globalMatch(text)
            while match.hasNext():
                m = match.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

class NotePad(QMainWindow):

    def set_delta_design_night_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(PRIMARY_DARK))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(NIGHT_TEAL))
        palette.setColor(QPalette.ColorRole.Base, QColor(SECONDARY_DARK))
        palette.setColor(QPalette.ColorRole.Text, QColor(NIGHT_PURPLE))
        palette.setColor(QPalette.ColorRole.Button, QColor(SURFACE_LIGHT))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(NIGHT_BLUE))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(NIGHT_BLUE))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(SURFACE_LIGHT))

        self.setPalette(palette)
        self.setStyleSheet(f"""
            QToolBar {{ background-color: {SURFACE_MID}; border: none; }}
            QToolButton {{ background-color: {SURFACE_LIGHT}; border: none; }}
            QToolButton:hover {{ background-color: {SURFACE_DARK}; }}
            QMenuBar {{ background-color: {PRIMARY_DARK}; color: {NIGHT_TEAL}; }}
            QMenu {{ background-color: {SECONDARY_DARK}; color: {NIGHT_TEAL}; }}
            QMenu::item:selected {{ background-color: {NIGHT_BLUE}; }}
            QTextEdit {{ background-color: {SECONDARY_DARK}; color: {NIGHT_PURPLE}; }}
        """)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NotePad на PyQt6 с расширенной кастомизацией")
        self.setGeometry(100, 100, 800, 600)

        # Текстовый редактор
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # Подсветка синтаксиса
        self.highlighter = SyntaxHighlighter(self.text_edit.document())

        # Создаем панель инструментов
        self.create_toolbar()

        # Создаем строку состояния
        self.create_status_bar()

        # Создаем меню
        self.create_menu()

        # Инициализируем текущий файл
        self.current_file = None

        # Применяем Delta Design Night Theme
        self.set_delta_design_night_theme()

    def create_toolbar(self):
        toolbar = QToolBar("Панель инструментов")
        self.addToolBar(toolbar)

        # Кнопка "Открыть"
        open_action = QAction(QIcon.fromTheme("document-open"), "Открыть", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        # Кнопка "Сохранить"
        save_action = QAction(QIcon.fromTheme("document-save"), "Сохранить", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        # Кнопка "Сохранить как"
        save_as_action = QAction(QIcon.fromTheme("document-save-as"), "Сохранить как", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_file_as)
        toolbar.addAction(save_as_action)

        # Кнопка "Выход"
        exit_action = QAction(QIcon.fromTheme("application-exit"), "Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

        # Кнопка "Выбрать шрифт"
        font_action = QAction(QIcon.fromTheme("preferences-desktop-font"), "Выбрать шрифт", self)
        font_action.setShortcut("Ctrl+F")
        font_action.triggered.connect(self.choose_font)
        toolbar.addAction(font_action)

        # Кнопка "Выбрать цвет текста"
        color_action = QAction(QIcon.fromTheme("preferences-desktop-color"), "Выбрать цвет текста", self)
        color_action.setShortcut("Ctrl+T")
        color_action.triggered.connect(self.choose_text_color)
        toolbar.addAction(color_action)

    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"background-color: {SURFACE_MID}; color: {NIGHT_TEAL};")
        self.status_bar.showMessage("Готово", 5000)

    def create_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # Меню "Файл"
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction("Открыть", self.open_file)
        file_menu.addAction("Сохранить", self.save_file)
        file_menu.addAction("Сохранить как", self.save_file_as)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.close)

        # Меню "Вид"
        view_menu = menu_bar.addMenu("Вид")
        view_menu.addAction("Белая тема", self.set_white_theme)
        view_menu.addAction("Красная тема", self.set_red_theme)
        view_menu.addAction("Очень чёрная тема", self.set_dark_theme)
        view_menu.addAction("Синяя тема", self.set_blue_theme)
        view_menu.addAction("Зелёная тема", self.set_green_theme)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
                    self.current_file = file_path
                    self.status_bar.showMessage(f"Файл открыт: {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось открыть файл: {e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    content = self.text_edit.toPlainText()
                    file.write(content)
                    self.status_bar.showMessage(f"Файл сохранён: {self.current_file}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        # Открываем диалог для сохранения файла
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    content = self.text_edit.toPlainText()
                    file.write(content)
                    self.current_file = file_path
                    self.status_bar.showMessage(f"Файл сохранён: {file_path}", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить файл: {e}")

    def choose_font(self):
        # Выбор шрифта
        font, ok = QFontDialog.getFont(self.text_edit.currentFont(), self)
        if ok:
            self.text_edit.setCurrentFont(font)

    def choose_text_color(self):
        # Выбор цвета текста
        color = QColorDialog.getColor(self.text_edit.textColor(), self)
        if color.isValid():
            self.text_edit.setTextColor(color)

    def set_white_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        self.setPalette(palette)

    def set_red_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.darkRed)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    def set_blue_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.blue)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.darkBlue)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)

    def set_green_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.green)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.darkGreen)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        self.setPalette(palette)

    def closeEvent(self, event):
        # Проверяем, есть ли несохранённые изменения
        if self.text_edit.document().isModified():
            reply = QMessageBox.question(
                self, "Выход", "У вас есть несохранённые изменения. Вы действительно хотите выйти?",
                QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel
            )
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
