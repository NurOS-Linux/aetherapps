import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox, QComboBox
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtCore import Qt, QRect, QTimer, QSize


class FourInARowGame:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # 0 - пусто, 1 - игрок, 2 - ИИ
        self.current_player = 1

    def drop_piece(self, col):
        """Помещает шарик в указанный столбец."""
        for row in reversed(range(self.rows)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                return row, col
        return None

    def check_winner(self):
        """Проверяет, есть ли победитель."""
        directions = [
            (1, 0),  # Горизонталь
            (0, 1),  # Вертикаль
            (1, 1),  # Диагональ вниз-вправо
            (1, -1)  # Диагональ вниз-влево
        ]
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] != 0:
                    for dr, dc in directions:
                        count = 1
                        for i in range(1, 4):
                            r, c = row + dr * i, col + dc * i
                            if 0 <= r < self.rows and 0 <= c < self.cols and self.board[r][c] == self.board[row][col]:
                                count += 1
                            else:
                                break
                        if count >= 4:
                            return self.board[row][col]
        return 0

    def reset(self):
        """Сбрасывает игру."""
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_player = 1

    def ai_move(self, difficulty):
        """ИИ делает ход в зависимости от уровня сложности."""
        if difficulty == "Легкий":
            return self.ai_random()
        elif difficulty == "Средний":
            return self.ai_medium()
        elif difficulty == "Высокий":
            return self.ai_hard()
        elif difficulty == "Хардкор":
            return self.ai_minimax()
        return None

    def ai_random(self):
        """ИИ делает случайный ход."""
        available_columns = [col for col in range(self.cols) if self.board[0][col] == 0]
        if available_columns:
            return random.choice(available_columns)
        return None

    def ai_medium(self):
        """ИИ пытается выиграть или блокировать игрока."""
        # Проверка, может ли ИИ выиграть
        for col in range(self.cols):
            if self.board[0][col] == 0:
                row, _ = self.drop_piece(col)
                if self.check_winner() == 2:
                    self.board[row][col] = 0  # Отменяем ход
                    return col
                self.board[row][col] = 0  # Отменяем ход

        # Проверка, может ли игрок выиграть следующим ходом
        for col in range(self.cols):
            if self.board[0][col] == 0:
                row, _ = self.drop_piece(col)
                if self.check_winner() == 1:
                    self.board[row][col] = 0  # Отменяем ход
                    return col
                self.board[row][col] = 0  # Отменяем ход

        # Случайный ход, если нет выигрышных или блокирующих ходов
        return self.ai_random()

    def ai_hard(self):
        """ИИ использует более сложную логику."""
        # Попытка выиграть или блокировать игрока
        move = self.ai_medium()
        if move is not None:
            return move

        # Предпочтение центральных столбцов
        center_columns = [3, 2, 4, 1, 5, 0, 6]
        for col in center_columns:
            if self.board[0][col] == 0:
                return col
        return None

    def ai_minimax(self, depth=4, alpha=-float('inf'), beta=float('inf'), maximizing_player=True):
        """ИИ использует алгоритм минимакс с альфа-бета отсечением."""
        if depth == 0 or self.check_winner() != 0:
            return self.evaluate_board()

        available_columns = [col for col in range(self.cols) if self.board[0][col] == 0]
        if maximizing_player:
            max_eval = -float('inf')
            best_col = random.choice(available_columns)
            for col in available_columns:
                row, _ = self.drop_piece(col)
                eval = self.ai_minimax(depth - 1, alpha, beta, False)
                self.board[row][col] = 0  # Отменяем ход
                if eval > max_eval:
                    max_eval = eval
                    best_col = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_col
        else:
            min_eval = float('inf')
            for col in available_columns:
                row, _ = self.drop_piece(col)
                eval = self.ai_minimax(depth - 1, alpha, beta, True)
                self.board[row][col] = 0  # Отменяем ход
                if eval < min_eval:
                    min_eval = eval
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self):
        """Оценка состояния доски для минимакс."""
        if self.check_winner() == 2:
            return 100
        elif self.check_winner() == 1:
            return -100
        return 0


