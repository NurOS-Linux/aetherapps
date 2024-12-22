"""
NurOS Media Player - Player Controls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Player Controls Implementation

Created: 2024-12-22 10:47:42 UTC
Author: AnmiTaliDev
License: GPL 3
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QSlider, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from .. import logger
from . import UiConstants, ui_style
from ..player import MediaPlayerCore

class PlayerControls(QFrame):
    """
    Виджет элементов управления плеером в стиле DeltaDesign Concept Night.
    Включает кнопки управления, слайдеры прогресса и громкости.
    """

    def __init__(self):
        super().__init__()
        self.player = None
        self.update_timer = QTimer()
        self.update_timer.setInterval(100)
        self.is_seeking = False
        
        self.init_ui()
        self.setup_connections()
        logger.info("Player controls initialized")

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        self.setObjectName("playerControls")
        
        # Основной layout
        layout = QVBoxLayout(self)
        layout.setSpacing(UiConstants.PADDING['medium'])

        # Прогресс бар и время
        progress_layout = QVBoxLayout()
        
        # Слайдер прогресса
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setObjectName("progressSlider")
        progress_layout.addWidget(self.progress_slider)

        # Время воспроизведения
        time_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_total = QLabel("00:00")
        time_layout.addWidget(self.time_current)
        time_layout.addStretch()
        time_layout.addWidget(self.time_total)
        progress_layout.addLayout(time_layout)
        
        layout.addLayout(progress_layout)

        # Кнопки управления
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(UiConstants.PADDING['large'])

        # Создание кнопок
        self.prev_button = self.create_control_button("⏮", "Предыдущий трек")
        self.play_button = self.create_control_button("▶", "Воспроизвести")
        self.stop_button = self.create_control_button("⏹", "Остановить")
        self.next_button = self.create_control_button("⏭", "Следующий трек")

        # Добавление кнопок в layout
        for button in (self.prev_button, self.play_button, 
                      self.stop_button, self.next_button):
            controls_layout.addWidget(button)

        # Регулятор громкости
        volume_layout = QHBoxLayout()
        volume_icon = QLabel("🔊")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(UiConstants.VOLUME_SLIDER_WIDTH)

        volume_layout.addStretch()
        volume_layout.addWidget(volume_icon)
        volume_layout.addWidget(self.volume_slider)

        controls_layout.addLayout(volume_layout)
        layout.addLayout(controls_layout)

    def create_control_button(self, text: str, tooltip: str) -> QPushButton:
        """Создание кнопки управления с заданными параметрами."""
        button = QPushButton(text)
        button.setFixedSize(UiConstants.BUTTON_SIZE)
        button.setToolTip(tooltip)
        return button

    def setup_connections(self):
        """Настройка сигналов и слотов."""
        # Слайдер прогресса
        self.progress_slider.sliderPressed.connect(self.on_seek_start)
        self.progress_slider.sliderReleased.connect(self.on_seek_end)
        self.progress_slider.sliderMoved.connect(self.on_seek_move)
        
        # Обновление времени
        self.update_timer.timeout.connect(self.update_time)

    def connect_player(self, player: MediaPlayerCore):
        """Подключение к медиаплееру."""
        self.player = player
        
        # Кнопки управления
        self.play_button.clicked.connect(self.toggle_playback)
        self.stop_button.clicked.connect(player.stop)
        self.prev_button.clicked.connect(player.previous_track)
        self.next_button.clicked.connect(player.next_track)
        
        # Громкость
        self.volume_slider.valueChanged.connect(lambda v: setattr(player, 'volume', v / 100))
        
        # Сигналы плеера
        player.stateChanged.connect(self.on_state_changed)
        player.positionChanged.connect(self.update_position)
        player.durationChanged.connect(self.update_duration)
        
        # Запуск таймера обновления
        self.update_timer.start()

    def toggle_playback(self):
        """Переключение воспроизведения."""
        if self.player:
            if self.player.is_playing:
                self.player.pause()
            else:
                self.player.play()

    def on_state_changed(self, is_playing: bool):
        """Обработка изменения состояния воспроизведения."""
        self.play_button.setText("⏸" if is_playing else "▶")

    def on_seek_start(self):
        """Начало перемотки."""
        self.is_seeking = True

    def on_seek_move(self, position: int):
        """Обработка перемотки."""
        self.time_current.setText(self.format_time(position))

    def on_seek_end(self):
        """Окончание перемотки."""
        if self.player:
            self.player.seek(self.progress_slider.value())
        self.is_seeking = False

    def update_position(self, position: int):
        """Обновление позиции воспроизведения."""
        if not self.is_seeking:
            self.progress_slider.setValue(position)
            self.time_current.setText(self.format_time(position))

    def update_duration(self, duration: int):
        """Обновление общей длительности."""
        self.progress_slider.setRange(0, duration)
        self.time_total.setText(self.format_time(duration))

    def update_time(self):
        """Обновление времени воспроизведения."""
        if self.player and self.player.is_playing and not self.is_seeking:
            position = self.player.position
            self.time_current.setText(self.format_time(position))

    @staticmethod
    def format_time(ms: int) -> str:
        """Форматирование времени в MM:SS."""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"