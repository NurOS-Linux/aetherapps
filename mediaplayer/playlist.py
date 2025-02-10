from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QListWidget, QPushButton, QFileDialog)
from PyQt6.QtCore import pyqtSignal
import os

class PlaylistWidget(QWidget):
    # Сигналы для взаимодействия с главным окном
    track_selected = pyqtSignal(str, int)  # путь к файлу, индекс
    playlist_updated = pyqtSignal(list)    # список путей к файлам
    
    def __init__(self):
        super().__init__()
        self.tracks = []  # список путей к файлам
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Список треков
        self.list_widget = QListWidget()
        self.list_widget.setMinimumWidth(300)
        layout.addWidget(self.list_widget)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить")
        self.remove_btn = QPushButton("Удалить")
        self.clear_btn = QPushButton("Очистить")
        
        for btn in [self.add_btn, self.remove_btn, self.clear_btn]:
            btn_layout.addWidget(btn)
            
        layout.addLayout(btn_layout)

    def connect_signals(self):
        self.add_btn.clicked.connect(self.add_files)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.clear_btn.clicked.connect(self.clear_playlist)
        self.list_widget.itemDoubleClicked.connect(self.on_track_selected)

    def add_files(self):
        """Добавление файлов в плейлист"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите аудиофайлы",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.m4a *.flac)"
        )
        
        if files:
            for file_path in files:
                self.tracks.append(file_path)
                self.list_widget.addItem(os.path.basename(file_path))
            
            self.playlist_updated.emit(self.tracks)

    def remove_selected(self):
        """Удаление выбранного трека"""
        current = self.list_widget.currentRow()
        if current >= 0:
            self.list_widget.takeItem(current)
            self.tracks.pop(current)
            self.playlist_updated.emit(self.tracks)

    def clear_playlist(self):
        """Очистка плейлиста"""
        self.list_widget.clear()
        self.tracks.clear()
        self.playlist_updated.emit(self.tracks)

    def on_track_selected(self, item):
        """Обработка выбора трека"""
        current = self.list_widget.row(item)
        if current >= 0:
            self.track_selected.emit(self.tracks[current], current)

    def get_next_track(self, current_index):
        """Получить следующий трек"""
        if self.tracks:
            next_index = (current_index + 1) % len(self.tracks)
            return self.tracks[next_index], next_index
        return None, -1

    def get_previous_track(self, current_index):
        """Получить предыдущий трек"""
        if self.tracks:
            prev_index = (current_index - 1) % len(self.tracks)
            return self.tracks[prev_index], prev_index
        return None, -1

    def highlight_playing(self, index):
        """Подсветка играющего трека"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if i == index:
                item.setText("▶ " + os.path.basename(self.tracks[i]))
            else:
                item.setText(os.path.basename(self.tracks[i]))

    def get_track_count(self):
        """Получить количество треков"""
        return len(self.tracks)

    def get_all_tracks(self):
        """Получить все треки"""
        return self.tracks.copy()

    def load_playlist(self, file_paths):
        """Загрузка плейлиста из списка путей"""
        self.clear_playlist()
        for path in file_paths:
            if os.path.exists(path):
                self.tracks.append(path)
                self.list_widget.addItem(os.path.basename(path))
        self.playlist_updated.emit(self.tracks)

    def save_playlist(self, file_path):
        """Сохранение плейлиста в файл"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for track in self.tracks:
                    f.write(f"{track}\n")
            return True
        except Exception as e:
            print(f"Ошибка при сохранении плейлиста: {e}")
            return False

    def get_current_track(self):
        """Получить текущий выбранный трек"""
        current = self.list_widget.currentRow()
        if current >= 0:
            return self.tracks[current], current
        return None, -1

    def set_current_index(self, index):
        """Установить текущий индекс"""
        if 0 <= index < self.list_widget.count():
            self.list_widget.setCurrentRow(index)

    def update_track_info(self, index, info):
        """Обновить информацию о треке"""
        if 0 <= index < self.list_widget.count():
            item = self.list_widget.item(index)
            item.setToolTip(
                f"Название: {info.get('title', 'Неизвестно')}\n"
                f"Исполнитель: {info.get('artist', 'Неизвестно')}\n"
                f"Альбом: {info.get('album', 'Неизвестно')}\n"
                f"Длительность: {info.get('duration', '00:00')}"
            )