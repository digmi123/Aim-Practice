import pygame
from gamelogic import *
from random import randint
import time
from gun import Gun
from env import *

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCORE_BOTTOM_LEFT = 0
GUN_TOP_LEFT = 0



clock = pygame.time.Clock()
BACKGROUND = pygame.transform.scale(pygame.image.load('../assets/smoke.png'),
                                    (CONFIG["graphics"]["width"], CONFIG["graphics"]["height"]))


# Main loop
def main():
    pygame.init()
    display = pygame.display.set_mode((CONFIG["graphics"]["width"], CONFIG["graphics"]["height"]))
    start_menu(display)
    # game_loop(display)
    pygame.quit()


def game_loop(display):
    timer = 0
    score = 0
    enemys = []  # [Enemy(50, 50, randint(0, WIDTH - 50), randint(SCORE_BOTTOM_LEFT, GUN_TOP_LEFT)) for _ in range(2)]
    crosshair = Crosshair(0, 0)
    gun = Gun(0, 0)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == 768:
                running = False
            #print(event.type)
            #print(pygame.K_ESCAPE)
            # if event.type == pygame.K_ESCAPE:
            #     running = False

        timer += 1
        if timer >= CONFIG["graphics"]["FPS"] * CONFIG["settings"]["time_to_add_enemy"]:
            timer = 0
            while True:
                temp_enemy = Enemy(50, 50, randint(0, CONFIG["graphics"]["width"] - 50),randint(SCORE_BOTTOM_LEFT, GUN_TOP_LEFT))
                if not enemy_collision(temp_enemy, enemys):
                    enemys.append(temp_enemy)
                    break

        for enemy in enemys:
            enemy.timer += 1
            if enemy.timer >= CONFIG["graphics"]["FPS"] * CONFIG["settings"]["time_to_remove_enemy"]:
                enemys.remove(enemy)
                if score > 0:
                    score -= 1

        mouse_posx, mouse_posy = pygame.mouse.get_pos()
        crosshair.pos_x = mouse_posx
        crosshair.pos_y = mouse_posy
        gun.pos_x = crosshair.pos_x + 80
        gun.pos_y = 0

        left_button, mid_button, right_button = pygame.mouse.get_pressed(num_buttons=3)
        if left_button:
            target_enemy = check_for_collision(enemys, crosshair)
            if target_enemy is not None:
                enemys.remove(target_enemy)
                score += 1

        draw_display(display, enemys, crosshair, score, gun)
        clock.tick(CONFIG["graphics"]["FPS"])


def draw_display(display, enemys, crosshair, score, gun):
    display.blit(BACKGROUND, (0, 0))
    draw_enemy(display, enemys)
    draw_crosshair(display, crosshair)
    draw_gun(display, gun, crosshair)

    # fonts :
    font = pygame.font.Font('../assets/GILSANUB.TTF', 28)
    if score > 0:
        color = GREEN
    else:
        color = RED
    text = font.render(f"SCORE : {score}", True, color)
    textRect = text.get_rect()
    textRect.center = (CONFIG["graphics"]["width"] - textRect.width / 1.5, textRect.height)
    display.blit(text, textRect)
    pygame.display.flip()
    global SCORE_BOTTOM_LEFT
    SCORE_BOTTOM_LEFT = textRect.y + textRect.height


def draw_gun(display, gun, crosshair):
    gun_width = 300
    gun_height = 200
    gun_image = pygame.image.load("../assets/gun.png")
    gun_image_center = (gun.pos_x, CONFIG["graphics"]["height"] - gun_height / 2)
    gun_scaled_image = pygame.transform.scale(gun_image, (gun_width, gun_height))
    image_get_rect = gun_scaled_image.get_rect(center=gun_image_center)
    global GUN_TOP_LEFT
    GUN_TOP_LEFT = image_get_rect.top
    display.blit(gun_scaled_image, image_get_rect)


def draw_enemy(display, enemys):
    for enemy in enemys:
        image_get_rect = enemy.image.get_rect(center=(enemy.pos_x + enemy.width / 2, enemy.pos_y + enemy.height / 2))
        # pygame.draw.rect(display, GREEN, image_get_rect)
        display.blit(enemy.image, image_get_rect)


def draw_crosshair(display, crosshair):
    crosshair_image = pygame.image.load("../assets/crosshair.png")
    crosshair_image_center = (crosshair.pos_x, crosshair.pos_y)
    scaled_image = pygame.transform.scale(crosshair_image, (50, 50))
    image_get_rect = scaled_image.get_rect(center=crosshair_image_center)
    display.blit(scaled_image, image_get_rect)


