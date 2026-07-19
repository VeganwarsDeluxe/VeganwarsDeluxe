from enum import Enum


class ActionTag(Enum):
    SKIP = 'core.action.skip'
    ITEM = 'core.action.item'
    ATTACK = 'core.action.attack'
    HARMFUL = 'core.action.harmful'
    MEDICINE = 'core.action.medicine'
    RELOAD = 'core.action.reload'
