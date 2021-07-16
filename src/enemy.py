

class Enemy:
    def __init__(self, width, height, pos_x, pos_y, velocity):
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity = velocity
        self.timer = 0

