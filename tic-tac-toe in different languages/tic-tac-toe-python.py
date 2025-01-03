import sys
import pygame
import random

# Инициализация Pygame
pygame.init()

# Размеры окна Pygame
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-Нолики с ИИ")

# Цвета
WHITE = (30, 30, 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LINE_COLOR = (200, 200, 200)
X_COLOR = (255, 69, 0)  # Изменен цвет X на ярко-красный
O_COLOR = (0, 191, 255)  # Изменен цвет O на ярко-голубой

# Настройки игры
BOARD_SIZE = 3
CELL_SIZE = WIDTH // BOARD_SIZE
board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 'X'
difficulty = "easy"  # Сложность ИИ: "easy", "medium" или "hard"

# Шрифт для текста
FONT = pygame.font.Font(None, 100)
MENU_FONT = pygame.font.Font(None, 50)

# Функция для отрисовки доски
def draw_board():
    screen.fill(BLACK)
    for row in range(1, BOARD_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 2)
        pygame.draw.line(screen, LINE_COLOR, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), 2)

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 'X':
                text = FONT.render("X", True, X_COLOR)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))
            elif board[row][col] == 'O':
                text = FONT.render("O", True, O_COLOR)
                screen.blit(text, (col * CELL_SIZE + CELL_SIZE // 4, row * CELL_SIZE + CELL_SIZE // 4))

# Функция для проверки победы
def check_winner():
    # Проверка строк
    for row in range(BOARD_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            return board[row][0]

    # Проверка столбцов
    for col in range(BOARD_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]

    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]

    # Проверка на ничью
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                return None
    return 'Ничья'

# Функция для обработки хода
def make_move(x, y):
    global current_player
    row = y // CELL_SIZE
    col = x // CELL_SIZE

    if board[row][col] == '':
        board[row][col] = current_player
        current_player = 'O' if current_player == 'X' else 'X'

# Функция для хода ИИ (лёгкий)
def ai_move_easy():
    empty_cells = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if board[row][col] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'

# Функция для хода ИИ (средний)
def ai_move_medium():
    # Проверка на возможность победы ИИ
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                board[row][col] = 'O'
                if check_winner() == 'O':
                    return
                board[row][col] = ''

    # Проверка на возможность победы игрока и блокировка
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                board[row][col] = 'X'
                if check_winner() == 'X':
                    board[row][col] = 'O'
                    return
                board[row][col] = ''

    # Если нет угроз, делаем случайный ход
    ai_move_easy()

# Функция для хода ИИ (сложный)
def ai_move_hard():
    best_score = -float('inf')
    best_move = None

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ''

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        board[best_move[0]][best_move[1]] = 'O'

# Алгоритм минимакс
def minimax(board, depth, is_maximizing):
    winner = check_winner()
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif winner == 'Ничья':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

# Функция для отрисовки меню
def draw_menu():
    screen.fill(BLACK)
    text_easy = MENU_FONT.render("Лёгкий", True, LINE_COLOR)
    text_medium = MENU_FONT.render("Средний", True, LINE_COLOR)
    text_hard = MENU_FONT.render("Сложный", True, LINE_COLOR)

    # Кнопки для выбора сложности
    button_easy = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    button_medium = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    button_hard = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)

    pygame.draw.rect(screen, BLUE, button_easy)
    pygame.draw.rect(screen, BLUE, button_medium)
    pygame.draw.rect(screen, BLUE, button_hard)

    screen.blit(text_easy, (WIDTH // 2 - 70, HEIGHT // 2 - 90))
    screen.blit(text_medium, (WIDTH // 2 - 70, HEIGHT // 2 + 10))
    screen.blit(text_hard, (WIDTH // 2 - 70, HEIGHT // 2 + 110))

    pygame.display.flip()

    # Ожидание выбора сложности
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if button_easy.collidepoint(x, y):
                    return "easy"
                elif button_medium.collidepoint(x, y):
                    return "medium"
                elif button_hard.collidepoint(x, y):
                    return "hard"

# Основной игровой цикл Pygame
def game_loop():
    global current_player, difficulty
    running = True
    while running:
        draw_board()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X':
                x, y = event.pos
                make_move(x, y)

        if current_player == 'O':
            if difficulty == "easy":
                ai_move_easy()
            elif difficulty == "medium":
                ai_move_medium()
            elif difficulty == "hard":
                ai_move_hard()
            current_player = 'X'

        winner = check_winner()
        if winner:
            print(f"Игрок {winner} победил!" if winner != 'Ничья' else "Ничья!")
            running = False

    pygame.quit()

# Основная программа
if __name__ == "__main__":
    # Меню выбора сложности
    difficulty = draw_menu()

    # Запуск игры
    game_loop()
