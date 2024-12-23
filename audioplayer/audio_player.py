import sys
import os
import json
import pygame
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QFileDialog, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QSpacerItem, QSizePolicy, QScrollArea, QGridLayout, QDialog
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
from pygame import mixer

class AudioPlayer(QMainWindow):
    CONFIG_FILE = "audio_config.json"

    def __init__(self):
        super().__init__()

        self.setWindowTitle("NurOS - Audio Player")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212;")
        self.current_index = -1
        self.audio_files = []

        pygame.init()
        mixer.init()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.playButton = self.createStyledButton('Play')
        self.playButton.clicked.connect(self.playAudio)

        self.pauseButton = self.createStyledButton('Pause')
        self.pauseButton.clicked.connect(self.pauseAudio)

        self.stopButton = self.createStyledButton('Stop')
        self.stopButton.clicked.connect(self.stopAudio)

        self.prevButton = self.createStyledButton('<')
        self.prevButton.clicked.connect(self.playPrevAudio)

        self.nextButton = self.createStyledButton('>')
        self.nextButton.clicked.connect(self.playNextAudio)

        self.mainLayout.addWidget(self.playButton)
        self.mainLayout.addWidget(self.pauseButton)
        self.mainLayout.addWidget(self.stopButton)
        self.mainLayout.addWidget(self.prevButton)
        self.mainLayout.addWidget(self.nextButton)

        self.infoLabel = QLabel(self)
        self.infoLabel.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.mainLayout.addWidget(self.infoLabel, 0, Qt.AlignCenter)

        self.createMenu()
        self.loadLastOpenedAudio()

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(1000)  # update every second

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
        openAction.triggered.connect(self.openAudio)
        fileMenu.addAction(openAction)

        appMenu = menubar.addMenu("App")
        quitAction = QAction("Exit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.triggered.connect(self.close)
        appMenu.addAction(quitAction)

    def openAudio(self, fileName=None):
        if not fileName:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(
                self, "Open Audio", "", "Audio Files (*.mp3 *.wav *.ogg *.flac *.aac)", options=options
            )
        if fileName:
            directory = os.path.dirname(fileName)
            self.audio_files = [
                os.path.abspath(os.path.join(directory, f))
                for f in os.listdir(directory)
                if f.lower().endswith((".mp3", ".wav", ".ogg", ".flac", ".aac"))
            ]
            fileName = os.path.abspath(fileName)
            self.current_index = self.audio_files.index(fileName)
            self.playAudio()
            self.updateAudioInfo(fileName)
            self.saveLastOpenedAudio(fileName)

    def playAudio(self):
        if self.current_index >= 0 and self.current_index < len(self.audio_files):
            fileName = self.audio_files[self.current_index]
            try:
                mixer.music.load(fileName)
                mixer.music.play()
                self.updateAudioInfo(fileName)
                self.logAction(f"Воспроизведение аудио: {fileName}")
            except Exception as e:
                self.logAction(f"Ошибка воспроизведения аудио: {e}")

    def pauseAudio(self):
        mixer.music.pause()
        self.logAction("Пауза воспроизведения")

    def stopAudio(self):
        mixer.music.stop()
        self.logAction("Остановить воспроизведение")

    def playPrevAudio(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.playAudio()
            self.logAction(f"Воспроизведение предыдущего трека: {self.audio_files[self.current_index]}")

    def playNextAudio(self):
        if self.current_index < len(self.audio_files) - 1:
            self.current_index += 1
            self.playAudio()
            self.logAction(f"Воспроизведение следующего трека: {self.audio_files[self.current_index]}")

    def updateAudioInfo(self, fileName):
        try:
            fileSize = os.path.getsize(fileName)
            fileModifiedTime = os.path.getmtime(fileName)
            fileModifiedTime = datetime.fromtimestamp(fileModifiedTime).strftime('%Y-%m-%d %H:%M:%S')

            infoText = f"Файл: {os.path.basename(fileName)}\n"
            infoText += f"Размер: {fileSize} байт\n"
            infoText += f"Последнее изменение: {fileModifiedTime}\n"

            self.infoLabel.setText(infoText)
        except Exception as e:
            self.infoLabel.setText(f"Ошибка при загрузке информации о файле: {e}")

    def updateProgress(self):
        if mixer.music.get_busy():
            position = mixer.music.get_pos() // 1000  # get position in seconds
            total_length = mixer.Sound(self.audio_files[self.current_index]).get_length()
            self.infoLabel.setText(f"Прогресс: {position}/{total_length} секунд")

    def logAction(self, message):
        with open("audio_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()}: {message}\n")

    def saveLastOpenedAudio(self, fileName):
        with open(self.CONFIG_FILE, "w") as config_file:
            json.dump({"last_opened": fileName}, config_file)

    def loadLastOpenedAudio(self):
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
                last_opened = config.get("last_opened")
                if last_opened and os.path.exists(last_opened):
                    self.openAudio(last_opened)

def main():
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#121212"))
    palette.setColor(QPalette.WindowText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Base, QColor("#121212"))
    palette.setColor(QPalette.AlternateBase, QColor("#1E1E1E"))
    palette.setColor(QPalette.ToolTipBase, QColor("#FFFFFF"))
    palette.setColor(QPalette.ToolTipText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Text, QColor("#FFFFFF"))
    palette.setColor(QPalette.Button, QColor("#2C2C2C"))
    palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))
    palette.setColor(QPalette.BrightText, QColor("#FFFFFF"))
    palette.setColor(QPalette.Highlight, QColor("#2D5B9E"))
    palette.setColor(QPalette.HighlightedText, QColor("#FFFFFF"))

    app.setPalette(palette)

    player = AudioPlayer()
    player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
