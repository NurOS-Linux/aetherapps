"""
NurOS Media Player - Utilities Package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Core utilities and helpers for DeltaDesign Concept Night.

Created: 2024-12-22 11:01:06 UTC
Author: AnmiTaliDev
License: GPL 3
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime

from .. import logger

class FileUtils:
    """Утилиты для работы с файлами."""
    
    SUPPORTED_FORMATS = {
        '.mp3': 'MPEG Audio Layer III',
        '.wav': 'Waveform Audio',
        '.ogg': 'Ogg Vorbis Audio',
        '.flac': 'Free Lossless Audio Codec'
    }
    
    @staticmethod
    def is_audio_file(path: Path) -> bool:
        """Проверка является ли файл аудио."""
        return path.suffix.lower() in FileUtils.SUPPORTED_FORMATS
    
    @staticmethod
    def get_file_info(path: Path) -> Dict[str, Any]:
        """Получение информации о файле."""
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
            
        return {
            'name': path.name,
            'size': path.stat().st_size,
            'modified': datetime.fromtimestamp(path.stat().st_mtime),
            'format': FileUtils.SUPPORTED_FORMATS.get(
                path.suffix.lower(), 'Unknown Format'
            )
        }
    
    @staticmethod
    def format_size(size: int) -> str:
        """Форматирование размера файла."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

class ConfigManager:
    """Менеджер конфигурации приложения."""
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config: Dict[str, Any] = {}
        self.load_config()
        
    def load_config(self):
        """Загрузка конфигурации."""
        config_file = self.config_dir / "config.json"
        try:
            if config_file.exists():
                import json
                with config_file.open('r', encoding='utf-8') as f:
                    self._config = json.load(f)
                logger.info("Configuration loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self._config = {}
    
    def save_config(self):
        """Сохранение конфигурации."""
        config_file = self.config_dir / "config.json"
        try:
            import json
            with config_file.open('w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=4)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получение значения конфигурации."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Установка значения конфигурации."""
        self._config[key] = value
        self.save_config()

class TimeUtils:
    """Утилиты для работы со временем."""
    
    @staticmethod
    def format_duration(ms: int) -> str:
        """Форматирование длительности из миллисекунд."""
        seconds = ms // 1000
        minutes = seconds // 60
        hours = minutes // 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes%60:02d}:{seconds%60:02d}"
        return f"{minutes:02d}:{seconds%60:02d}"
    
    @staticmethod
    def parse_duration(time_str: str) -> Optional[int]:
        """Парсинг строки времени в миллисекунды."""
        try:
            parts = time_str.split(':')
            if len(parts) == 2:
                minutes, seconds = map(int, parts)
                return (minutes * 60 + seconds) * 1000
            elif len(parts) == 3:
                hours, minutes, seconds = map(int, parts)
                return (hours * 3600 + minutes * 60 + seconds) * 1000
        except ValueError:
            return None
        return None

# Экспорт публичных компонентов
__all__ = ['FileUtils', 'ConfigManager', 'TimeUtils']

# Создаем глобальный конфиг
config = ConfigManager(Path.home() / '.config' / 'nuros-mediaplayer')
logger.info("Utils package initialized")