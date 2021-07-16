from enemy import Enemy
from crosshair import Crosshair


def check_for_collision(enemys, crosshair):
    for enemy in enemys:
        if enemy.pos_x < crosshair.pos_x < enemy.width + enemy.pos_x and \
                enemy.pos_y < crosshair.pos_y < enemy.height + enemy.pos_y:
            return enemy
    return None
