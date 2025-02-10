def get_spotify_style():
    return """
        /* Основные стили окна и виджетов */
        QMainWindow, QWidget {
            background-color: #121212;
            color: white;
            font-family: 'Segoe UI', Arial, sans-serif;
        }

        /* Кнопки */
        QPushButton {
            background-color: #1db954;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
            min-width: 100px;
        }

        QPushButton:hover {
            background-color: #1ed760;
        }

        QPushButton:pressed {
            background-color: #179443;
        }

        /* Круглые кнопки плеера */
        QPushButton#player-control {
            border-radius: 25px;
            min-width: 50px;
            max-width: 50px;
            min-height: 50px;
            max-height: 50px;
            font-size: 20px;
            padding: 0px;
        }

        /* Плейлист */
        QListWidget {
            background-color: #282828;
            border: none;
            border-radius: 10px;
            padding: 10px;
            outline: none;
        }

        QListWidget::item {
            color: #b3b3b3;
            padding: 8px 10px;
            border-radius: 4px;
            margin: 2px 0px;
        }

        QListWidget::item:selected {
            background-color: #1db954;
            color: white;
        }

        QListWidget::item:hover {
            background-color: #404040;
            color: white;
        }

        /* Слайдеры */
        QSlider {
            height: 20px;
        }

        QSlider::groove:horizontal {
            border: none;
            height: 4px;
            background: #404040;
            border-radius: 2px;
            margin: 0px;
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
            transform: scale(1.1);
        }

        QSlider::sub-page:horizontal {
            background: #1db954;
            border-radius: 2px;
        }

        /* Метки */
        QLabel {
            color: white;
        }

        QLabel#track-title {
            font-size: 24px;
            font-weight: bold;
        }

        QLabel#track-artist {
            font-size: 16px;
            color: #b3b3b3;
        }

        QLabel#time-label {
            color: #b3b3b3;
            font-size: 12px;
        }

        /* Полоса прокрутки */
        QScrollBar:vertical {
            border: none;
            background: #121212;
            width: 10px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #404040;
            border-radius: 5px;
            min-height: 20px;
        }

        QScrollBar::handle:vertical:hover {
            background: #535353;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
            border: none;
        }

        /* Выпадающие списки */
        QComboBox {
            background-color: #282828;
            border: none;
            border-radius: 4px;
            padding: 5px 10px;
            color: white;
            min-width: 100px;
        }

        QComboBox:hover {
            background-color: #404040;
        }

        QComboBox::drop-down {
            border: none;
        }

        QComboBox::down-arrow {
            image: none;
        }

        /* Всплывающие подсказки */
        QToolTip {
            background-color: #282828;
            color: white;
            border: none;
            padding: 5px;
            border-radius: 4px;
        }
    """

# Цветовые константы
COLORS = {
    'background': '#121212',
    'surface': '#282828',
    'primary': '#1db954',
    'primary_hover': '#1ed760',
    'primary_pressed': '#179443',
    'text_primary': '#ffffff',
    'text_secondary': '#b3b3b3',
    'divider': '#404040',
}

# Размеры
SIZES = {
    'border_radius_small': '4px',
    'border_radius_medium': '8px',
    'border_radius_large': '12px',
    'padding_small': '5px',
    'padding_medium': '10px',
    'padding_large': '20px',
}