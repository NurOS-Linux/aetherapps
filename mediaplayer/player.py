from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

class PlayerWidget(QWidget):
    # Сигналы
    playback_ended = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_player()
        self.setup_ui()
        self.connect_signals()

    def setup_player(self):
        """Инициализация медиаплеера"""
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.5)  # 50% громкость по умолчанию

    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Информация о треке
        self.track_info = QLabel("Нет воспроизведения")
        self.track_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.track_info.setObjectName("track-title")
        layout.addWidget(self.track_info)

        # Прогресс воспроизведения
        progress_layout = QHBoxLayout()
        
        self.time_current = QLabel("0:00")
        self.time_current.setObjectName("time-label")
        
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setEnabled(False)
        
        self.time_total = QLabel("0:00")
        self.time_total.setObjectName("time-label")
        
        progress_layout.addWidget(self.time_current)
        progress_layout.addWidget(self.progress_slider, 1)
        progress_layout.addWidget(self.time_total)
        layout.addLayout(progress_layout)

        # Кнопки управления
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.prev_button = QPushButton("⏮")
        self.play_button = QPushButton("⏵")
        self.next_button = QPushButton("⏭")
        
        for button in [self.prev_button, self.play_button, self.next_button]:
            button.setObjectName("player-control")
            controls_layout.addWidget(button)
            
        layout.addLayout(controls_layout)

        # Громкость
        volume_layout = QHBoxLayout()
        
        volume_icon = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.setValue(50)
        
        volume_layout.addWidget(volume_icon)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addStretch()
        layout.addLayout(volume_layout)

    def connect_signals(self):
        """Подключение сигналов"""
        # Кнопки управления
        self.play_button.clicked.connect(self.play_pause)
        self.volume_slider.valueChanged.connect(
            lambda x: self.audio_output.setVolume(x / 100))
        
        # События плеера
        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)
        self.player.playbackStateChanged.connect(self.update_play_button)
        self.progress_slider.sliderMoved.connect(self.seek_position)
        
        # Обработка окончания трека
        self.player.mediaStatusChanged.connect(self.handle_media_status)

    def load_track(self, path):
        """Загрузка трека"""
        self.player.setSource(path)
        self.track_info.setText(self.get_filename_from_path(path))
        self.progress_slider.setEnabled(True)
        self.play()

    def play(self):
        """Начать воспроизведение"""
        self.player.play()

    def pause(self):
        """Поставить на паузу"""
        self.player.pause()

    def stop(self):
        """Остановить воспроизведение"""
        self.player.stop()
        self.progress_slider.setEnabled(False)
        self.track_info.setText("Нет воспроизведения")
        self.time_current.setText("0:00")
        self.time_total.setText("0:00")

    def play_pause(self):
        """Переключение воспроизведение/пауза"""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def seek_position(self, position):
        """Перемотка"""
        self.player.setPosition(position)

    def update_position(self, position):
        """Обновление текущей позиции"""
        self.progress_slider.setValue(position)
        self.time_current.setText(self.format_time(position))

    def update_duration(self, duration):
        """Обновление общей длительности"""
        self.progress_slider.setRange(0, duration)
        self.time_total.setText(self.format_time(duration))

    def update_play_button(self, state):
        """Обновление иконки кнопки воспроизведения"""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setText("⏸")
        else:
            self.play_button.setText("⏵")

    def handle_media_status(self, status):
        """Обработка статуса медиа"""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playback_ended.emit()

    def set_volume(self, volume):
        """Установка громкости"""
        self.volume_slider.setValue(int(volume * 100))
        self.audio_output.setVolume(volume)

    def get_position(self):
        """Получение текущей позиции"""
        return self.player.position()

    def get_duration(self):
        """Получение длительности трека"""
        return self.player.duration()

    def is_playing(self):
        """Проверка воспроизведения"""
        return self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState

    @staticmethod
    def format_time(ms):
        """Форматирование времени"""
        s = ms // 1000
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}:{m:02d}:{s:02d}"
        return f"{m}:{s:02d}"

    @staticmethod
    def get_filename_from_path(path):
        """Получение имени файла из пути"""
        return path.rsplit('/', 1)[-1] if '/' in path else path