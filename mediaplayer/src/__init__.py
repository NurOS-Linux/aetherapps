"""
NurOS Media Player
~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Media Player Package

Created: 2024-12-22 09:52:48 UTC
Author: AnmiTaliDev
License: GPL 3
"""

import logging
from pathlib import Path
from datetime import datetime
from PyQt6.QtCore import QSettings

# Информация о приложении
APP_NAME = "NurOS Media Player"
VERSION = "1.0.0"
AUTHOR = "AnmiTaliDev"
CREATED = datetime(2024, 12, 22, 9, 52, 48)

# Настройка путей
CONFIG_DIR = Path.home() / ".config" / "nuros-mediaplayer"
CACHE_DIR = Path.home() / ".cache" / "nuros-mediaplayer"
LOG_DIR = Path.home() / ".local" / "share" / "nuros-mediaplayer" / "logs"

# Создаем необходимые директории
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# DeltaDesign Concept Night тема
class DeltaNightTheme:
    """Цветовая схема DeltaDesign Concept Night"""
    
    # Основные цвета
    PRIMARY_DARK = "#121212"
    SECONDARY_DARK = "#1E1E1E"
    NIGHT_BLUE = "#2D5B9E"
    NIGHT_PURPLE = "#6B4BA3"
    NIGHT_TEAL = "#1C746C"
    
    # Поверхности
    SURFACE_LIGHT = "#3A3A3A"
    SURFACE_MID = "#2C2C2C"
    SURFACE_DARK = "#1A1A1A"
    
    # Текст
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B3B3B3"
    
    # UI элементы
    BORDER_RADIUS = 14
    PADDING = 5
    
    @classmethod
    def get_theme_dict(cls):
        """Получить словарь с цветами темы"""
        return {
            'primary_dark': cls.PRIMARY_DARK,
            'secondary_dark': cls.SECONDARY_DARK,
            'night_blue': cls.NIGHT_BLUE,
            'night_purple': cls.NIGHT_PURPLE,
            'night_teal': cls.NIGHT_TEAL,
            'surface_light': cls.SURFACE_LIGHT,
            'surface_mid': cls.SURFACE_MID,
            'surface_dark': cls.SURFACE_DARK,
            'text_primary': cls.TEXT_PRIMARY,
            'text_secondary': cls.TEXT_SECONDARY
        }

# Настройки плеера
class PlayerSettings:
    """Настройки медиаплеера по умолчанию"""
    
    # Аудио настройки
    AUDIO = {
        'volume': 0.7,
        'fade_duration': 0.5,
        'buffer_size': 4096,
    }
    
    # Поддерживаемые форматы
    FORMATS = [
        '.mp3',
        '.wav',
        '.ogg',
        '.flac'
    ]
    
    # Настройки окна
    WINDOW = {
        'min_width': 800,
        'min_height': 600,
        'default_width': 1024,
        'default_height': 768
    }
    
    # Плейлист
    PLAYLIST = {
        'auto_play': True,
        'remember_position': True,
        'shuffle_on_load': False
    }

# Настройка логирования
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)

# Файловый обработчик
file_handler = logging.FileHandler(
    LOG_DIR / "mediaplayer.log",
    encoding='utf-8'
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(levelname)s: %(message)s')
)
logger.addHandler(console_handler)

# Глобальные настройки приложения
settings = QSettings("NurOS", APP_NAME)

def get_app_info():
    """Получить информацию о приложении"""
    return {
        'name': APP_NAME,
        'version': VERSION,
        'author': AUTHOR,
        'created': CREATED.isoformat(),
        'theme': DeltaNightTheme.get_theme_dict(),
        'settings': PlayerSettings.AUDIO | PlayerSettings.WINDOW
    }

# Экспортируем публичные компоненты
__all__ = [
    'APP_NAME',
    'VERSION',
    'AUTHOR',
    'DeltaNightTheme',
    'PlayerSettings',
    'logger',
    'settings',
    'get_app_info'
]

# Логируем инициализацию пакета
logger.info(f"Initializing {APP_NAME} v{VERSION}")
logger.info(f"Created by: {AUTHOR}")
logger.info(f"Creation date: {CREATED}")