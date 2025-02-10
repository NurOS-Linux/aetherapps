import sys
import os
import json
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QLabel, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QSpacerItem, QSizePolicy, QScrollArea, QGridLayout, QDialog,
    QFrame
)
from PyQt6.QtGui import QPixmap, QPalette, QColor, QFont, QAction
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PIL import Image, ImageEnhance, ExifTags

# Цвета из вашего дизайна
PRIMARY_DARK = '#1a1a1a'
SECONDARY_DARK = '#2d2d2d'
ACCENT_BLUE = '#5c90ff'
SURFACE_DARK = '#3d3d3d'
HOVER_DARK = '#454545'
BUTTON_HOVER = '#4a7ae0'
BUTTON_PRESSED = '#3e68c7'

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app_log.log", mode='a', encoding='utf-8')
    ]
)

class PhotoViewer(QMainWindow):
    CONFIG_FILE = "config.json"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modern Photo Viewer")
        self.setMinimumSize(800, 600)
        
        # Инициализация переменных
        self.current_index = -1
        self.image_files = []
        self.scale_factor = 1.0

        # Создаем центральный виджет с карточкой
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Создаем основную карточку
        self.card = QFrame()
        self.card.setObjectName("card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        
        # Создаем панель для фото
        self.photoPanel = QFrame()
        self.photoPanel.setObjectName("photoPanel")
        photo_layout = QHBoxLayout(self.photoPanel)
        
        # Создаем виджет для изображения
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("imageLabel")
        photo_layout.addWidget(self.label)
        
        # Добавляем кнопки навигации
        self.prevButton = self.createStyledButton('⟨')
        self.nextButton = self.createStyledButton('⟩')
        
        # Создаем контейнер для фото и кнопок
        photo_container = QHBoxLayout()
        photo_container.addWidget(self.prevButton)
        photo_container.addWidget(self.photoPanel, 1)
        photo_container.addWidget(self.nextButton)
        
        # Добавляем панель управления
        control_panel = QFrame()
        control_panel.setObjectName("controlPanel")
        control_layout = QHBoxLayout(control_panel)
        
        self.zoomInButton = self.createStyledButton('🔍+')
        self.zoomOutButton = self.createStyledButton('🔍-')
        self.fullScreenButton = self.createStyledButton('⛶')
        
        control_layout.addWidget(self.zoomInButton)
        control_layout.addWidget(self.zoomOutButton)
        control_layout.addStretch()
        control_layout.addWidget(self.fullScreenButton)
        
        # Создаем галерею миниатюр
        self.thumbnailScrollArea = QScrollArea()
        self.thumbnailScrollArea.setObjectName("thumbnailArea")
        self.thumbnailScrollArea.setWidgetResizable(True)
        self.thumbnailContainer = QWidget()
        self.thumbnailGrid = QGridLayout(self.thumbnailContainer)
        self.thumbnailScrollArea.setWidget(self.thumbnailContainer)
        
        # Добавляем информационную панель
        self.infoLabel = QLabel()
        self.infoLabel.setObjectName("infoLabel")
        
        # Собираем все в основной layout
        card_layout.addLayout(photo_container)
        card_layout.addWidget(control_panel)
        card_layout.addWidget(self.thumbnailScrollArea)
        card_layout.addWidget(self.infoLabel)
        
        main_layout.addWidget(self.card)
        
        # Подключаем сигналы
        self.connectSignals()
        
        # Применяем стили
        self.applyStyles()
        
        # Создаем меню и загружаем последнее изображение
        self.createMenu()
        self.loadLastOpenedImage()

    def createStyledButton(self, text):
        button = QPushButton(text)
        button.setObjectName("actionButton")
        return button

    def applyStyles(self):
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {PRIMARY_DARK};
            }}
            
            #card {{
                background-color: {SECONDARY_DARK};
                border-radius: 10px;
                padding: 20px;
            }}
            
            #photoPanel {{
                background-color: {SURFACE_DARK};
                border-radius: 5px;
                min-height: 400px;
            }}
            
            #actionButton {{
                background-color: {ACCENT_BLUE};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }}
            
            #actionButton:hover {{
                background-color: {BUTTON_HOVER};
            }}
            
            #actionButton:pressed {{
                background-color: {BUTTON_PRESSED};
            }}
            
            #thumbnailArea {{
                background-color: {SURFACE_DARK};
                border-radius: 5px;
                padding: 10px;
                margin-top: 10px;
            }}
            
            #imageLabel {{
                color: white;
                font-size: 14px;
            }}
            
            #infoLabel {{
                color: white;
                font-size: 12px;
                padding: 10px;
                background-color: {SURFACE_DARK};
                border-radius: 5px;
                margin-top: 10px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {SURFACE_DARK};
                height: 8px;
                border-radius: 4px;
            }}
            
            QScrollBar::handle:horizontal {{
                background-color: {ACCENT_BLUE};
                border-radius: 4px;
            }}
            
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)
        def connectSignals(self):
            self.prevButton.clicked.connect(self.showPrevImage)
        self.nextButton.clicked.connect(self.showNextImage)
        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomOutButton.clicked.connect(self.zoomOut)
        self.fullScreenButton.clicked.connect(self.showFullScreenImage)

    def createMenu(self):
        menubar = self.menuBar()
        menubar.setObjectName("menuBar")
        
        fileMenu = menubar.addMenu("File")
        fileMenu.setObjectName("menu")
        
        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openImage)
        fileMenu.addAction(openAction)
        
        fileMenu.addSeparator()
        
        exitAction = QAction("Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Добавляем информацию о времени и пользователе в строку состояния
        self.statusBar = self.statusBar()
        self.statusBar.setObjectName("statusBar")
        
        self.timeLabel = QLabel("2025-02-10 05:55:57")
        self.timeLabel.setObjectName("timeLabel")
        self.statusBar.addPermanentWidget(self.timeLabel)
        
        self.userLabel = QLabel("AnmiTaliDev")
        self.userLabel.setObjectName("userLabel")
        self.statusBar.addPermanentWidget(self.userLabel)

        # Добавляем стили для меню и статусбара
        additional_styles = f"""
            #menuBar {{
                background-color: {SECONDARY_DARK};
                color: white;
                border: none;
                padding: 5px;
            }}
            
            #menu {{
                background-color: {SECONDARY_DARK};
                color: white;
                border: none;
            }}
            
            #menu::item:selected {{
                background-color: {ACCENT_BLUE};
            }}
            
            #statusBar {{
                background-color: {SECONDARY_DARK};
                color: white;
            }}
            
            #timeLabel, #userLabel {{
                color: {ACCENT_BLUE};
                padding: 5px;
            }}
        """
        self.setStyleSheet(self.styleSheet() + additional_styles)

    def openImage(self, fileName=None):
        logging.info("Открытие изображения...")
        if not fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self, 
                "Open Image", 
                "", 
                "Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp);;All Files (*)",
                options=options
            )
        if fileName:
            logging.info(f"Изображение выбрано: {fileName}")
            directory = os.path.dirname(fileName)
            self.image_files = [
                os.path.abspath(os.path.join(directory, f))
                for f in os.listdir(directory)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"))
            ]
            fileName = os.path.abspath(fileName)
            self.current_index = self.image_files.index(fileName)
            self.showImage(fileName)
            self.updateThumbnails()
            self.saveLastOpenedImage(fileName)

    def showImage(self, fileName):
        logging.info(f"Отображение изображения: {fileName}")
        try:
            self.pixmap = QPixmap(fileName)
            if self.pixmap.isNull() and fileName.lower().endswith(".webp"):
                image = Image.open(fileName)
                image.save("temp.png")
                self.pixmap = QPixmap("temp.png")

            # Масштабируем изображение с сохранением пропорций
            label_size = self.photoPanel.size()
            scaled_pixmap = self.pixmap.scaled(
                label_size, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.label.setPixmap(scaled_pixmap)
            self.updateImageInfo(fileName, self.pixmap)
        except Exception as e:
            logging.error(f"Ошибка при загрузке изображения: {e}")

    def updateThumbnails(self):
        logging.info("Обновление миниатюр")
        # Очищаем текущие миниатюры
        for i in reversed(range(self.thumbnailGrid.count())):
            widget = self.thumbnailGrid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Создаем новые миниатюры
        for index, fileName in enumerate(self.image_files):
            frame = QFrame()
            frame.setObjectName("thumbnailFrame")
            frame_layout = QVBoxLayout(frame)
            
            thumbnail = QLabel()
            thumbnail.setObjectName("thumbnail")
            pixmap = QPixmap(fileName)
            if pixmap.isNull() and fileName.lower().endswith(".webp"):
                image = Image.open(fileName)
                image.save("temp_thumb.png")
                pixmap = QPixmap("temp_thumb.png")
            
            scaled_pixmap = pixmap.scaled(
                100, 100, 
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            thumbnail.setPixmap(scaled_pixmap)
            
            frame_layout.addWidget(thumbnail)
            
            # Добавляем стили для миниатюр
            frame.setStyleSheet(f"""
                #thumbnailFrame {{
                    background-color: {SURFACE_DARK};
                    border-radius: 5px;
                    padding: 5px;
                }}
                #thumbnailFrame:hover {{
                    background-color: {HOVER_DARK};
                }}
                #thumbnail {{
                    border: none;
                }}
            """)
            
            # Добавляем обработчик клика
            frame.mousePressEvent = lambda e, idx=index: self.thumbnailClicked(idx)
            
            # Добавляем миниатюру в сетку
            row = index // 6  # 6 миниатюр в ряд
            col = index % 6
            self.thumbnailGrid.addWidget(frame, row, col)

    def thumbnailClicked(self, index):
        logging.info(f"Клик по миниатюре: {index}")
        if 0 <= index < len(self.image_files):
            self.current_index = index
            self.showImage(self.image_files[self.current_index])
            
            # Анимация выбранной миниатюры
            animation = QPropertyAnimation(self.thumbnailGrid.itemAt(index).widget(), b"geometry")
            animation.setDuration(200)
            animation.setEasingCurve(QEasingCurve.Type.OutBack)
            start_geometry = self.thumbnailGrid.itemAt(index).widget().geometry()
            animation.setStartValue(start_geometry)
            animation.setEndValue(start_geometry)
            animation.start()

    # Остальные методы остаются без изменений, но с обновленным визуальным стилем
    def showFullScreenImage(self):
        if self.pixmap and not self.pixmap.isNull():
            dialog = FullScreenDialog(self.pixmap, self)
            dialog.setStyleSheet(f"""
                QDialog {{
                    background-color: {PRIMARY_DARK};
                }}
            """)
            dialog.exec()

class FullScreenDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent, Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowState(Qt.WindowState.WindowFullScreen)

        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setPixmap(pixmap)
        layout.addWidget(self.label)

        screen_geometry = QApplication.primaryScreen().geometry()
        screen_center = screen_geometry.center()
        
        pixmap_size = pixmap.size()
        dialog_width = pixmap_size.width()
        dialog_height = pixmap_size.height()
        
        x_pos = screen_center.x() - dialog_width // 2
        y_pos = screen_center.y() - dialog_height // 2
        self.setGeometry(x_pos, y_pos, dialog_width, dialog_height)

    def mousePressEvent(self, event):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec())