"""
NurOS Media Player - Player Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Core media player functionality with DeltaDesign Concept Night integration.

Created: 2024-12-22 09:55:02 UTC
Author: NurOS
License: GPL 3
"""

import logging
from pathlib import Path
from typing import Optional, List, Dict
from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData

from . import DeltaNightTheme, PlayerSettings, logger

class MediaPlayerCore(QObject):
    """
    Ядро медиаплеера с поддержкой DeltaDesign Concept Night.
    Обрабатывает воспроизведение медиа и управление аудио.
    """

    # Сигналы для обновления UI
    trackChanged = pyqtSignal(str)  # Новый трек загружен
    stateChanged = pyqtSignal(bool)  # Изменение состояния воспроизведения
    positionChanged = pyqtSignal(int)  # Изменение позиции
    durationChanged = pyqtSignal(int)  # Изменение длительности
    volumeChanged = pyqtSignal(float)  # Изменение громкости
    errorOccurred = pyqtSignal(str)  # Ошибка воспроизведения
    metadataChanged = pyqtSignal(dict)  # Изменение метаданных

    def __init__(self):
        super().__init__()
        
        # Инициализация компонентов
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)
        
        # Состояние плеера
        self._current_track: Optional[Path] = None
        self._is_playing: bool = False
        self._volume: float = PlayerSettings.AUDIO['volume']
        self._metadata: Dict = {}
        
        # Fade эффект
        self._fade_timer = QTimer()
        self._fade_timer.setInterval(50)
        self._fade_timer.timeout.connect(self._handle_fade)
        
        # Настройка связей
        self._setup_connections()
        
        logger.info("MediaPlayerCore initialized")

    def _setup_connections(self):
        """Настройка обработчиков событий."""
        self._player.errorOccurred.connect(self._handle_error)
        self._player.positionChanged.connect(self.positionChanged.emit)
        self._player.durationChanged.connect(self.durationChanged.emit)
        self._player.metaDataChanged.connect(self._handle_metadata)

    def load_track(self, file_path: Path) -> bool:
        """Загрузка трека для воспроизведения."""
        if not file_path.exists():
            self.errorOccurred.emit(f"File not found: {file_path}")
            return False
            
        if file_path.suffix.lower() not in PlayerSettings.FORMATS:
            self.errorOccurred.emit(f"Unsupported format: {file_path.suffix}")
            return False

        try:
            self._player.setSource(QUrl.fromLocalFile(str(file_path)))
            self._current_track = file_path
            self.trackChanged.emit(file_path.name)
            logger.info(f"Loaded track: {file_path.name}")
            return True
            
        except Exception as e:
            self.errorOccurred.emit(f"Failed to load track: {str(e)}")
            logger.error(f"Track loading error: {str(e)}")
            return False

    def play(self):
        """Начать воспроизведение с fade in."""
        if self._current_track:
            self._start_fade(True)
            self._player.play()
            self._is_playing = True
            self.stateChanged.emit(True)
            logger.debug("Playback started")

    def pause(self):
        """Поставить на паузу с fade out."""
        self._start_fade(False)
        self._is_playing = False
        self.stateChanged.emit(False)
        logger.debug("Playback paused")

    def stop(self):
        """Остановить воспроизведение."""
        self._player.stop()
        self._is_playing = False
        self.stateChanged.emit(False)
        logger.debug("Playback stopped")

    def seek(self, position: int):
        """Перемотка на указанную позицию."""
        self._player.setPosition(position)

    @property
    def volume(self) -> float:
        """Текущая громкость (0.0 - 1.0)."""
        return self._volume

    @volume.setter
    def volume(self, value: float):
        """Установка громкости с проверкой диапазона."""
        self._volume = max(0.0, min(1.0, value))
        self._audio_output.setVolume(self._volume)
        self.volumeChanged.emit(self._volume)

    def _start_fade(self, fade_in: bool):
        """Запуск fade эффекта."""
        self._fade_in = fade_in
        self._fade_steps = 10
        self._fade_timer.start()

    def _handle_fade(self):
        """Обработка fade эффекта."""
        if self._fade_in:
            self._volume = min(1.0, self._volume + 0.1)
        else:
            self._volume = max(0.0, self._volume - 0.1)
            
        self._audio_output.setVolume(self._volume)
        self._fade_steps -= 1
        
        if self._fade_steps <= 0:
            self._fade_timer.stop()
            if not self._fade_in:
                self._player.pause()

    def _handle_metadata(self):
        """Обработка метаданных трека."""
        metadata = {
            'title': self._player.metaData().stringValue(QMediaMetaData.Key.Title),
            'artist': self._player.metaData().stringValue(QMediaMetaData.Key.AlbumArtist),
            'album': self._player.metaData().stringValue(QMediaMetaData.Key.AlbumTitle),
            'duration': self._player.duration()
        }
        self._metadata = metadata
        self.metadataChanged.emit(metadata)

    def _handle_error(self, error):
        """Обработка ошибок воспроизведения."""
        error_msg = f"Playback error: {error}"
        self.errorOccurred.emit(error_msg)
        logger.error(error_msg)

    @property
    def is_playing(self) -> bool:
        """Текущее состояние воспроизведения."""
        return self._is_playing

    @property
    def current_track(self) -> Optional[Path]:
        """Текущий воспроизводимый трек."""
        return self._current_track

    @property
    def metadata(self) -> Dict:
        """Метаданные текущего трека."""
        return self._metadata.copy()