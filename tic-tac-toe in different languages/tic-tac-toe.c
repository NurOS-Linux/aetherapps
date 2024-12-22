#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <time.h>

// Размер игрового поля
#define SIZE 3

// Функция для отображения игрового поля
void display_board(char board[SIZE][SIZE]) {
    printf("\n");
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            printf(" %c ", board[i][j]);
            if (j < SIZE - 1) {
                printf("|");
            }
        }
        printf("\n");
        if (i < SIZE - 1) {
            printf("---+---+---\n");
        }
    }
    printf("\n");
}

// Функция для проверки победы
bool check_winner(char board[SIZE][SIZE], char player) {
    // Проверка строк
    for (int i = 0; i < SIZE; i++) {
        if (board[i][0] == player && board[i][1] == player && board[i][2] == player) {
            return true;
        }
    }

    // Проверка столбцов
    for (int j = 0; j < SIZE; j++) {
        if (board[0][j] == player && board[1][j] == player && board[2][j] == player) {
            return true;
        }
    }

    // Проверка диагоналей
    if (board[0][0] == player && board[1][1] == player && board[2][2] == player) {
        return true;
    }
    if (board[0][2] == player && board[1][1] == player && board[2][0] == player) {
        return true;
    }

    return false;
}

// Функция для проверки ничьей
bool check_draw(char board[SIZE][SIZE]) {
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            if (board[i][j] == ' ') {
                return false;
            }
        }
    }
    return true;
}

// Функция для хода ИИ
void ai_move(char board[SIZE][SIZE], char ai_player) {
    int row, col;

    // Проверка, есть ли возможность выиграть
    for (row = 0; row < SIZE; row++) {
        for (col = 0; col < SIZE; col++) {
            if (board[row][col] == ' ') {
                board[row][col] = ai_player;
                if (check_winner(board, ai_player)) {
                    return;
                }
                board[row][col] = ' ';
            }
        }
    }

    // Проверка, есть ли угроза проигрыша
    char opponent = (ai_player == 'X') ? 'O' : 'X';
    for (row = 0; row < SIZE; row++) {
        for (col = 0; col < SIZE; col++) {
            if (board[row][col] == ' ') {
                board[row][col] = opponent;
                if (check_winner(board, opponent)) {
                    board[row][col] = ai_player;
                    return;
                }
                board[row][col] = ' ';
            }
        }
    }

    // Если нет выигрыша или угрозы, выбираем случайную свободную ячейку
    do {
        row = rand() % SIZE;
        col = rand() % SIZE;
    } while (board[row][col] != ' ');

    board[row][col] = ai_player;
}

// Основная функция
int main() {
    char board[SIZE][SIZE] = {
        {' ', ' ', ' '},
        {' ', ' ', ' '},
        {' ', ' ', ' '}
    };

    char current_player = 'X';
    int row, col;

    // Инициализация генератора случайных чисел
    srand(time(NULL));

    printf("Добро пожаловать в игру Крестики-Нолики!\n");
    printf("Вы играете за 'X', компьютер играет за 'O'.\n");

    while (true) {
        // Отображение игрового поля
        display_board(board);

        if (current_player == 'X') {
            // Ход игрока
            printf("Ваш ход (строка и столбец, например, 1 2): ");
            scanf("%d %d", &row, &col);

            // Проверка валидности хода
            if (row < 1 || row > SIZE || col < 1 || col > SIZE || board[row - 1][col - 1] != ' ') {
                printf("Неверный ход! Попробуйте снова.\n");
                continue;
            }

            // Выполнение хода
            board[row - 1][col - 1] = current_player;
        } else {
            // Ход ИИ
            printf("Ход компьютера...\n");
            ai_move(board, current_player);
        }

        // Проверка на победу
        if (check_winner(board, current_player)) {
            display_board(board);
            if (current_player == 'X') {
                printf("Вы победили!\n");
            } else {
                printf("Компьютер победил!\n");
            }
            break;
        }

        // Проверка на ничью
        if (check_draw(board)) {
            display_board(board);
            printf("Ничья!\n");
            break;
        }

        // Переключение игрока
        current_player = (current_player == 'X') ? 'O' : 'X';
    }

    return 0;
}