class GameBoard(QWidget):
    def __init__(self, game, on_click):
        super().__init__()
        self.game = game
        self.on_click = on_click
        self.cell_size = 100  # Начальный размер ячейки
        self.setMinimumSize(700, 600)  # Минимальный размер окна

    def resizeEvent(self, event):
        """Обрабатывает изменение размера окна."""
        super().resizeEvent(event)
        self.cell_size = min(self.width() // self.game.cols, self.height() // self.game.rows)
        self.update()

    def paintEvent(self, event):
        """Отрисовка игрового поля."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Отрисовка сетки
        for row in range(self.game.rows):
            for col in range(self.game.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                rect = QRect(x, y, self.cell_size, self.cell_size)
                painter.setPen(Qt.GlobalColor.blue)
                painter.setBrush(QBrush(QColor(30, 30, 30)))  # Черный фон
                painter.drawRect(rect)

                # Отрисовка шариков
                if self.game.board[row][col] == 1:
                    painter.setBrush(QBrush(QColor(255, 0, 0)))  # Красный шарик (игрок)
                elif self.game.board[row][col] == 2:
                    painter.setBrush(QBrush(QColor(255, 255, 0)))  # Желтый шарик (ИИ)
                else:
                    continue
                painter.drawEllipse(x + 10, y + 10, self.cell_size - 20, self.cell_size - 20)

    def mousePressEvent(self, event):
        """Обрабатывает клик мыши."""
        if event.button() == Qt.MouseButton.LeftButton:
            col = int(event.position().x() // self.cell_size)  # Преобразуем в целое число
            if 0 <= col < self.game.cols:
                self.on_click(col)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Четыре шарика в линию (ИИ)")
        self.setGeometry(100, 100, 700, 600)

        # Инициализация игры
        self.game = FourInARowGame()
        self.difficulty = "Легкий"  # Уровень сложности по умолчанию

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем вертикальный layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Добавляем выбор уровня сложности
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Легкий", "Средний", "Высокий", "Хардкор"])
        self.difficulty_combo.currentTextChanged.connect(self.set_difficulty)
        layout.addWidget(self.difficulty_combo)

        # Добавляем заголовок
        self.status_label = QLabel("Ход игрока 1")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Добавляем кнопку сброса
        reset_button = QPushButton("Сбросить игру")
        reset_button.clicked.connect(self.reset_game)
        layout.addWidget(reset_button)

        # Добавляем игровое поле
        self.game_board = GameBoard(self.game, self.on_column_click)
        layout.addWidget(self.game_board)

        # Таймер для хода ИИ
        self.ai_timer = QTimer()
        self.ai_timer.timeout.connect(self.ai_turn)

    def set_difficulty(self, difficulty):
        """Устанавливает уровень сложности."""
        self.difficulty = difficulty

    def on_column_click(self, col):
        """Обрабатывает клик по столбцу."""
        if self.game.current_player == 1:  # Ход игрока
            if self.game.drop_piece(col) is not None:
                winner = self.game.check_winner()
                if winner:
                    self.show_winner_message(winner)
                else:
                    self.game.current_player = 2  # Переход хода к ИИ
                    self.status_label.setText("Ход ИИ")
                    self.game_board.update()
                    self.ai_timer.start(1000)  # Запуск таймера для хода ИИ

    def ai_turn(self):
        """Ход ИИ."""
        self.ai_timer.stop()  # Останавливаем таймер
        col = self.game.ai_move(self.difficulty)  # ИИ делает ход
        if col is not None:
            if self.game.drop_piece(col) is not None:
                winner = self.game.check_winner()
                if winner:
                    self.show_winner_message(winner)
                else:
                    self.game.current_player = 1  # Переход хода к игроку
                    self.status_label.setText("Ход игрока 1")
                    self.game_board.update()

    def show_winner_message(self, winner):
        """Показывает сообщение о победе."""
        msg = QMessageBox()
        msg.setWindowTitle("Победа!")
        msg.setText(f"Победил {'игрок' if winner == 1 else 'ИИ'}!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
        self.reset_game()

    def reset_game(self):
        """Сбрасывает игру."""
        self.game.reset()
        self.status_label.setText("Ход игрока 1")
        self.game_board.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
