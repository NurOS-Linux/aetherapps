"""
NurOS Media Player - UI Package
~~~~~~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night UI components initialization.

Created: 2024-12-22 09:59:36 UTC
Author: AnmiTaliDev
License: GPL 3
"""

from pathlib import Path
from typing import Dict, Any
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette, QLinearGradient, QGradient
from .. import DeltaNightTheme, logger

class UiConstants:
    """Константы интерфейса в стиле DeltaDesign Concept Night."""
    
    # Размеры окна
    WINDOW_MIN_SIZE = QSize(800, 600)
    WINDOW_DEFAULT_SIZE = QSize(1024, 768)
    
    # Размеры компонентов
    BUTTON_SIZE = QSize(40, 40)
    ICON_SIZE = QSize(24, 24)
    SLIDER_HEIGHT = 4
    SLIDER_HANDLE_SIZE = 16
    VOLUME_SLIDER_WIDTH = 100
    
    # Отступы и скругления
    BORDER_RADIUS = 14
    PADDING = {
        'small': 5,
        'medium': 10,
        'large': 20
    }
    
    # Анимации
    ANIMATION = {
        'fade': 200,
        'hover': 150,
        'press': 100
    }
    
    # Шрифты
    FONT = {
        'family': 'Segoe UI',
        'size': {
            'small': 10,
            'normal': 12,
            'large': 14,
            'title': 16
        }
    }

class UiStylesheet:
    """Генератор стилей в стиле DeltaDesign Concept Night."""
    
    def __init__(self):
        self.theme = DeltaNightTheme()
        self.constants = UiConstants()
        logger.info("UI stylesheet generator initialized")

    def get_main_style(self) -> str:
        """Основной стиль приложения."""
        return f"""
            QMainWindow {{
                background-color: {self.theme.PRIMARY_DARK};
            }}
            QWidget {{
                color: {self.theme.TEXT_PRIMARY};
                font-family: {self.constants.FONT['family']};
                font-size: {self.constants.FONT['size']['normal']}px;
            }}
        """

    def get_button_style(self) -> str:
        """Стиль для кнопок."""
        return f"""
            QPushButton {{
                background-color: {self.theme.SECONDARY_DARK};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                border-radius: {self.constants.BORDER_RADIUS}px;
                padding: {self.constants.PADDING['medium']}px;
            }}
            QPushButton:hover {{
                background-color: {self.theme.SURFACE_MID};
            }}
            QPushButton:pressed {{
                background-color: {self.theme.SURFACE_DARK};
            }}
        """

    def get_slider_style(self) -> str:
        """Стиль для слайдеров."""
        return f"""
            QSlider::groove:horizontal {{
                border: none;
                height: {self.constants.SLIDER_HEIGHT}px;
                background: {self.theme.SURFACE_DARK};
                border-radius: {self.constants.SLIDER_HEIGHT // 2}px;
            }}
            QSlider::handle:horizontal {{
                background: {self.theme.NIGHT_TEAL};
                width: {self.constants.SLIDER_HANDLE_SIZE}px;
                height: {self.constants.SLIDER_HANDLE_SIZE}px;
                margin: -{(self.constants.SLIDER_HANDLE_SIZE - self.constants.SLIDER_HEIGHT) // 2}px 0;
                border-radius: {self.constants.SLIDER_HANDLE_SIZE // 2}px;
            }}
        """

    def get_list_style(self) -> str:
        """Стиль для списков."""
        return f"""
            QListWidget {{
                background-color: {self.theme.SECONDARY_DARK};
                border: none;
                border-radius: {self.constants.BORDER_RADIUS}px;
                padding: {self.constants.PADDING['small']}px;
            }}
            QListWidget::item {{
                color: {self.theme.TEXT_PRIMARY};
                padding: {self.constants.PADDING['small']}px;
            }}
            QListWidget::item:selected {{
                background-color: {self.theme.NIGHT_BLUE};
            }}
            QListWidget::item:hover {{
                background-color: {self.theme.SURFACE_MID};
            }}
        """

    def get_label_style(self) -> str:
        """Стиль для текстовых меток."""
        return f"""
            QLabel {{
                color: {self.theme.TEXT_PRIMARY};
                padding: {self.constants.PADDING['small']}px;
            }}
        """

    def get_complete_style(self) -> str:
        """Полный набор стилей."""
        return "\n".join([
            self.get_main_style(),
            self.get_button_style(),
            self.get_slider_style(),
            self.get_list_style(),
            self.get_label_style()
        ])

# Экспорт публичных компонентов
__all__ = ['UiConstants', 'UiStylesheet']

# Создаем глобальный экземпляр стилей
ui_style = UiStylesheet()
logger.info("UI styles initialized")