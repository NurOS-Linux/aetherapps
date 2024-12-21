import sys
import os
import pygame
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPalette, QColor


class MediaPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Медиаплеер")
        self.setGeometry(100, 100, 600, 300)

        # Инициализация Pygame и звукового модуля
        pygame.init()
        pygame.mixer.init()
        self.current_track = None
        self.is_playing = False
        self.volume = 0.5  # Начальная громкость (от 0.0 до 1.0)
        self.duration = 0  # Длительность трека
        self.position = 0  # Текущая позиция трека

        # Таймер для обновления позиции трека
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)

        # Создание интерфейса
        self.create_ui()

    def create_ui(self):
        """Создает графический интерфейс."""
        # Основной виджет
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Вертикальный layout
        layout = QVBoxLayout()

        # Метка для отображения текущего трека
        self.track_label = QLabel("Нет загруженного трека", self)
        self.track_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.track_label)

        # Слайдер для перемотки трека
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(1000)  # Максимальное значение для слайдера
        self.position_slider.sliderMoved.connect(self.set_position)
        layout.addWidget(self.position_slider)

        # Кнопки управления
        control_layout = QHBoxLayout()

        self.play_button = QPushButton("▶ Воспроизвести", self)
        self.play_button.clicked.connect(self.play)
        control_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("⏸ Пауза", self)
        self.pause_button.clicked.connect(self.pause)
        control_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("⏹ Стоп", self)
        self.stop_button.clicked.connect(self.stop)
        control_layout.addWidget(self.stop_button)

        layout.addLayout(control_layout)

        # Кнопка загрузки трека
        self.load_button = QPushButton("Загрузить трек", self)
        self.load_button.clicked.connect(self.load_track)
        layout.addWidget(self.load_button)

        # Слайдер для управления громкостью
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(int(self.volume * 100))  # Устанавливаем начальную громкость
        self.volume_slider.valueChanged.connect(self.set_volume)
        layout.addWidget(self.volume_slider)

        # Чекбокс для переключения темы
        self.theme_checkbox = QCheckBox("Черная тема", self)
        self.theme_checkbox.stateChanged.connect(self.toggle_theme)
        layout.addWidget(self.theme_checkbox)

        # Установка layout
        main_widget.setLayout(layout)

    def load_track(self):
        """Загружает аудиофайл для воспроизведения."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите аудиофайл", "", "MP3 files (*.mp3);;WAV files (*.wav);;All files (*.*)"
        )
        if file_path:
            self.current_track = file_path
            self.track_label.setText(f"Текущий трек: {os.path.basename(file_path)}")
            pygame.mixer.music.load(file_path)
            self.duration = pygame.mixer.Sound(file_path).get_length()  # Получаем длительность трека
            self.position_slider.setMaximum(int(self.duration * 1000))  # Устанавливаем максимальное значение слайдера
            QMessageBox.information(self, "Успешно", f"Файл {os.path.basename(file_path)} загружен.")

    def play(self):
        """Воспроизводит текущий аудиофайл."""
        if self.current_track:
            pygame.mixer.music.play(start=self.position / 1000)  # Воспроизведение с текущей позиции
            self.is_playing = True
            self.play_button.setText("⏸ Пауза")
            self.timer.start(100)  # Запускаем таймер для обновления позиции
        else:
            QMessageBox.warning(self, "Ошибка", "Нет загруженного файла для воспроизведения.")

    def pause(self):
        """Ставит воспроизведение на паузу."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_button.setText("▶ Воспроизвести")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_button.setText("⏸ Пауза")

    def stop(self):
        """Останавливает воспроизведение."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_button.setText("▶ Воспроизвести")
            self.position = 0
            self.position_slider.setValue(0)
            self.timer.stop()

    def set_volume(self, value):
        """Устанавливает громкость воспроизведения."""
        volume = value / 100
        pygame.mixer.music.set_volume(volume)
        self.volume = volume

    def set_position(self, value):
        """Устанавливает текущую позицию трека."""
        self.position = value
        if self.is_playing:
            pygame.mixer.music.play(start=self.position / 1000)

    def update_position(self):
        """Обновляет текущую позицию трека."""
        if self.is_playing:
            self.position = pygame.mixer.music.get_pos() / 1000  # Получаем текущую позицию в секундах
            self.position_slider.setValue(int(self.position * 1000))

    def toggle_theme(self, state):
        """Переключает тему (белая/черная)."""
        if state == Qt.CheckState.Checked.value:
            self.set_dark_theme()
        else:
            self.set_light_theme()

    def set_dark_theme(self):
        """Устанавливает темную тему."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.setPalette(palette)

    def set_light_theme(self):
        """Устанавливает светлую тему."""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Base, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.AlternateBase, Qt.GlobalColor.lightGray)
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.Button, Qt.GlobalColor.lightGray)
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        self.setPalette(palette)

    def closeEvent(self, event):
        """Обработка закрытия окна."""
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        event.accept()


# Основная программа
if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = MediaPlayer()
    player.show()
    sys.exit(app.exec())
