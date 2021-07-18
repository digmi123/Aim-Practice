from enum import Enum

from src.main import BLACK


class Button(Enum):
    START_GAME = 0
    OPTIONS = 1
    TEST = {"color": BLACK, "text": "TEST"}
