import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                            QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QSlider, QListWidget, QFileDialog)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import os

class SpotifyClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mediaplayer")
        self.setFixedSize(1200, 800)
        
        # Инициализация плеера
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        # Состояние плеера
        self.playlist = []
        self.current_track = 0
        
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Основной контент
        content = QHBoxLayout()
        
        # Левая панель (плейлист)
        playlist_panel = QWidget()
        playlist_layout = QVBoxLayout(playlist_panel)
        
        self.playlist_widget = QListWidget()
        self.playlist_widget.setMinimumWidth(300)
        
        playlist_controls = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.remove_button = QPushButton("Удалить")
        playlist_controls.addWidget(self.add_button)
        playlist_controls.addWidget(self.remove_button)
        
        playlist_layout.addWidget(self.playlist_widget)
        playlist_layout.addLayout(playlist_controls)
        content.addWidget(playlist_panel)
        
        # Правая панель (плеер)
        player_panel = QWidget()
        player_layout = QVBoxLayout(player_panel)
        
        # Информация о треке
        self.track_info = QLabel("Нет воспроизведения")
        self.track_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_info.setStyleSheet("font-size: 18px; font-weight: bold; margin: 20px;")
        player_layout.addWidget(self.track_info)
        
        # Прогресс
        progress_layout = QHBoxLayout()
        self.time_label = QLabel("0:00")
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_label = QLabel("0:00")
        
        progress_layout.addWidget(self.time_label)
        progress_layout.addWidget(self.progress_slider)
        progress_layout.addWidget(self.duration_label)
        player_layout.addLayout(progress_layout)
        
        # Контролы воспроизведения
        controls_layout = QHBoxLayout()
        self.prev_button = QPushButton("⏮")
        self.play_button = QPushButton("⏵")
        self.next_button = QPushButton("⏭")
        
        for button in [self.prev_button, self.play_button, self.next_button]:
            button.setFixedSize(50, 50)
            controls_layout.addWidget(button)
            
        player_layout.addLayout(controls_layout)
        
        # Громкость
        volume_layout = QHBoxLayout()
        volume_label = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.setValue(50)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addStretch()
        player_layout.addLayout(volume_layout)
        
        content.addWidget(player_panel)
        layout.addLayout(content)
        
        self.apply_styles()

    def setup_connections(self):
        # Плейлист
        self.add_button.clicked.connect(self.add_files)
        self.remove_button.clicked.connect(self.remove_selected)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected)
        
        # Контролы
        self.play_button.clicked.connect(self.play_pause)
        self.prev_button.clicked.connect(self.play_previous)
        self.next_button.clicked.connect(self.play_next)
        self.volume_slider.valueChanged.connect(
            lambda x: self.audio_output.setVolume(x / 100))
        
        # События плеера
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.progress_slider.sliderMoved.connect(self.set_position)

    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите аудиофайлы",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.m4a *.flac)"
        )
        
        for file in files:
            self.playlist.append(file)
            self.playlist_widget.addItem(os.path.basename(file))

    def remove_selected(self):
        current = self.playlist_widget.currentRow()
        if current >= 0:
            self.playlist_widget.takeItem(current)
            self.playlist.pop(current)
            if current == self.current_track:
                self.player.stop()
                self.track_info.setText("Нет воспроизведения")

    def play_selected(self):
        current = self.playlist_widget.currentRow()
        if current >= 0:
            self.current_track = current
            self.play_current()

    def play_pause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.play_button.setText("⏵")
        else:
            if self.player.position() == 0 and not self.playlist:
                return
            self.player.play()
            self.play_button.setText("⏸")

    def play_previous(self):
        if self.playlist:
            self.current_track = (self.current_track - 1) % len(self.playlist)
            self.play_current()

    def play_next(self):
        if self.playlist:
            self.current_track = (self.current_track + 1) % len(self.playlist)
            self.play_current()

    def play_current(self):
        if 0 <= self.current_track < len(self.playlist):
            self.player.setSource(QUrl.fromLocalFile(self.playlist[self.current_track]))
            self.player.play()
            self.play_button.setText("⏸")
            self.track_info.setText(os.path.basename(self.playlist[self.current_track]))
            self.playlist_widget.setCurrentRow(self.current_track)

    def set_position(self, position):
        self.player.setPosition(position)

    def update_position(self, position):
        self.progress_slider.setValue(position)
        self.time_label.setText(self.format_time(position))

    def update_duration(self, duration):
        self.progress_slider.setRange(0, duration)
        self.duration_label.setText(self.format_time(duration))

    def format_time(self, ms):
        s = ms // 1000
        m, s = divmod(s, 60)
        return f"{m}:{s:02d}"

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #121212;
                color: white;
            }
            QPushButton {
                background-color: #1db954;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
            QListWidget {
                background-color: #282828;
                border-radius: 10px;
                padding: 10px;
            }
            QListWidget::item {
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QListWidget::item:selected {
                background-color: #1db954;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: #404040;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #1db954;
                border: none;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #1ed760;
            }
            QLabel {
                color: white;
            }
        """)

def main():
    app = QApplication(sys.argv)
    window = SpotifyClone()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()