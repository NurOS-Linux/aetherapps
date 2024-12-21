import pygame
import random

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1028, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juldyz")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Загрузка изображений
background_image = pygame.image.load("background.jpg").convert()
ship_image = pygame.image.load("ship.png").convert_alpha()
star_image = pygame.image.load("star.png").convert_alpha()
explosion_image = pygame.image.load("explosion.png").convert_alpha()

# Масштабирование изображений
ship_image = pygame.transform.scale(ship_image, (40, 60))
star_image = pygame.transform.scale(star_image, (20, 20))
explosion_image = pygame.transform.scale(explosion_image, (60, 60))

# Параметры корабля
ship_width, ship_height = ship_image.get_size()
ship_x = WIDTH // 2 - ship_width // 2
ship_y = HEIGHT - ship_height - 10
ship_speed = 5

# Параметры звезд
star_width, star_height = star_image.get_size()
star_speed = 3
stars = []

# Счёт
score = 0
font = pygame.font.Font(None, 36)

# Взрывы
explosions = []


def create_star():
    star_x = random.randint(0, WIDTH - star_width)
    star_y = 0
    stars.append(pygame.Rect(star_x, star_y, star_width, star_height))


def draw_ship(x, y):
    window.blit(ship_image, (x, y))


def draw_stars():
    for star in stars:
        window.blit(star_image, (star.x, star.y))


def draw_explosions():
    for explosion in explosions:
        window.blit(explosion_image, (explosion[0], explosion[1]))
        explosion[2] += 1
        if explosion[2] > 10:  # Удаляем взрыв через 10 кадров
            explosions.remove(explosion)


def draw_score():
    score_text = font.render(f"Счёт: {score}", True, WHITE)
    window.blit(score_text, (10, 10))


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ship_x > 0:
        ship_x -= ship_speed
    if keys[pygame.K_RIGHT] and ship_x < WIDTH - ship_width:
        ship_x += ship_speed

    if random.randint(1, 100) < 5:
        create_star()

    for star in stars[:]:
        star.y += star_speed
        if star.y > HEIGHT:
            stars.remove(star)

        if star.colliderect(pygame.Rect(ship_x, ship_y, ship_width, ship_height)):
            stars.remove(star)
            score += 1
            explosions.append([star.x, star.y, 0])  # Добавляем взрыв

    # Отрисовка
    window.blit(background_image, (0, 0))  # Фон
    draw_ship(ship_x, ship_y)
    draw_stars()
    draw_explosions()
    draw_score()

    pygame.display.flip()

pygame.quit()
