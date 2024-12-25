"""
NurOS Media Player - Main Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Media Player

Created: 2024-12-22 09:50:14 UTC
Author: AnmiTaliDev
License: GPL 3.0
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QListWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class DeltaNightTheme:
    """DeltaDesign Concept Night цветовая схема"""
    PRIMARY_DARK = "#121212"
    SECONDARY_DARK = "#1E1E1E"
    NIGHT_BLUE = "#2D5B9E"
    NIGHT_PURPLE = "#6B4BA3"
    NIGHT_TEAL = "#1C746C"
    SURFACE_LIGHT = "#3A3A3A"
    SURFACE_MID = "#2C2C2C"
    SURFACE_DARK = "#1A1A1A"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B3B3B3"


class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme = DeltaNightTheme()
        self.initUI()
        self.initPlayer()
        self.setupConnections()

    def initUI(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("NurOS Media Player")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.theme.PRIMARY_DARK};
            }}
            QLabel {{
                color: {self.theme.TEXT_PRIMARY};
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {self.theme.SECONDARY_DARK};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                border-radius: 14px;
                padding: 8px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.SURFACE_MID};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.SURFACE_DARK};
            }}
            QSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: {self.theme.SURFACE_DARK};
            }}
            QSlider::handle:horizontal {{
                background: {self.theme.NIGHT_TEAL};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QListWidget {{
                background-color: {self.theme.SECONDARY_DARK};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                border-radius: 14px;
                padding: 5px;
            }}
            QListWidget::item:selected {{
                background-color: {self.theme.NIGHT_BLUE};
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Информация о треке
        self.track_info = QLabel("Нет загруженного трека")
        self.track_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.track_info)

        # Прогресс-бар
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.progress_slider)

        # Время воспроизведения
        time_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_total = QLabel("00:00")
        time_layout.addWidget(self.time_current)
        time_layout.addStretch()
        time_layout.addWidget(self.time_total)
        layout.addLayout(time_layout)

        # Контролы воспроизведения
        controls = QHBoxLayout()
        self.prev_button = QPushButton("⏮")
        self.play_button = QPushButton("▶")
        self.next_button = QPushButton("⏭")
        self.stop_button = QPushButton("⏹")
        for button in (self.prev_button, self.play_button, self.next_button, self.stop_button):
            button.setFixedSize(40, 40)
            controls.addWidget(button)

        # Регулятор громкости
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(100)
        controls.addStretch()
        controls.addWidget(QLabel("🔊"))
        controls.addWidget(self.volume_slider)
        layout.addLayout(controls)

        # Плейлист
        self.playlist = QListWidget()
        layout.addWidget(self.playlist)

    def initPlayer(self):
        """Инициализация медиаплеера"""
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.7)
        self.current_file = None
        self.is_playing = False

    def setupConnections(self):
        """Настройка связей между компонентами"""
        self.play_button.clicked.connect(self.togglePlayback)
        self.stop_button.clicked.connect(self.stopPlayback)
        self.prev_button.clicked.connect(self.previousTrack)
        self.next_button.clicked.connect(self.nextTrack)
        self.volume_slider.valueChanged.connect(lambda x: self.audio_output.setVolume(x / 100))
        self.progress_slider.sliderMoved.connect(lambda x: self.player.setPosition(x))
        self.player.positionChanged.connect(self.updatePosition)
        self.player.durationChanged.connect(self.updateDuration)
        self.playlist.itemDoubleClicked.connect(self.playSelected)

    def togglePlayback(self):
        """Переключение воспроизведения"""
        if self.is_playing:
            self.player.pause()
            self.play_button.setText("▶")
        else:
            self.player.play()
            self.play_button.setText("⏸")
        self.is_playing = not self.is_playing

    def stopPlayback(self):
        """Остановка воспроизведения"""
        self.player.stop()
        self.play_button.setText("▶")
        self.is_playing = False

    def previousTrack(self):
        """Переход к предыдущему треку в плейлисте"""
        current_row = self.playlist.currentRow()
        if current_row > 0:
            self.playlist.setCurrentRow(current_row - 1)
            self.playSelected()

    def nextTrack(self):
        """Переход к следующему треку в плейлисте"""
        current_row = self.playlist.currentRow()
        if current_row < self.playlist.count() - 1:
            self.playlist.setCurrentRow(current_row + 1)
            self.playSelected()

    def playSelected(self):
        """Воспроизведение выбранного трека"""
        current_item = self.playlist.currentItem()
        if current_item:
            self.current_file = current_item.text()
            self.track_info.setText(f"Воспроизведение: {self.current_file}")
            self.player.setSource(QUrl.fromLocalFile(self.current_file))
            self.togglePlayback()

    def updatePosition(self, position):
        """Обновление позиции воспроизведения"""
        self.progress_slider.setValue(position)
        self.time_current.setText(self.formatTime(position))

    def updateDuration(self, duration):
        """Обновление общей длительности трека"""
        self.progress_slider.setRange(0, duration)
        self.time_total.setText(self.formatTime(duration))

    @staticmethod
    def formatTime(ms):
        """Форматирование времени в MM:SS"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"

    def dragEnterEvent(self, event):
        """Обработка начала перетаскивания файлов"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Обработка броска файлов"""
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                self.playlist.addItem(Path(file_path).name)


def main():
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
