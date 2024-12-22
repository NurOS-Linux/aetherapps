"""
NurOS Media Player - Style Module
~~~~~~~~~~~~~~~~~~~~~~~~~~~
DeltaDesign Concept Night Style Definitions

Created: 2024-12-22 10:57:24 UTC
Author: AnmiTaliDev
License: GPL 3
"""

from typing import Dict, Any
from PyQt6.QtGui import QColor, QLinearGradient, QGradient, QPalette
from PyQt6.QtCore import Qt

from .. import DeltaNightTheme, logger

class DeltaNightStyle:
    """
    Стилевой провайдер DeltaDesign Concept Night.
    Определяет цвета, градиенты и стили для UI компонентов.
    """

    def __init__(self):
        self.theme = DeltaNightTheme()
        self.init_gradients()
        logger.info("DeltaNight style provider initialized")

    def init_gradients(self):
        """Инициализация градиентов."""
        # Фоновый градиент
        self.background_gradient = QLinearGradient(0, 0, 0, 1)
        self.background_gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self.background_gradient.setStops([
            (0.0, QColor(self.theme.PRIMARY_DARK)),
            (1.0, QColor(self.theme.SECONDARY_DARK))
        ])

        # Градиент для кнопок
        self.button_gradient = QLinearGradient(0, 0, 0, 1)
        self.button_gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self.button_gradient.setStops([
            (0.0, QColor(self.theme.SURFACE_LIGHT)),
            (1.0, QColor(self.theme.SURFACE_MID))
        ])

        # Акцентный градиент
        self.accent_gradient = QLinearGradient(0, 0, 0, 1)
        self.accent_gradient.setCoordinateMode(QGradient.CoordinateMode.ObjectBoundingMode)
        self.accent_gradient.setStops([
            (0.0, QColor(self.theme.NIGHT_BLUE)),
            (1.0, QColor(self.theme.NIGHT_PURPLE))
        ])

    def get_stylesheet(self) -> str:
        """Получение полного набора стилей."""
        return f"""
            /* Главное окно */
            QMainWindow {{
                background: {self.theme.PRIMARY_DARK};
            }}

            /* Базовые виджеты */
            QWidget {{
                background-color: transparent;
                color: {self.theme.TEXT_PRIMARY};
            }}

            /* Фреймы */
            QFrame {{
                background-color: {self.theme.SECONDARY_DARK};
                border-radius: 14px;
                padding: 10px;
            }}

            /* Кнопки */
            QPushButton {{
                background-color: {self.theme.SURFACE_MID};
                color: {self.theme.TEXT_PRIMARY};
                border: none;
                border-radius: 14px;
                padding: 8px 16px;
                min-width: 80px;
            }}

            QPushButton:hover {{
                background-color: {self.theme.SURFACE_LIGHT};
            }}

            QPushButton:pressed {{
                background-color: {self.theme.SURFACE_DARK};
            }}

            /* Слайдеры */
            QSlider::groove:horizontal {{
                border: none;
                height: 4px;
                background: {self.theme.SURFACE_DARK};
                border-radius: 2px;
            }}

            QSlider::handle:horizontal {{
                background: {self.theme.NIGHT_TEAL};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}

            QSlider::sub-page:horizontal {{
                background: {self.theme.NIGHT_TEAL};
                border-radius: 2px;
            }}

            /* Списки */
            QListWidget {{
                background-color: {self.theme.SECONDARY_DARK};
                border: none;
                border-radius: 14px;
                padding: 5px;
            }}

            QListWidget::item {{
                color: {self.theme.TEXT_PRIMARY};
                padding: 5px;
                border-radius: 7px;
            }}

            QListWidget::item:selected {{
                background-color: {self.theme.NIGHT_BLUE};
            }}

            QListWidget::item:hover {{
                background-color: {self.theme.SURFACE_MID};
            }}

            /* Метки */
            QLabel {{
                color: {self.theme.TEXT_PRIMARY};
            }}

            QLabel#trackInfo {{
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }}

            /* Полосы прокрутки */
            QScrollBar:vertical {{
                border: none;
                background: {self.theme.SURFACE_DARK};
                width: 8px;
                border-radius: 4px;
            }}

            QScrollBar::handle:vertical {{
                background: {self.theme.SURFACE_LIGHT};
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
            }}

            /* Специальные элементы управления */
            #playerControls {{
                background-color: {self.theme.SECONDARY_DARK};
                border-radius: 14px;
                padding: 15px;
            }}

            #volumeSlider {{
                max-width: 100px;
            }}

            #progressSlider {{
                height: 20px;
            }}
        """

    def get_palette(self) -> QPalette:
        """Получение цветовой палитры."""
        palette = QPalette()
        
        # Основные цвета
        palette.setColor(QPalette.ColorRole.Window, QColor(self.theme.PRIMARY_DARK))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(self.theme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Base, QColor(self.theme.SECONDARY_DARK))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self.theme.SURFACE_MID))
        palette.setColor(QPalette.ColorRole.Text, QColor(self.theme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Button, QColor(self.theme.SURFACE_MID))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(self.theme.TEXT_PRIMARY))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(self.theme.NIGHT_BLUE))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(self.theme.TEXT_PRIMARY))

        return palette

# Создаем глобальный экземпляр стиля
style_provider = DeltaNightStyle()
logger.info("DeltaNight style initialized")