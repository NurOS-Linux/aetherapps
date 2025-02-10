import sys
import os
import datetime
import getpass
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFrame, QTreeView, QMenu,
    QMessageBox, QInputDialog, QSplitter, QToolBar, QStatusBar,
    QScrollArea, QVBoxLayout, QListWidget, QListWidgetItem,
    QAbstractItemView
)
from PyQt6.QtCore import Qt, QDir, QTimer, QSize
from PyQt6.QtGui import QAction, QColor, QFileSystemModel, QIcon, QPixmap

# Цвета в стиле Modern Dark
PRIMARY_DARK = '#1a1a1a'
SECONDARY_DARK = '#2d2d2d'
ACCENT_BLUE = '#5c90ff'
SURFACE_DARK = '#3d3d3d'
HOVER_DARK = '#454545'
BUTTON_HOVER = '#4a7ae0'
BUTTON_PRESSED = '#3e68c7'

class FileIconView(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(self.widget)
        self.setStyleSheet(f"""
            background-color: {SURFACE_DARK};
            border-radius: 10px;
        """)
        self.icon_size = 64

    def clear(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def add_item(self, name, path, is_dir=False):
        item_widget = QWidget()
        item_layout = QVBoxLayout(item_widget)
        item_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        item_widget.setFixedSize(self.icon_size + 20, self.icon_size + 40)

        if is_dir:
            icon = QIcon.fromTheme("folder")
        else:
            icon = QIcon.fromTheme("text-x-generic")  # Default file icon

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(self.icon_size, self.icon_size))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text_label = QLabel(name)
        text_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        text_label.setStyleSheet("color: white;")

        item_layout.addWidget(icon_label)
        item_layout.addWidget(text_label)

        item_widget.mousePressEvent = lambda event: self.itemClicked(path)
        item_widget.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border-radius: 5px;
            }}
            &:hover {{
                background-color: {HOVER_DARK};
            }}
        """)

        self.layout.addWidget(item_widget)

    def itemClicked(self, path):
        # Handle item click event here
        print(f"Item clicked: {path}")

class AstrumFileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astrum File Manager")
        self.setMinimumSize(1000, 700)

        # 1. Центральный виджет и основной макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 2. Панель инструментов
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.setStyleSheet(f"""
            QToolBar {{
                background-color: {SECONDARY_DARK};
                border: none;
                padding: 5px;
                border-radius: 10px;
            }}
            QToolButton {{
                background-color: transparent;
                border: none;
                margin: 2px;
                border-radius: 5px;
            }}
            QToolButton:hover {{
                background-color: {HOVER_DARK};
            }}
        """)

        # Кнопки панели инструментов
        self.back_btn = self.create_action(QIcon.fromTheme("go-previous"), "Back", self.goBack)
        self.forward_btn = self.create_action(QIcon.fromTheme("go-next"), "Forward", self.goForward)
        self.up_btn = self.create_action(QIcon.fromTheme("go-up"), "Up", self.goUp)
        self.refresh_btn = self.create_action(QIcon.fromTheme("view-refresh"), "Refresh", self.refreshView)
        self.new_folder_btn = self.create_action(QIcon.fromTheme("folder-new"), "New Folder", self.createNewFolder)
        self.delete_btn = self.create_action(QIcon.fromTheme("edit-delete"), "Delete", self.deleteSelected)

        self.toolbar.addActions([self.back_btn, self.forward_btn, self.up_btn, self.refresh_btn, self.new_folder_btn, self.delete_btn])
        self.toolbar.addSeparator()

        # 3. Строка пути
        self.path_edit = QLineEdit()
        self.path_edit.setObjectName("pathEdit")
        self.path_edit.setReadOnly(True)
        self.path_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {SURFACE_DARK};
                color: white;
                border: 1px solid {ACCENT_BLUE};
                border-radius: 5px;
                padding: 5px;
            }}
        """)
        self.toolbar.addWidget(self.path_edit)

        # 4. Разделитель (Bookmarks + FileIconView)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("QSplitter::handle { background: gray; }")

        # Левая часть: Bookmarks
        self.bookmarks = QListWidget()
        self.bookmarks.setObjectName("bookmarks")
        self.bookmarks.setViewMode(QListWidget.ViewMode.ListMode)
        self.bookmarks.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.bookmarks.setSpacing(5)

        # Add bookmarks
        self.add_bookmark(QIcon.fromTheme("user-home"), "Home", QDir.homePath())
        self.add_bookmark(QIcon.fromTheme("folder-download"), "Downloads", QDir.homePath() + "/Downloads")
        self.add_bookmark(QIcon.fromTheme("folder-documents"), "Documents", QDir.homePath() + "/Documents")

        self.bookmarks.setStyleSheet(f"""
            QListWidget {{
                background-color: {SURFACE_DARK};
                color: white;
                border: none;
                border-right: 1px solid {ACCENT_BLUE};
                border-radius: 10px;
                padding: 10px;
            }}
            QListWidget::item {{
                padding: 5px;
                border-radius: 5px;
            }}
            QListWidget::item:selected {{
                background-color: {ACCENT_BLUE};
            }}
            QListWidget::item:hover {{
                background-color: {HOVER_DARK};
            }}
        """)

        # Правая часть: FileIconView
        self.file_icon_view = FileIconView()

        self.splitter.addWidget(self.bookmarks)
        self.splitter.addWidget(self.file_icon_view)
        self.splitter.setSizes([200, 800])

        # 5. Статусная строка
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {SECONDARY_DARK};
                color: white;
                border: none;
                padding: 5px;
                border-radius: 10px;
            }}
        """)

        self.items_label = QLabel("Items: 0")
        self.items_label.setObjectName("statusLabel")
        self.items_label.setStyleSheet("color: white;")

        self.date_time_label = QLabel()
        self.date_time_label.setObjectName("statusLabel")
        self.date_time_label.setStyleSheet("color: white;")

        self.user_label = QLabel()
        self.user_label.setObjectName("statusLabel")
        self.user_label.setStyleSheet("color: white;")

        self.status_bar.addWidget(self.items_label)
        self.status_bar.addPermanentWidget(self.date_time_label)
        self.status_bar.addPermanentWidget(self.user_label)

        # 6. Добавление виджетов в основной макет
        main_layout.addWidget(self.toolbar)
        main_layout.addWidget(self.splitter)

        # 7. Подключение сигналов
        self.connectSignals()

        # 8. Обновление информации о пользователе и времени
        self.updateDateTime()
        self.updateUserInfo()

        # 9. Таймер для обновления времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        # 10. Применение стилей
        self.applyStyles()

        # 11. Создание меню
        self.createMenu()

    def create_action(self, icon, tip, triggered=None):
        action = QAction(icon, tip, self)
        if triggered:
            action.triggered.connect(triggered)
        action.setStatusTip(tip)
        return action

    def add_bookmark(self, icon, name, path):
        item = QListWidgetItem(icon, name)
        item.setData(Qt.ItemDataRole.UserRole, path)
        self.bookmarks.addItem(item)

    def applyStyles(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {PRIMARY_DARK};
                border-radius: 10px;
            }}

            QMenu {{
                background-color: {SECONDARY_DARK};
                color: white;
                border: none;
                border-radius: 10px;
            }}
            QMenu::item:selected {{
                background-color: {ACCENT_BLUE};
            }}
        """)

    def connectSignals(self):
        self.back_btn.triggered.connect(self.goBack)
        self.forward_btn.triggered.connect(self.goForward)
        self.up_btn.triggered.connect(self.goUp)
        self.refresh_btn.triggered.connect(self.refreshView)
        self.new_folder_btn.triggered.connect(self.createNewFolder)
        self.delete_btn.triggered.connect(self.deleteSelected)
        self.bookmarks.itemClicked.connect(self.bookmarkClicked)
        #self.tree.clicked.connect(self.updatePath)
        #self.tree.clicked.connect(self.displayDirectoryContents)
        #self.tree.doubleClicked.connect(self.onDoubleClick)

    def createMenu(self):
        menubar = self.menuBar()
        menubar.setObjectName("menuBar")
        menubar.setStyleSheet(f"background-color: {SECONDARY_DARK}; color: white; border: none; border-radius: 10px;")

        # File
        file_menu = menubar.addMenu("File")
        file_menu.setObjectName("menu")
        file_menu.setStyleSheet(f"background-color: {SECONDARY_DARK}; color: white; border: none; border-radius: 10px;")

        new_folder = QAction("New Folder", self)
        new_folder.triggered.connect(self.createNewFolder)
        file_menu.addAction(new_folder)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.deleteSelected)
        file_menu.addAction(delete_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View
        view_menu = menubar.addMenu("View")
        view_menu.setObjectName("menu")
        view_menu.setStyleSheet(f"background-color: {SECONDARY_DARK}; color: white; border: none; border-radius: 10px;")

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refreshView)
        view_menu.addAction(refresh_action)

    def updatePath(self, path):
        self.path_edit.setText(path)
        self.updateItemCount()

    def updateItemCount(self):
        current_path = self.path_edit.text()
        if os.path.exists(current_path):
            items = len(os.listdir(current_path))
            self.items_label.setText(f"Items: {items}")
        else:
            self.items_label.setText("Items: 0")

    def goBack(self):
        current = self.tree.currentIndex()
        if current.parent().isValid():
            self.tree.setCurrentIndex(current.parent())
            self.updatePath(current.parent())
            self.displayDirectoryContents(current.parent())

    def goForward(self):
        current = self.tree.currentIndex()
        if self.model.hasChildren(current):
            child = self.model.index(0, 0, current)
            self.tree.setCurrentIndex(child)
            self.updatePath(child)
            self.displayDirectoryContents(child)

    def goUp(self):
        current = self.tree.currentIndex()
        parent = current.parent()
        if parent.isValid():
            self.tree.setCurrentIndex(parent)
            self.updatePath(parent)
            self.displayDirectoryContents(parent)

    def refreshView(self):
        self.updateItemCount()
        self.displayDirectoryContents(self.path_edit.text())

    def displayDirectoryContents(self, path):
        self.updatePath(path)

        if os.path.isdir(path):
            try:
                items = os.listdir(path)
                self.file_icon_view.clear()
                for item in items:
                    item_path = os.path.join(path, item)
                    is_dir = os.path.isdir(item_path)
                    self.file_icon_view.add_item(item, item_path, is_dir)
            except PermissionError:
                self.file_icon_view.clear()
                self.file_icon_view.add_item("Permission denied", "", False)
        else:
            self.file_icon_view.clear()
            self.file_icon_view.add_item("Select a directory to view its contents", "", False)

    def onDoubleClick(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            try:
                os.startfile(path)
            except AttributeError:
                os.system(f'xdg-open "{path}"')
            except OSError as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def createNewFolder(self):
        current_path = self.path_edit.text()
        if os.path.exists(current_path):
            name, ok = QInputDialog.getText(self, "New Folder", "Enter folder name:")
            if ok and name:
                try:
                    os.mkdir(os.path.join(current_path, name))
                    self.refreshView()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def deleteSelected(self):
        indexes = self.tree.selectedIndexes()
        if indexes:
            path = self.model.filePath(indexes[0])
            reply = QMessageBox.question(self, "Delete",
                                       f"Are you sure you want to delete {path}?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        os.rmdir(path)
                    self.refreshView()
                except Exception as e:
                    QMessageBox.critical(self, "Error", str(e))

    def updateDateTime(self):
        now = datetime.datetime.utcnow()
        self.date_time_label.setText(f"Date and Time (UTC): {now.strftime('%Y-%m-%d %H:%M:%S')}")

    def updateUserInfo(self):
        username = getpass.getuser()
        self.user_label.setText(f"User: {username}")

    def bookmarkClicked(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        self.displayDirectoryContents(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AstrumFileManager()
    window.show()
    sys.exit(app.exec())