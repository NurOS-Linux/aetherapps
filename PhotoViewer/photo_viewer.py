import sys
import os
import json
import logging
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QFileDialog, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QSpacerItem, QSizePolicy, QScrollArea, QGridLayout, QDialog
)
from PyQt5.QtGui import QPixmap, QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PIL import Image, ImageEnhance, ExifTags

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Вывод логов в консоль
        logging.FileHandler("app_log.log", mode='a', encoding='utf-8')  # Запись логов в файл
    ]
)

class PhotoViewer(QMainWindow):
    CONFIG_FILE = "config.json"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NurOS - Photo Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")
        self.current_index = -1
        self.image_files = []
        self.scale_factor = 1.0

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.photoPanel = QWidget(self)
        self.photoPanel.setStyleSheet("background-color: #1E1E1E; border-radius: 10px;")

        self.photoLayout = QHBoxLayout(self.photoPanel)
        self.photoLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.photoPanel)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #FFFFFF;")
        self.label.setScaledContents(True)
        self.photoLayout.addWidget(self.label)

        self.mainLayout.addStretch()

        self.prevButton = self.createStyledButton('<')
        self.prevButton.clicked.connect(self.showPrevImage)

        self.nextButton = self.createStyledButton('>')
        self.nextButton.clicked.connect(self.showNextImage)

        self.zoomInButton = self.createStyledButton('Zoom In')
        self.zoomInButton.clicked.connect(self.zoomIn)

        self.zoomOutButton = self.createStyledButton('Zoom Out')
        self.zoomOutButton.clicked.connect(self.zoomOut)

        self.fullScreenButton = self.createStyledButton('Fullscreen')
        self.fullScreenButton.clicked.connect(self.showFullScreenImage)

        self.photoPanelContainer = QHBoxLayout()
        self.photoPanelContainer.addWidget(self.prevButton, 0, Qt.AlignVCenter)
        self.photoPanelContainer.addWidget(self.photoPanel, 1, Qt.AlignCenter)
        self.photoPanelContainer.addWidget(self.nextButton, 0, Qt.AlignVCenter)
        self.mainLayout.addLayout(self.photoPanelContainer)

        self.mainLayout.addStretch()

        self.zoomLayout = QHBoxLayout()
        self.zoomLayout.addWidget(self.zoomInButton)
        self.zoomLayout.addWidget(self.zoomOutButton)
        self.mainLayout.addLayout(self.zoomLayout)

        self.fullScreenLayout = QHBoxLayout()
        self.fullScreenLayout.addStretch()
        self.fullScreenLayout.addWidget(self.fullScreenButton, 0, Qt.AlignRight | Qt.AlignBottom)
        self.mainLayout.addLayout(self.fullScreenLayout)

        self.thumbnailLayout = QHBoxLayout()
        self.thumbnailScrollArea = QScrollArea(self)
        self.thumbnailScrollArea.setWidgetResizable(True)
        self.thumbnailScrollArea.setStyleSheet("background-color: #1E1E1E; border-radius: 10px;")
        self.thumbnailContainer = QWidget()
        self.thumbnailGrid = QGridLayout(self.thumbnailContainer)
        self.thumbnailScrollArea.setWidget(self.thumbnailContainer)
        self.thumbnailLayout.addWidget(self.thumbnailScrollArea)
        self.mainLayout.addLayout(self.thumbnailLayout)

        self.infoLabel = QLabel(self)
        self.infoLabel.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.mainLayout.addWidget(self.infoLabel, 0, Qt.AlignCenter)

        self.createMenu()
        self.loadLastOpenedImage()

    def createStyledButton(self, text):
        button = QPushButton(text, self)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #2C2C2C;
                color: #FFFFFF;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3A3A3A;
            }
            QPushButton:pressed {
                background-color: #1A1A1A;
            }
            """
        )
        return button

    def createMenu(self):
        menubar = self.menuBar()
        menubar.clear()

        fileMenu = menubar.addMenu("File")
        openAction = QAction("Open", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openImage)
        fileMenu.addAction(openAction)

        appMenu = menubar.addMenu("App")
        quitAction = QAction("Exit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        appMenu.addAction(quitAction)

    def openImage(self, fileName=None):
        logging.info("Открытие изображения...")
        if not fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self, "Open Image", "", "All Files (*);;Images (*.png *.jpg *.jpeg *.bmp *.gif *.webp)", options=options
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

            self.scale_factor = min(1.0, 512 / max(self.pixmap.width(), self.pixmap.height()))
            self.label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.scale_factor, Qt.KeepAspectRatio))
            self.updateImageInfo(fileName, self.pixmap)
        except Exception as e:
            logging.error(f"Ошибка при загрузке изображения: {e}")

    def zoomIn(self):
        logging.info("Увеличение масштаба изображения")
        if self.pixmap and not self.pixmap.isNull():
            self.scale_factor *= 1.2
            self.label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.scale_factor, Qt.KeepAspectRatio))

    def zoomOut(self):
        logging.info("Уменьшение масштаба изображения")
        if self.pixmap and not self.pixmap.isNull():
            self.scale_factor /= 1.2
            self.label.setPixmap(self.pixmap.scaled(self.pixmap.size() * self.scale_factor, Qt.KeepAspectRatio))

    def showFullScreenImage(self):
        logging.info("Открытие изображения на весь экран")
        if self.pixmap and not self.pixmap.isNull():
            dialog = FullScreenDialog(self.pixmap, self)
            dialog.exec()

    def updateThumbnails(self):
        logging.info("Обновление миниатюр")
        for i in reversed(range(self.thumbnailGrid.count())):
            widget = self.thumbnailGrid.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        for index, fileName in enumerate(self.image_files):
            thumbnail = QPixmap(fileName)
            if thumbnail.isNull() and fileName.lower().endswith(".webp"):
                image = Image.open(fileName)
                image.save("temp_thumb.png")
                thumbnail = QPixmap("temp_thumb.png")

            thumbLabel = QLabel()
            thumbLabel.setPixmap(thumbnail.scaled(64, 64, Qt.KeepAspectRatio))
            thumbLabel.mousePressEvent = lambda event, idx=index: self.thumbnailClicked(idx)
            self.thumbnailGrid.addWidget(thumbLabel, 0, index)

    def thumbnailClicked(self, index):
        logging.info(f"Клик по миниатюре: {index}")
        if 0 <= index < len(self.image_files):
            self.current_index = index
            self.showImage(self.image_files[self.current_index])

    def updateImageInfo(self, fileName, pixmap):
        logging.info(f"Обновление информации о изображении: {fileName}")
        if not pixmap or pixmap.isNull():
            self.infoLabel.setText("No image loaded.")
            return

        imageSize = pixmap.size()
        fileWidth = imageSize.width()
        fileHeight = imageSize.height()
        aspectRatio = fileWidth / fileHeight

        img = Image.open(fileName)
        bitDepth = img.mode
        fileSize = os.path.getsize(fileName)
        fileModifiedTime = datetime.fromtimestamp(os.path.getmtime(fileName)).strftime('%Y-%m-%d %H:%M:%S')
        dpi = img.info.get('dpi', (72, 72))
        gps_info = self.getGPSInfo(img)

        infoText = f"Size: {fileWidth}x{fileHeight} pixels\n"
        infoText += f"Aspect Ratio: {aspectRatio:.2f}\n"
        infoText += f"Bit Depth: {bitDepth}\n"
        infoText += f"Last Modified: {fileModifiedTime}\n"
        infoText += f"File Size: {fileSize} bytes\n"
        infoText += f"DPI: {dpi[0]}\n"
        infoText += gps_info

        self.infoLabel.setText(infoText)

    def getGPSInfo(self, img):
        try:
            exif = img._getexif()
            if not exif:
                return "No GPS Info.\n"

            gps_info = exif.get(ExifTags.TAGS.get("GPSInfo"))
            if not gps_info:
                return "No GPS Info.\n"

            return f"GPS Info: {gps_info}\n"
        except Exception as e:
            return "Error retrieving GPS Info.\n"

    def showPrevImage(self):
        logging.info("Предыдущее изображение")
        if self.current_index > 0:
            self.current_index -= 1
            self.showImage(self.image_files[self.current_index])

    def showNextImage(self):
        logging.info("Следующее изображение")
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.showImage(self.image_files[self.current_index])

    def saveLastOpenedImage(self, fileName):
        logging.info(f"Сохранение последнего открытого изображения: {fileName}")
        with open(self.CONFIG_FILE, "w") as config_file:
            json.dump({"last_opened": fileName}, config_file)

    def loadLastOpenedImage(self):
        logging.info("Загрузка последнего открытого изображения")
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
                last_opened = config.get("last_opened")
                if last_opened and os.path.exists(last_opened):
                    self.openImage(last_opened)

class FullScreenDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")
        self.setWindowState(Qt.WindowFullScreen)

        layout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setPixmap(pixmap)
        layout.addWidget(self.label)

        # Центрируем окно
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_center = screen_geometry.center()

        pixmap_size = pixmap.size()
        dialog_width = pixmap_size.width()
        dialog_height = pixmap_size.height()

        x_pos = screen_center.x() - dialog_width // 2
        y_pos = screen_center.y() - dialog_height // 2
        self.setGeometry(x_pos, y_pos, dialog_width, dialog_height)

    def mousePressEvent(self, event):
        self.close()  # Закрытие диалога при клике на изображение

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())
