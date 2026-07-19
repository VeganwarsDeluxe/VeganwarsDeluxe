from enum import Enum

from VegansDeluxe.core.States.State import State


class Skill(State):
    type = 'skill'

class SkillTag(Enum):
    RANGED_WEAPON_ONLY = 'core.skill.ranged_weapon_only'
    MELEE_WEAPON_ONLY = 'core.skill.melee_weapon_only'
