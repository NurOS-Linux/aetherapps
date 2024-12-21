import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1028, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juldyz")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

ship_width = 40
ship_height = 60
ship_x = WIDTH // 2 - ship_width // 2
ship_y = HEIGHT - ship_height - 10
ship_speed = 5


star_width = 20
star_height = 20
star_speed = 3
stars = []


score = 0
font = pygame.font.Font(None, 36)


def create_star():
    star_x = random.randint(0, WIDTH - star_width)
    star_y = 0
    stars.append(pygame.Rect(star_x, star_y, star_width, star_height))

def draw_ship(x, y):
    pygame.draw.rect(window, YELLOW, (x, y, ship_width, ship_height))


def draw_stars():
    for star in stars:
        pygame.draw.rect(window, WHITE, star)


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


    window.fill(BLACK)
    draw_ship(ship_x, ship_y)
    draw_stars()
    draw_score()

    pygame.display.flip()

pygame.quit()
