import pygame
from gamelogic import *
from random import randint
import time

FPS = 60
WIDTH = 900
HEIGHT = 600
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


# Main loop
def main():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    game_loop(display)
    pygame.quit()


def game_loop(display):
    timer = 0
    score = 0
    clock = pygame.time.Clock()
    enemys = [Enemy(30, 30, randint(0, WIDTH - 30), randint(0, HEIGHT - 30), 0) for _ in range(2)]
    crosshair = Crosshair(0, 0)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        timer += 1
        if timer == FPS * 1:
            timer = 0
            enemys.append(Enemy(30, 30, randint(0, WIDTH - 30), randint(0, HEIGHT - 30), 0))

        for enemy in enemys:
            enemy.timer += 1
            if enemy.timer == FPS * 3:
                enemys.remove(enemy)
                if score > 0:
                    score -= 1



        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        crosshair.pos_x = mouse_posx
        crosshair.pos_y = mouse_posy

        left_button, mid_button, right_button = pygame.mouse.get_pressed(num_buttons=3)
        if left_button:
            target_enemy = check_for_collision(enemys, crosshair)
            if target_enemy is not None:
                enemys.remove(target_enemy)
                score += 1

        draw_display(display, enemys, crosshair, score)
        clock.tick(FPS)


def draw_display(display, enemys, crosshair, score):
    display.fill(BLACK)
    draw_enemy(display, enemys)
    draw_crosshair(display, crosshair)

    # fonts :
    font = pygame.font.Font('../assets/GILSANUB.TTF', 28)
    if score > 0:
        color = GREEN
    else:
        color = RED
    text = font.render(f"SCORE : {score}", True, color)
    textRect = text.get_rect()
    textRect.center = (800, 100)
    display.blit(text, textRect)
    pygame.display.flip()


def draw_enemy(display, enemys):
    for enemy in enemys:
        enemy_image = pygame.image.load("../assets/godfather.png")
        enemy_scaled_image = pygame.transform.scale(enemy_image, (50, 50))
        image_get_rect = enemy_scaled_image.get_rect(center=(enemy.pos_x + enemy.width/2,enemy.pos_y + enemy.height/2))
        display.blit(enemy_scaled_image, image_get_rect)


def draw_crosshair(display, crosshair):
    crosshair_image = pygame.image.load("../assets/crosshair.png")
    crosshair_image_center = (crosshair.pos_x, crosshair.pos_y)
    scaled_image = pygame.transform.scale(crosshair_image, (50, 50))
    image_get_rect = scaled_image.get_rect(center=crosshair_image_center)
    display.blit(scaled_image, image_get_rect)


if __name__ == '__main__':
    main()
