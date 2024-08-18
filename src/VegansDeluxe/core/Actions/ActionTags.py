from enum import Enum


class ActionTag(Enum):
    SKIP = 'skip'
    ITEM = 'item'
    ATTACK = 'attack'
    HARMFUL = 'harmful'
    MEDICINE = 'medicine'
    RELOAD = 'reload'
