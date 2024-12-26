import sys
import os
import json
import logging
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QAction, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QSlider, QComboBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class AudioPlayer(QMainWindow):
    CONFIG_FILE = "audio_config.json"

    def __init__(self):
        super().__init__()

        self.initLogger()

        self.setWindowTitle("NurOS - Audio Player")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #121212;")
        self.current_index = -1
        self.audio_files = []
        self.audio_data = None
        self.audio_samplerate = None
        self.audio_position = 0
        self.audio_playing = False
        self.eq_settings = {"Bass Boost": 1.2, "Treble Boost": 0.8, "Normal": 1.0}

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.mainLayout = QVBoxLayout(self.centralWidget)

        self.initUI()
        self.createMenu()
        self.initTimer()

        self.log("Application started.")

    def initLogger(self):
        logging.basicConfig(
            filename="audio_player.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        
    def initTimer(self):
        self.timer = QTimer(self)
        self.timer.setInterval(100)  # Интервал в миллисекундах
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start()
        self.log("Timer initialized.")


    def log(self, message):
        logging.info(message)

    def initUI(self):
        # Buttons Layout
        self.buttonLayout = QHBoxLayout()

        self.prevButton = self.createStyledButton('<')
        self.prevButton.clicked.connect(self.playPrevAudio)

        self.playButton = self.createStyledButton('Play')
        self.playButton.clicked.connect(self.playAudio)

        self.pauseButton = self.createStyledButton('Pause')
        self.pauseButton.clicked.connect(self.pauseAudio)

        self.stopButton = self.createStyledButton('Stop')
        self.stopButton.clicked.connect(self.stopAudio)

        self.nextButton = self.createStyledButton('>')
        self.nextButton.clicked.connect(self.playNextAudio)

        self.buttonLayout.addWidget(self.prevButton)
        self.buttonLayout.addWidget(self.playButton)
        self.buttonLayout.addWidget(self.pauseButton)
        self.buttonLayout.addWidget(self.stopButton)
        self.buttonLayout.addWidget(self.nextButton)

        self.mainLayout.addLayout(self.buttonLayout)

        # Progress Bar
        self.progressBar = QSlider(Qt.Horizontal, self)
        self.progressBar.setStyleSheet(
            """
            QSlider::groove:horizontal {
                background: #2C2C2C;
                height: 6px;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #6B4BA3;
                width: 12px;
                height: 12px;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #2D5B9E;
                border-radius: 3px;
            }
            """
        )
        self.progressBar.sliderMoved.connect(self.seekAudio)
        self.mainLayout.addWidget(self.progressBar)

        # Equalizer
        self.eqLayout = QHBoxLayout()
        self.eqLabel = QLabel("Equalizer:", self)
        self.eqLabel.setStyleSheet("color: #FFFFFF;")
        self.eqLayout.addWidget(self.eqLabel)

        self.eqComboBox = QComboBox(self)
        self.eqComboBox.setStyleSheet("color: #FFFFFF; background-color: #2C2C2C;")
        self.eqComboBox.addItems(["Normal", "Bass Boost", "Treble Boost"])
        self.eqComboBox.currentIndexChanged.connect(self.applyEqualizer)
        self.eqLayout.addWidget(self.eqComboBox)

        self.mainLayout.addLayout(self.eqLayout)

        # Info Label
        self.infoLabel = QLabel(self)
        self.infoLabel.setStyleSheet("color: #FFFFFF; font-size: 14px;")
        self.mainLayout.addWidget(self.infoLabel, 0, Qt.AlignCenter)

    def createStyledButton(self, text):
        button = QPushButton(text, self)
        button.setStyleSheet(
            """
            QPushButton {
                background-color: #2C2C2C;
                color: #FFFFFF;
                border: none;
                border-radius: 14px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3A3A3A;
            }
            QPushButton:pressed {
                background-color: #1A1A1A;
            }
            """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(2, 2)
        button.setGraphicsEffect(shadow)
        return button

    def createMenu(self):
        menubar = self.menuBar()
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

    def openAudio(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open Audio", "", "Audio Files (*.wav *.flac *.mp3)", options=options
        )
        if fileName:
            directory = os.path.dirname(fileName)
            self.audio_files = [
                os.path.abspath(os.path.join(directory, f))
                for f in os.listdir(directory)
                if f.lower().endswith((".wav", ".flac", ".mp3"))
            ]
            fileName = os.path.abspath(fileName)
            self.current_index = self.audio_files.index(fileName)
            self.loadAudio(fileName)

    def loadAudio(self, fileName):
        try:
            self.audio_data, self.audio_samplerate = sf.read(fileName, dtype='float32')
            self.audio_position = 0
            self.audio_playing = False
            self.updateAudioInfo(fileName)
            self.log(f"Loaded audio file: {fileName}")
        except Exception as e:
            self.infoLabel.setText(f"Error loading audio: {e}")
            self.log(f"Error loading audio file: {fileName} - {e}")

    def applyEqualizer(self):
        if self.audio_data is None:
            self.infoLabel.setText("No audio loaded to apply equalizer.")
            return

        selected_eq = self.eqComboBox.currentText()
        self.infoLabel.setText(f"Applying equalizer: {selected_eq}")

        # Работаем с данными напрямую
        if selected_eq == "Normal":
            # Нормальный режим (без изменений)
            pass
        elif selected_eq == "Bass Boost":
            # Усиление низких частот
            freqs = np.fft.rfft(self.audio_data, axis=0)
            freqs[:int(len(freqs) * 0.1)] *= 1.5  # Усиление нижних 10% частот
            self.audio_data = np.fft.irfft(freqs, axis=0).astype('float32')
        elif selected_eq == "Treble Boost":
            # Усиление высоких частот
            freqs = np.fft.rfft(self.audio_data, axis=0)
            freqs[int(len(freqs) * 0.9):] *= 1.5  # Усиление верхних 10% частот
            self.audio_data = np.fft.irfft(freqs, axis=0).astype('float32')

        self.log(f"Equalizer applied: {selected_eq}")



    def updateAudioInfo(self, fileName):
        fileSize = os.path.getsize(fileName)
        fileModifiedTime = os.path.getmtime(fileName)
        fileModifiedTime = datetime.fromtimestamp(fileModifiedTime).strftime('%Y-%m-%d %H:%M:%S')
        infoText = f"File: {os.path.basename(fileName)}\nSize: {fileSize} bytes\nLast Modified: {fileModifiedTime}"
        self.infoLabel.setText(infoText)

    def playPrevAudio(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.loadAudio(self.audio_files[self.current_index])
            self.playAudio()
        else:
            self.infoLabel.setText("No previous audio file.")

    def playNextAudio(self):
        if self.current_index < len(self.audio_files) - 1:
            self.current_index += 1
            self.loadAudio(self.audio_files[self.current_index])
            self.playAudio()
        else:
            self.infoLabel.setText("No next audio file.")

    def updateProgress(self):
        if self.audio_playing and self.audio_data is not None:
            progress = int((self.audio_position / len(self.audio_data)) * 100)
            self.progressBar.setValue(progress)

    def seekAudio(self, position):
        if self.audio_data is not None:
            self.audio_position = int((position / 100) * len(self.audio_data))

    def playAudio(self):
        if self.audio_data is None:
            self.infoLabel.setText("No audio loaded to play.")
            return

        if not self.audio_playing:
            self.audio_playing = True
            self.infoLabel.setText("Playing audio...")
            self.stream = sd.OutputStream(
                samplerate=self.audio_samplerate,
                channels=self.audio_data.shape[1] if self.audio_data.ndim > 1 else 1,
                callback=self.audioCallback,
            )
            self.stream.start()
            self.log("Audio playback started.")

    def pauseAudio(self):
        if self.audio_playing:
            self.audio_playing = False
            self.infoLabel.setText("Audio paused.")
            self.log("Audio playback paused.")

    def stopAudio(self):
        if self.audio_playing:
            self.audio_playing = False
            self.audio_position = 0
            self.infoLabel.setText("Audio stopped.")
            if hasattr(self, "stream"):
                self.stream.stop()
                self.stream.close()
            self.log("Audio playback stopped.")


    def audioCallback(self, outdata, frames, time, status):
        if not self.audio_playing or self.audio_data is None:
            outdata.fill(0)
            return

        start = self.audio_position
        end = start + frames
        if end > len(self.audio_data):
            end = len(self.audio_data)
            outdata[:end - start] = self.audio_data[start:end]
            outdata[end - start:] = 0
            self.stopAudio()  # Останавливаем воспроизведение в конце
        else:
            outdata[:] = self.audio_data[start:end]
            self.audio_position += frames


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = AudioPlayer()
    player.show()
    sys.exit(app.exec_())