def start_menu(display):
    clicked = False
    running = True
    text_buttons = {"START GAME": BLACK, "OPTIONS": BLACK}
    font = pygame.font.Font('../assets/GILSANUB.TTF', 34)
    color = BLACK

    while running:
        display.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        mouse_position = pygame.mouse.get_pos()

        for index, text1 in enumerate(text_buttons):
            text = font.render(text1, True, text_buttons[text1])
            text_rect = text.get_rect()
            text_rect.center = (
            CONFIG["graphics"]["width"] // 2, CONFIG["graphics"]["offset"] + index * CONFIG["graphics"]["gap"])
            if text_collision(text_rect, mouse_position):
                text_buttons[text1] = GREEN
                if text1 == "START GAME" and clicked:
                    clicked = False
                    game_loop(display)

                if text1 == "OPTIONS" and clicked:
                    clicked = False
                    options_menu(display)

            else:
                text_buttons[text1] = BLACK
            display.blit(text, text_rect)
        pygame.display.flip()

        clock.tick(CONFIG["graphics"]["FPS"])


def text_collision(text_rect, mouse_positions):
    return text_rect.collidepoint(mouse_positions)


def enemy_collision(temp_enemy, enemys):
    for enemy in enemys:
        if ((temp_enemy.center[0] - enemy.center[0]) ** 2 + (
                temp_enemy.center[1] - enemy.center[1]) ** 2) ** 0.5 < 2 * enemy.radius:
            return True
    return False


def options_menu(display):
    clicked = False
    running = True
    text_buttons = {"BACK": BLACK, "VELOCITY": BLACK}
    font = pygame.font.Font('../assets/GILSANUB.TTF', 34)
    color = BLACK
    text1 = None
    while running:
        display.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        mouse_position = pygame.mouse.get_pos()

        for index, text1 in enumerate(text_buttons):
            text = font.render(text1, True, text_buttons[text1])
            text_rect = text.get_rect()
            text_rect.center = (
            CONFIG["graphics"]["width"] // 2, CONFIG["graphics"]["offset"] + index * CONFIG["graphics"]["gap"])
            if text_collision(text_rect, mouse_position):
                text_buttons[text1] = GREEN
                if text1 == "VELOCITY" and clicked:
                    clicked = False
                    velocity_menu(display)

                if text1 == "BACK" and clicked:
                    clicked = False
                    running = False

            else:
                text_buttons[text1] = BLACK
            display.blit(text, text_rect)
        pygame.display.flip()

        clock.tick(CONFIG["graphics"]["FPS"])


def velocity_menu(display):
    clicked = False
    running = True
    text_buttons = {"BACK": BLACK, "NORMAL": BLACK, "MEDIUM": BLACK, "HARD": BLACK}
    font = pygame.font.Font('../assets/GILSANUB.TTF', 34)
    color = BLACK
    while running:
        display.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        mouse_position = pygame.mouse.get_pos()

        for index, text1 in enumerate(text_buttons):
            text = font.render(text1, True, text_buttons[text1])
            text_rect = text.get_rect()
            text_rect.center = (
            CONFIG["graphics"]["width"] // 2, CONFIG["graphics"]["offset"] + index * CONFIG["graphics"]["gap"])
            if text_collision(text_rect, mouse_position):
                text_buttons[text1] = GREEN

                if text1 == "BACK" and clicked:
                    clicked = False
                    running = False

                if text1 == "NORMAL" and clicked:
                    clicked = False
                    CONFIG["settings"]["time_to_add_enemy"] = 0.7
                    CONFIG["settings"]["time_to_remove_enemy"] = 2.6
                    save_to_config()


                if text1 == "MEDIUM" and clicked:
                    clicked = False
                    CONFIG["settings"]["time_to_add_enemy"] = 0.5
                    CONFIG["settings"]["time_to_remove_enemy"] = 2.2
                    save_to_config()


                if text1 == "HARD" and clicked:
                    clicked = False
                    CONFIG["settings"]["time_to_add_enemy"] = 0.3
                    CONFIG["settings"]["time_to_remove_enemy"] = 1.5
                    save_to_config()

            else:
                text_buttons[text1] = BLACK
            display.blit(text, text_rect)
        pygame.display.flip()

        clock.tick(CONFIG["graphics"]["FPS"])


if __name__ == '__main__':
    main()
