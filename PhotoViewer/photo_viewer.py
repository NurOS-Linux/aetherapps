import sys
import os
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QAction, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QMenu
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NurOS - Просмотр Фото")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2E3436;")
        self.current_index = -1
        self.image_files = []

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.photoPanel = QWidget(self)
        self.photoPanel.setStyleSheet("background-color: #1C1C1C;")
        self.photoPanel.setFixedSize(400, 300)

        self.photoLayout = QHBoxLayout(self.photoPanel)
        self.photoLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(self.photoPanel)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #FFFFFF;")
        self.photoLayout.addWidget(self.label)

        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.photoPanel, 0, Qt.AlignCenter)
        self.mainLayout.addStretch()

        self.infoLabel = QLabel(self)
        self.infoLabel.setStyleSheet("color: #FFFFFF;")
        self.mainLayout.addWidget(self.infoLabel, 0, Qt.AlignCenter)

        self.buttonLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.prevButton = QPushButton('<', self)
        self.prevButton.clicked.connect(self.showPrevImage)
        self.prevButton.setStyleSheet("background-color: #1C1C1C; color: #FFFFFF;")
        self.buttonLayout.addWidget(self.prevButton)

        self.nextButton = QPushButton('>', self)
        self.nextButton.clicked.connect(self.showNextImage)
        self.nextButton.setStyleSheet("background-color: #1C1C1C; color: #FFFFFF;")
        self.buttonLayout.addWidget(self.nextButton)

        self.createMenu()

    def createMenu(self):
        menubar = self.menuBar()
        menubar.clear()

        fileMenu = menubar.addMenu("Файл")
        openAction = QAction("Открыть", self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.openImage)
        fileMenu.addAction(openAction)

        appMenu = menubar.addMenu("Программа")
        quitAction = QAction("Выход", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        appMenu.addAction(quitAction)

    def openImage(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Открыть изображение", "", "Все файлы (*);;Изображения (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            directory = os.path.dirname(fileName)
            self.image_files = [os.path.abspath(os.path.join(directory, f)) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
            fileName = os.path.abspath(fileName)
            self.current_index = self.image_files.index(fileName)
            self.showImage(fileName)

    def showImage(self, fileName):
        pixmap = QPixmap(fileName)
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)
        self.updateImageInfo(pixmap)

    def updateImageInfo(self, pixmap):
        imageSize = pixmap.size()
        fileWidth = imageSize.width()
        fileHeight = imageSize.height()
        aspectRatio = fileWidth / fileHeight

        infoText = f"Размер изображения: {fileWidth}x{fileHeight} пикселей\n"
        infoText += f"Соотношение сторон: {aspectRatio:.2f}"

        self.infoLabel.setText(infoText)

    def showPrevImage(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.showImage(self.image_files[self.current_index])

    def showNextImage(self):
        if self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.showImage(self.image_files[self.current_index])

def main():
    global app
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#2E3436"))
    palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Base, QColor("#2E3436"))
    palette.setColor(QPalette.AlternateBase, QColor("#2E3436"))
    palette.setColor(QPalette.ToolTipBase, QColor("#FFFFFF"))
    palette.setColor(QPalette.ToolTipText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Text, QColor("#FFFFFF"))
    palette.setColor(QPalette.Button, QColor("#2E3436"))
    palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
    palette.setColor(QPalette.BrightText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Highlight, QColor("#729FCF"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))

    app.setPalette(palette)

    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
